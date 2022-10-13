from sqlalchemy.orm import Session

from . import models, schemas


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_mercenaries(db: Session):
    return db.query(models.Mercenary).all()


def create_mercenary(db: Session, mercenary: schemas.MercenaryCreate):
    db_mercenary = models.Mercenary(name=mercenary.name)
    db.add(db_mercenary)
    db.commit()
    db.refresh(db_mercenary)
    return db_mercenary
