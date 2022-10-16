from pydantic import BaseModel
from sql_app.enums import Role, Rarity, MinionType, Faction
from typing import List


class EquipmentBase(BaseModel):
    name: str
    desc: str


class EquipmentCreate(EquipmentBase):
    mercenary_id: int


class Equipment(EquipmentBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class MercenaryBase(BaseModel):
    name: str = ''
    role: Role = Role.PROTECTOR
    rarity: Rarity = Rarity.RARE
    minion_type: MinionType = MinionType.NONE
    faction: Faction = Faction.NONE
    equipments: List[Equipment] = []


class MercenaryCreate(MercenaryBase):
    pass


class Mercenary(MercenaryBase):
    id: int = 0

    class Config:
        orm_mode = True
