from sqlalchemy import Column, String, Integer

from .database import Base


class Mercenary(Base):
    __tablename__ = "mercenaries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    role = Column(String)
    rarity = Column(String)
    minion_type = Column(String)
    faction = Column(String)

class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
