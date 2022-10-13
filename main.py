import argparse
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

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
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wiki', type=str2bool, default=False, required=False,
                        help='Read text file of wiki page sources to make dataset')

    main(parser.parse_args())
