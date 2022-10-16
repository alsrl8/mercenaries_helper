from enum import Enum


class Role(str, Enum):
    PROTECTOR = 'Protector'
    CASTER = 'Caster'
    FIGHTER = 'Fighter'


class Rarity(str, Enum):
    RARE = 'Rare'
    EPIC = 'Epic'
    LEGENDARY = 'Legendary'


class MinionType(str, Enum):
    DRAENEI = 'Draenei'
    DWARF = 'Dwarf'
    GNOME = 'Gnome'
    HIGH_ELF = 'High Elf'
    HUMAN = 'Human'
    NIGHT_ELF = 'Night Elf'
    WORGEN = 'Worgen'
    BLOOD_ELF = 'Blood Elf'
    GOBLIN = 'Goblin'
    HALF_ORC = 'Half-Orc'
    ORC = 'Orc'
    TAUREN = 'Tauren'
    TROLL = 'Troll'
    UNDEAD = 'Undead'
    NONE = 'None'
    BEAST = 'Beast'
    CENTAUR = 'Centaur'
    DEMON = 'Demon'
    DRAGON = 'Dragon'
    EGG = 'Egg'
    ELEMENTAL = 'Elemental'
    FURBOLG = 'Furbolg'
    GRONN = 'Gronn'
    MECH = 'Mech'
    MURLOC = 'Murloc'
    NAGA = 'Naga'
    OGRE = 'Ogre'
    OLD_GOD = 'Old God'
    PANDAREN = 'Pandaren'
    PIRATE = 'Pirate'
    QUILBOAR = 'Quilboar'
    TOTEM = 'Totem'
    TREANT = 'Treant'


class Faction(str, Enum):
    ALLIANCE = 'Alliance'
    HORDE = 'Horde'
    NONE = 'None'