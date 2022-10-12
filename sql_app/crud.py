from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


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
    print(f'{db_mercenary=}')
    print(f'id: {db_mercenary.id}, name: {db_mercenary.name}')
    print(f'type(db_user): {type(db_mercenary)}')
    return db_mercenary

