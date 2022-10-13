from sqlalchemy.orm import Session

from . import models, schemas


def get_mercenaries(db: Session):
    return db.query(models.Mercenary).all()


def create_mercenary(db: Session, mercenary: schemas.MercenaryCreate):
    db_mercenary = models.Mercenary(name=mercenary.name)
    db.add(db_mercenary)
    db.commit()
    db.refresh(db_mercenary)
    return db_mercenary
