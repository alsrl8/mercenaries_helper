from pydantic import BaseModel
from sql_app.enums import Role, Rarity, MinionType, Faction
from typing import List, Optional


class AbilityBase(BaseModel):
    name: str
    speed: Optional[int] = 0
    cooldown: Optional[int] = 0
    spell_school: Optional[str] = ''
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
    abilities: List[Ability] = []


class MercenaryCreate(MercenaryBase):
    pass


class Mercenary(MercenaryBase):
    id: int = 0

    class Config:
        orm_mode = True
