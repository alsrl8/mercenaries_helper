from sqlalchemy.orm import Session

from . import models, schemas


def get_mercenaries(db: Session):
    return db.query(models.Mercenary).all()


def get_mercenary_by_name(db: Session, name: str):
    return db.query(models.Mercenary).filter(models.Mercenary.name == name).first()


def create_mercenary(db: Session, mercenary: schemas.MercenaryCreate):
    db_mercenary = \
        models.Mercenary(name=mercenary.name,
                         role=mercenary.role,
                         rarity=mercenary.rarity,
                         minion_type=mercenary.minion_type,
                         faction=mercenary.faction
                         )
    db.add(db_mercenary)
    db.commit()
    db.refresh(db_mercenary)
    return db_mercenary
