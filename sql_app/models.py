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
    abilities = relationship("Ability", back_populates="owner")


class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    text = Column(String)
    owner_id = Column(Integer, ForeignKey("mercenaries.id"))

    owner = relationship("Mercenary", back_populates="equipments")


class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    speed = Column(Integer)
    cooldown = Column(Integer)
    spell_school = Column(String)
    text = Column(String)
    owner_id = Column(Integer, ForeignKey("mercenaries.id"))

    owner = relationship("Mercenary", back_populates="abilities")


class Zone:
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    bounties = relationship("Bounty", back_populates="zone")


class Bounty:
    __tablename__ = "bounties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))

    zone = relationship("Zone", back_populates="bounties")
