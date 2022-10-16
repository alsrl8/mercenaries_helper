from pydantic import BaseModel
from sql_app.enums import Role, Rarity, MinionType, Faction


class MercenaryBase(BaseModel):
    name: str = ''
    role: Role = Role.PROTECTOR
    rarity: Rarity = Rarity.RARE
    minion_type: MinionType = MinionType.NONE
    faction: Faction = Faction.NONE


class MercenaryCreate(MercenaryBase):
    pass


class Mercenary(MercenaryBase):
    id: int = 0

    class Config:
        orm_mode = True
