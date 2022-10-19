from pydantic import BaseModel
from sql_app.enums import Role, Rarity, MinionType, Faction
from typing import List


class AbilityBase(BaseModel):
    name: str
    speed: int
    cooldown: int
    spell_school: str
    text: str


class AbilityCreate(AbilityBase):
    pass


class Ability(AbilityBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class EquipmentBase(BaseModel):
    name: str
    text: str


class EquipmentCreate(EquipmentBase):
    pass


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
