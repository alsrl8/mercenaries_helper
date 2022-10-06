from typing import Union
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RoleEnum(str, Enum):
    protector = 'Protector'
    fighter = 'Fighter'
    caster = 'Caster'


class RarityEnum(str, Enum):
    rare = 'Rare'
    epic = 'Epic'
    legendary = 'Legendary'


class Mercenary(BaseModel):
    name: str
    role: RoleEnum
    rarity: RarityEnum
    # TODO minion type 추가
    # TODO faction(진영) 어떻게 처리할지


@app.get("/")
def read_root():
    return {"Hello", "World"}
