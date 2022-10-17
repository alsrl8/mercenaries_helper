from sqlalchemy.orm import Session

from . import models, schemas


def get_mercenaries(db: Session):
    return db.query(models.Mercenary).all()


def get_mercenary(db: Session, id: int = 0, name: str = ''):
    if not id and not name:
        return None
    data = db.query(models.Mercenary).outerjoin(models.Equipment)
    if id:
        data = data.filter(models.Mercenary.id == id)
    if name:
        data = data.filter(models.Mercenary.name == name)
    return data.first()


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


def create_equipment(db: Session, equipment: schemas.EquipmentCreate):
    db_equipment = \
        models.Equipment(name=equipment.name,
                         desc=equipment.desc,
                         owner_id=equipment.mercenary_id
                         )
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment
