from sqlalchemy.orm import Session

from . import models, schemas


def get_mercenaries(db: Session):
    return db.query(models.Mercenary).all()


def get_mercenary(db: Session, id: int = 0, name: str = ''):
    if not id and not name:
        return None
    data = db.query(models.Mercenary).outerjoin(models.Equipment).outerjoin(models.Ability)
    if id:
        data = data.filter(models.Mercenary.id == id)
    if name:
        data = data.filter(models.Mercenary.name == name)
    return data.first()


def get_equipment(db: Session, id: int = 0, name: str = '', owner_id: int = 0):
    if not id and not name:
        return None
    if owner_id:
        data = db.query(models.Equipment).join(models.Mercenary).filter(models.Mercenary.id == owner_id)
    else:
        data = db.query(models.Equipment)
    if id:
        data = data.filter(models.Equipment.id == id)
    if name:
        data = data.filter(models.Equipment.name == name)
    return data.first()


def get_ability(db: Session, id: int = 0, name: str = '', owner_id: int = 0):
    if not id and not name:
        return None
    if owner_id:
        data = db.query(models.Ability).join(models.Mercenary).filter(models.Mercenary.id == owner_id)
    else:
        data = db.query(models.Ability)
    if id:
        data = data.filter(models.Ability.id == id)
    if name:
        data = data.filter(models.Ability.name == name)
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
    db_equipment = models.Equipment(name=equipment.name,
                                    text=equipment.text)
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


def create_ability(db: Session, ability: schemas.AbilityCreate):
    db_ability = models.Ability(name=ability.name,
                                speed=ability.speed,
                                cooldown=ability.cooldown,
                                spell_school=ability.spell_school,
                                text=ability.text
                                )
    db.add(db_ability)
    db.commit()
    db.refresh(db_ability)
    return db_ability


def update_equipment(db: Session, name: str, new_equipment: schemas.Equipment):
    find_equipment = get_equipment(db=db, name=name)
    if new_equipment.name:
        find_equipment.name = new_equipment.name
    if new_equipment.text:
        find_equipment.text = new_equipment.text
    if new_equipment.owner_id:
        find_equipment.owner_id = new_equipment.owner_id
    db.commit()
    db.refresh(find_equipment)
    return find_equipment


def update_ability(db: Session, name: str, new_ability: schemas.Ability):
    find_ability = get_ability(db=db, name=name)
    if new_ability.name:
        find_ability.name = new_ability.name
    if new_ability.speed:
        find_ability.speed = new_ability.speed
    if new_ability.cooldown:
        find_ability.cooldown = new_ability.cooldown
    if new_ability.spell_school:
        find_ability.spell_school = new_ability.spell_school
    if new_ability.text:
        find_ability.text = new_ability.text
    if new_ability.owner_id:
        find_ability.owner_id = new_ability.owner_id
    db.commit()
    db.refresh(find_ability)
    return find_ability
