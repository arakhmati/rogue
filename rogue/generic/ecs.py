"""
Generic Entity-Component-System code

In this file, access to private members of EntityComponentDatabase[Component] class is allowed.
"""


from typing import (
    Protocol,
    Generic,
    Type,
    TypeVar,
    Iterable,
    Optional,
    Tuple,
    Generator,
)

import attr
import pyrsistent.typing

from rogue.generic.functions import type_to_str


@attr.s(frozen=True, kw_only=True)
class Entity:
    unique_id: int = attr.ib()


SetOfEntities = pyrsistent.typing.PSet[Entity]

ComponentTemplate = TypeVar("ComponentTemplate")
IterableOfComponents = Iterable[ComponentTemplate]
SetOfComponents = pyrsistent.typing.PSet[ComponentTemplate]
ComponentStr = str
MapFromComponentStrToComponent = pyrsistent.typing.PMap[ComponentStr, ComponentTemplate]
MapFromEntityToMapFromComponentStrToComponent = pyrsistent.typing.PMap[
    Entity, MapFromComponentStrToComponent[ComponentTemplate]
]
MapFromComponentToSetOfEntities = pyrsistent.typing.PMap[ComponentStr, SetOfEntities]


class EntityComponentDatabase(Generic[ComponentTemplate], pyrsistent.PClass):
    _last_unique_id: int = pyrsistent.field(mandatory=True)
    _entities: MapFromEntityToMapFromComponentStrToComponent[ComponentTemplate] = pyrsistent.field(
        initial=pyrsistent.pmap
    )


class FilterFunction(Protocol):
    def __call__(self, components: Iterable[ComponentTemplate]) -> bool:
        ...


def create_ecdb() -> EntityComponentDatabase[ComponentTemplate]:
    return EntityComponentDatabase(_last_unique_id=0)


def add_entity(
    *,
    ecdb: EntityComponentDatabase[ComponentTemplate],
    components: Optional[IterableOfComponents[ComponentTemplate]] = None,
) -> Tuple[EntityComponentDatabase[ComponentTemplate], Entity]:
    unique_id = ecdb._last_unique_id  # pylint: disable=protected-access
    new_unique_id = unique_id + 1

    entity = Entity(unique_id=unique_id)
    new_entities = ecdb._entities.set(entity, pyrsistent.pmap())  # pylint: disable=protected-access

    ecdb = ecdb.set(_last_unique_id=new_unique_id, _entities=new_entities)

    if components is not None:
        for component in components:
            ecdb = add_component(ecdb=ecdb, entity=entity, component=component)

    return ecdb, entity


def add_component(
    *, ecdb: EntityComponentDatabase[ComponentTemplate], entity: Entity, component: ComponentTemplate
) -> EntityComponentDatabase[ComponentTemplate]:
    component_type = type(component)
    component_type_str = type_to_str(component_type)

    entities = ecdb._entities  # pylint: disable=protected-access
    entity_components = entities.get(entity, pyrsistent.pmap())
    new_entity_components = entity_components.set(component_type_str, component)
    new_entities = entities.set(entity, new_entity_components)

    return ecdb.set(_entities=new_entities)


def query_entities(
    *,
    ecdb: EntityComponentDatabase[ComponentTemplate],
    component_types: Optional[Iterable[Type[ComponentTemplate]]] = None,
    filter_function: Optional[FilterFunction] = None,
) -> Generator[Tuple[Entity, Tuple[Optional[ComponentTemplate], ...]], None, None]:
    for entity, components in ecdb._entities.items():  # pylint: disable=protected-access

        if filter_function is not None:
            if not filter_function(components=components.values()):
                continue

        requested_components: Tuple[Optional[ComponentTemplate], ...]
        if component_types is None:
            requested_components = tuple(components.values())
        else:
            component_types_as_str = [type_to_str(component_type) for component_type in component_types]
            requested_components = tuple(
                components[component_type_str] if component_type_str in components else None
                for component_type_str in component_types_as_str
            )

        yield entity, requested_components


# Systems
SystemPriority = int
SystemTemplate = TypeVar("SystemTemplate")
SetOfSystems = pyrsistent.typing.PSet[SystemTemplate]
MapFromPriorityToSetOfSystems = pyrsistent.typing.PMap[SystemPriority, SetOfSystems[SystemTemplate]]


class Systems(Generic[SystemTemplate], pyrsistent.PClass):
    _priority_to_systems: MapFromPriorityToSetOfSystems[SystemTemplate] = pyrsistent.field(initial=pyrsistent.pmap)


def create_systems() -> Systems[SystemTemplate]:
    return Systems()


def add_system(
    *, systems: Systems[SystemTemplate], system: SystemTemplate, priority: SystemPriority
) -> Systems[SystemTemplate]:
    assert priority >= 0, "Priority must be a positive number!"

    priority_to_systems = systems._priority_to_systems  # pylint: disable=protected-access
    systems_with_given_priority = priority_to_systems.get(priority, pyrsistent.pset())
    new_systems_with_given_priority = systems_with_given_priority.add(system)
    new_priority_to_systems = priority_to_systems.set(priority, new_systems_with_given_priority)
    return systems.set(_priority_to_systems=new_priority_to_systems)


def get_systems(*, systems: Systems[SystemTemplate]) -> Generator[SystemTemplate, None, None]:
    for _, systems_with_given_priority in systems._priority_to_systems.items():  # pylint: disable=protected-access
        for system in systems_with_given_priority:
            yield system


# Systems End
