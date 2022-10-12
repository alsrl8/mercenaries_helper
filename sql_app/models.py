from sqlalchemy import Column, String, Integer

from .database import Base


class Mercenary(Base):
    __tablename__ = "mercenaries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
