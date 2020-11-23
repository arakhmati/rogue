import typing

import attr
import pyrsistent.typing

import pygcurse


@attr.s(frozen=True, kw_only=True)
class Entity:
    unique_id: int = attr.ib()


ComponentTemplate = typing.TypeVar("ComponentTemplate")


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

IterableOfComponents = typing.Iterable[ComponentTemplate]
SetOfComponents = pyrsistent.typing.PSet[ComponentTemplate]

SetOfSystems = pyrsistent.typing.PSet[System]

Priority = int

# Type Definitions End


# EntityComponentSystem

ComponentStr = str
MapFromComponentStrToComponent = pyrsistent.typing.PMap[ComponentStr, ComponentTemplate]
MapFromEntityToMapFromComponentStrToComponent = pyrsistent.typing.PMap[
    Entity, MapFromComponentStrToComponent[ComponentTemplate]
]
MapFromComponentToSetOfEntities = pyrsistent.typing.PMap[ComponentStr, SetOfEntities]
MapFromPriorityToSetOfSystems = pyrsistent.typing.PMap[Priority, SetOfSystems]


class EntityComponentSystem(typing.Generic[ComponentTemplate], pyrsistent.PClass):
    _last_unique_id: int = pyrsistent.field(mandatory=True)
    _entities: MapFromEntityToMapFromComponentStrToComponent[ComponentTemplate] = pyrsistent.field(
        initial=pyrsistent.pmap
    )
    _components: MapFromComponentToSetOfEntities = pyrsistent.field(initial=pyrsistent.pmap)
    _systems: MapFromPriorityToSetOfSystems = pyrsistent.field(initial=pyrsistent.pmap)


# EntityComponentSystem End


# Others
class QueryFunction(typing.Protocol):
    def __call__(self, ecs: EntityComponentSystem[ComponentTemplate], entity: Entity) -> bool:
        ...


# Others End
