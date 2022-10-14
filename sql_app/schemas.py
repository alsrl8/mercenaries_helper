from pydantic import BaseModel


class MercenaryBase(BaseModel):
    name: str
    role: str
    rarity: str
    minion_type: str
    faction: str


class MercenaryCreate(MercenaryBase):
    pass


class Mercenary(MercenaryBase):
    id: int

    class Config:
        orm_mode = True
