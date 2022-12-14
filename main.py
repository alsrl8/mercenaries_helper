import argparse
from typing import List

from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from tqdm import tqdm

import utils
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sql_app.schemas import MercenaryCreate, EquipmentCreate, AbilityCreate, BountyCreate

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.get("/mercenaries/", response_model=List[schemas.Mercenary])
def read_mercenaries(request: Request, db: Session = Depends(get_db)):
    mercenaries = crud.get_mercenaries(db)
    return templates.TemplateResponse('mercenaries.html', {'request': request, 'mercenaries': mercenaries})


@app.get("/mercenary/", response_model=schemas.Mercenary)
def read_mercenary(request: Request, id: int = 0, name: str = '', db: Session = Depends(get_db)):
    mercenary = crud.get_mercenary(db=db, id=id, name=name)
    if not mercenary:
        mercenary = schemas.Mercenary()
    data = {'request': request,
            'name': mercenary.name,
            'role': mercenary.role,
            'rarity': mercenary.rarity,
            'minion_type': mercenary.minion_type,
            'faction': mercenary.faction,
            'path': f'images/mercenaries/{mercenary.name}.png',
            'equipments': mercenary.equipments,
            'abilities': mercenary.abilities
            }
    return templates.TemplateResponse('mercenary.html', context=data)


@app.get("/bounties", response_model=None)
def read_bounties(request: Request):
    bounties = crud.get_bounties(db=SessionLocal())
    return templates.TemplateResponse('bounties.html', {'request': request, 'bounties': bounties})


@app.get("/add_equipment/")
def create_equipment(request: Request):
    return templates.TemplateResponse('add_equipment.html', {'request': request})


@app.post("/add_equipment/", response_model=schemas.Equipment)
def create_equipment(mercenary_id: int = Form(), equipment_name: str = Form(), desc: str = Form(), db: Session = Depends(get_db)):
    equipment = schemas.EquipmentCreate(mercenary_id=mercenary_id, name=equipment_name, desc=desc)
    db_equipment = crud.create_equipment(db, equipment)
    return db_equipment


def store_all_mercenaries():
    mercenary_names = utils.read_all_mercenary_names_from_local()
    for name in tqdm(mercenary_names):
        mercenary = utils.read_mercenary_from_local(name)
        db_mercenary = MercenaryCreate(name=mercenary['Name'],
                                       role=mercenary['Role'],
                                       rarity=mercenary['Rarity'],
                                       minion_type=mercenary['Minion type'],
                                       faction=mercenary['Faction']
                                       )
        find_mercenary = crud.get_mercenary(db=SessionLocal(), name=name)
        if not find_mercenary:
            equipments = mercenary['Equipments']
            for equipment in equipments:
                find_equipment = crud.get_equipment(db=SessionLocal(), name=equipment['Name'])
                if not find_equipment:
                    db_equipment = EquipmentCreate(name=equipment['Name'], text=equipment['Text'])
                    crud.create_equipment(db=SessionLocal(), equipment=db_equipment)
            abilities = mercenary['Abilities']
            for ability in abilities:
                find_ability = crud.get_ability(db=SessionLocal(), name=ability['Name'])
                if not find_ability:
                    db_ability = AbilityCreate(name=ability['Name'],
                                               speed=ability['Speed'],
                                               cooldown=ability['Cooldown'],
                                               spell_school=ability['Spell school'],
                                               text=ability['Text']
                                               )
                    crud.create_ability(db=SessionLocal(), ability=db_ability)
            create_mercenary = crud.create_mercenary(db=SessionLocal(), mercenary=db_mercenary)
            for equipment in equipments:
                new_equipment = schemas.Equipment(id=0, name='', text='', owner_id=create_mercenary.id)
                crud.update_equipment(db=SessionLocal(), name=equipment['Name'], new_equipment=new_equipment)
            for ability in abilities:
                new_ability = schemas.Ability(id=0, name='', speed=0, cooldown=0, spell_school='', text='', owner_id=create_mercenary.id)
                crud.update_ability(db=SessionLocal(), name=ability['Name'], new_ability=new_ability)


def store_all_bounties():
    bounty_names_with_links = utils.read_all_bounty_names_with_links_from_local()
    for name in tqdm(bounty_names_with_links):
        for difficulty in ['Normal', 'Heroic']:
            if difficulty not in bounty_names_with_links[name]:
                continue
            link = bounty_names_with_links[name][difficulty]
            bounty = utils.read_bounty_from_wiki(name, link)
            find_zone = crud.get_zone(db=SessionLocal(), name=bounty['Zone'])
            if not find_zone:
                db_zone = schemas.ZoneCreate(name=bounty['Zone'])
                find_zone = crud.create_zone(db=SessionLocal(), zone=db_zone)
            if crud.get_bounty(db=SessionLocal(), name=name, difficulty=difficulty):
                continue
            db_bounty = schemas.BountyCreate(name=bounty['Name'], difficulty=difficulty, zone_id=find_zone.id)
            crud.create_bounty(db=SessionLocal(), bounty=db_bounty)


def str2bool(v):
    if isinstance(v, bool):
        return v
    elif v.lower() in ('yes', 'y', 'true', 't', '1'):
        return True
    elif v.lower() in ('no', 'n', 'false', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentError()


def main(args):
    if args.mercenary:
        print(f'Scraping mercenaries from hearthstone wiki')
        utils.write_all_mercenaries()
    if args.bounty:
        print(f'Scraping bounties from hearthstone wiki')
        utils.write_all_bounties()
    if args.init:
        print(f'Inserting mercenaries and bounties into database')
        store_all_mercenaries()
        store_all_bounties()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mercenary', type=str2bool, default=False, required=False,
                        help='Read mercenary data from wiki page')
    parser.add_argument('-b', '--bounty', type=str2bool, default=False, required=False,
                        help='Read bounty data from wiki page')
    parser.add_argument('-i', '--init', type=str2bool, default=False, required=False,
                        help='Input all mercenaries and bounties data into database')

    main(parser.parse_args())
