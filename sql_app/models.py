from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Mercenary(Base):
    __tablename__ = "mercenaries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    role = Column(String)
    rarity = Column(String)
    minion_type = Column(String)
    faction = Column(String)

    equipments = relationship("Equipment", back_populates="owner")


class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    desc = Column(String)
    owner_id = Column(Integer, ForeignKey("mercenaries.id"))

    owner = relationship("Mercenary", back_populates="equipments")
