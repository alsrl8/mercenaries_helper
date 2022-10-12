from pydantic import BaseModel


class MercenaryBase(BaseModel):
    name: str


class MercenaryCreate(MercenaryBase):
    pass


class Mercenary(MercenaryBase):
    id: int

    class Config:
        orm_mode = True
