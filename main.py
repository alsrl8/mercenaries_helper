import argparse
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from utils import read_all_mercenary_names_from_local, read_mercenary_from_local
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sql_app.schemas import MercenaryCreate

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/mercenaries/", response_model=List[schemas.Mercenary])
def read_mercenaries(db: Session = Depends(get_db)):
    mercenaries = crud.get_mercenaries(db)
    return mercenaries


@app.post("/mercenaries/", response_model=schemas.Mercenary)
def create_mercenary(mercenary: schemas.MercenaryCreate, db: Session = Depends(get_db)):
    db_mercenary = crud.create_mercenary(db, mercenary)
    return db_mercenary


def input_all_mercenaries():
    mercenary_names = read_all_mercenary_names_from_local()
    for name in mercenary_names:
        mercenary = read_mercenary_from_local(name)
        db_mercenary = MercenaryCreate(name=mercenary['Name'])
        crud.create_mercenary(db=SessionLocal(), mercenary=db_mercenary)



def str2bool(v):
    if isinstance(v, bool):
        return v
    elif v.lower() in ('yes', 'y', 'true', 't', '1'):
        return True
    elif v.lower() in ('no', 'n', 'false', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentParser('Boolean value is expected')


def main(args):
    input_all_mercenaries()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wiki', type=str2bool, default=False, required=False,
                        help='Read text file of wiki page sources to make dataset')

    main(parser.parse_args())
