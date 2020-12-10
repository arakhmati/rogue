from enum import Enum, auto


import pyrsistent


class TypeEnum(Enum):
    Hero = auto()

    # Enemy Types
    Hobgoblin = auto()

    # Weapon Types
    Dagger = auto()
    Mace = auto()
    Sword = auto()
    DoubleSword = auto()

    # Item Types
    Gold = auto()
    Potion = auto()

    # Level-related Types
    Door = auto()
    Room = auto()


TYPE_ENUM_TO_STRING = {value: value.name for value in TypeEnum}
STRING_TO_TYPE_ENUM = {value: key for key, value in TYPE_ENUM_TO_STRING.items()}

ENEMY_TYPES = pyrsistent.s(TypeEnum.Hobgoblin)

WEAPON_TYPES = pyrsistent.s(TypeEnum.Dagger, TypeEnum.Mace, TypeEnum.Sword, TypeEnum.DoubleSword)

ITEM_TYPES = pyrsistent.s(TypeEnum.Gold, TypeEnum.Potion)
ITEM_TYPES = ITEM_TYPES.update(WEAPON_TYPES)
