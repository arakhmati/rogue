import typing

import attr
import pyrsistent.typing

import pygcurse


@attr.s(frozen=True, kw_only=True)
class Entity:
    unique_id: int = attr.ib()


# Components
@attr.s(frozen=True, kw_only=True)
class PositionComponent:
    y_axis: int = attr.ib()
    x_axis: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class VelocityComponent:
    x_axis: int = attr.ib()
    y_axis: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class SizeComponent:
    height: int = attr.ib()
    width: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class AppearanceComponent:
    symbol: str = attr.ib()
    color: str = attr.ib()


@attr.s(frozen=True, kw_only=True)
class MoneyComponent:
    amount: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class HealthComponent:
    amount: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class DamageComponent:
    damage: int = attr.ib()


Component = typing.Union[
    PositionComponent,
    VelocityComponent,
    SizeComponent,
    AppearanceComponent,
    MoneyComponent,
    HealthComponent,
    DamageComponent,
]


# Components End


# Systems
@attr.s(frozen=True, kw_only=True)
class PygcurseRenderSystem:
    window: pygcurse.PygcurseWindow = attr.ib()


@attr.s(frozen=True, kw_only=True)
class MovementSystem:
    ...


@attr.s(frozen=True, kw_only=True)
class EnemyAISystem:
    ...


System = typing.Union[PygcurseRenderSystem, MovementSystem, EnemyAISystem]
# Systems End


# Type Definitions
SetOfEntities = pyrsistent.typing.PSet[Entity]

IterableOfComponents = typing.Iterable[Component]
SetOfComponents = pyrsistent.typing.PSet[Component]

SetOfSystems = pyrsistent.typing.PSet[System]

Priority = int

# Type Definitions End


# EntityComponentSystem

ComponentStr = str
MapFromComponentStrToComponent = pyrsistent.typing.PMap[ComponentStr, Component]
MapFromEntityToMapFromComponentStrToComponent = pyrsistent.typing.PMap[Entity, MapFromComponentStrToComponent]
MapFromComponentToSetOfEntities = pyrsistent.typing.PMap[ComponentStr, SetOfEntities]
MapFromPriorityToSetOfSystems = pyrsistent.typing.PMap[Priority, SetOfSystems]


class EntityComponentSystem(pyrsistent.PClass):
    _last_unique_id: int = pyrsistent.field(mandatory=True)
    _entities: MapFromEntityToMapFromComponentStrToComponent = pyrsistent.field(initial=pyrsistent.pmap)
    _components: MapFromComponentToSetOfEntities = pyrsistent.field(initial=pyrsistent.pmap)
    _systems: MapFromPriorityToSetOfSystems = pyrsistent.field(initial=pyrsistent.pmap)


# EntityComponentSystem End


# Others
class QueryFunction(typing.Protocol):
    def __call__(self, ecs: EntityComponentSystem, entity: Entity) -> bool:
        ...


# Others End
