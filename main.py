import argparse
from typing import List

from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import utils
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sql_app.schemas import MercenaryCreate

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
def read_mercenaries(db: Session = Depends(get_db)):
    mercenaries = crud.get_mercenaries(db)
    return mercenaries


@app.get("/mercenary/", response_model=schemas.Mercenary)
def read_mercenary(request: Request, id: int = 0, name: str = '', db: Session = Depends(get_db)):
    mercenary = crud.get_mercenary(db=db, id=id, name=name)
    if not mercenary:
        mercenary = schemas.Mercenary()
    return templates.TemplateResponse('mercenary.html', {'request': request, 'name': mercenary.name, 'role': mercenary.role, 'path': f'images/{mercenary.name}.webp'})


@app.post("/mercenaries/", response_model=schemas.Mercenary)
def create_mercenary(mercenary: schemas.MercenaryCreate, db: Session = Depends(get_db)):
    db_mercenary = crud.create_mercenary(db, mercenary)
    return db_mercenary


def input_all_mercenaries():
    mercenary_names = utils.read_all_mercenary_names_from_local()
    for name in mercenary_names:
        mercenary = utils.read_mercenary_from_local(name)
        db_mercenary = MercenaryCreate(name=mercenary['Name'],
                                       role=mercenary['Role'],
                                       rarity=mercenary['Rarity'],
                                       minion_type=mercenary['Minion type'],
                                       faction=mercenary['Faction']
                                       )
        find_mercenary = crud.get_mercenary(db=SessionLocal(), name=name)
        if not find_mercenary:
            crud.create_mercenary(db=SessionLocal(), mercenary=db_mercenary)


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
    if args.wiki:
        print(f'Scraping mercenaries from hearthstone wiki')
        utils.write_all_mercenaries()
    if args.init:
        print(f'Inserting mercenaries into database')
        input_all_mercenaries()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wiki', type=str2bool, default=False, required=False,
                        help='Read text file of wiki page sources to make dataset')
    parser.add_argument('--init', type=str2bool, default=False, required=False,
                        help='Input all mercenaries information into database')

    main(parser.parse_args())
