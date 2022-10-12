from pydantic import BaseModel
from typing import Union, List


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str = ''


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class MercenaryBase(BaseModel):
    name: str


class MercenaryCreate(MercenaryBase):
    pass


class Mercenary(MercenaryBase):
    id: int

    class Config:
        orm_mode = True
