from typing import Union, Iterable

import attr
import pyrsistent
from pyrsistent.typing import PSet

from rogue.generic.ecs import Entity
from rogue.types import TypeEnum


@attr.s(frozen=True, kw_only=True)
class PositionComponent:
    y_axis: int = attr.ib()
    x_axis: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, y_axis: int, x_axis: int) -> "PositionComponent":
        return cls(y_axis=y_axis, x_axis=x_axis)


@attr.s(frozen=True, kw_only=True)
class VelocityComponent:
    x_axis: int = attr.ib()
    y_axis: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, y_axis: int, x_axis: int) -> "VelocityComponent":
        return cls(y_axis=y_axis, x_axis=x_axis)


@attr.s(frozen=True, kw_only=True)
class SizeComponent:
    height: int = attr.ib()
    width: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, height: int, width: int) -> "SizeComponent":
        return cls(height=height, width=width)


@attr.s(frozen=True, kw_only=True)
class TypeComponent:
    entity_type: TypeEnum = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, entity_type: TypeEnum) -> "TypeComponent":
        return cls(entity_type=entity_type)


@attr.s(frozen=True, kw_only=True)
class MoneyComponent:
    amount: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, amount: int) -> "MoneyComponent":
        return cls(amount=amount)


@attr.s(frozen=True, kw_only=True)
class HealthComponent:
    amount: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, amount: int) -> "HealthComponent":
        return cls(amount=amount)


@attr.s(frozen=True, kw_only=True)
class DamageComponent:
    damage: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, damage: int) -> "DamageComponent":
        return cls(damage=damage)


@attr.s(frozen=True, kw_only=True)
class InventoryComponent:
    entities: PSet[Entity] = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, entities: Iterable[Entity]) -> "InventoryComponent":
        return cls(entities=pyrsistent.pset(entities))


@attr.s(frozen=True, kw_only=True)
class EquipmentComponent:
    entities: PSet[Entity] = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, entities: Iterable[Entity]) -> "EquipmentComponent":
        return cls(entities=pyrsistent.pset(entities))


ComponentUnion = Union[
    PositionComponent,
    VelocityComponent,
    SizeComponent,
    TypeComponent,
    MoneyComponent,
    HealthComponent,
    DamageComponent,
    InventoryComponent,
    EquipmentComponent,
]
