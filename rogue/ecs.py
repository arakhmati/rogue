"""
Generic Entity-Component-System code

In this file, access to private members of EntityComponentSystem[Component] class is allowed.
"""


import typing

import attr
import pyrsistent.typing

from rogue.generic import type_to_str


@attr.s(frozen=True, kw_only=True)
class Entity:
    unique_id: int = attr.ib()


SetOfEntities = pyrsistent.typing.PSet[Entity]

ComponentTemplate = typing.TypeVar("ComponentTemplate")
IterableOfComponents = typing.Iterable[ComponentTemplate]
SetOfComponents = pyrsistent.typing.PSet[ComponentTemplate]
ComponentStr = str
MapFromComponentStrToComponent = pyrsistent.typing.PMap[ComponentStr, ComponentTemplate]
MapFromEntityToMapFromComponentStrToComponent = pyrsistent.typing.PMap[
    Entity, MapFromComponentStrToComponent[ComponentTemplate]
]
MapFromComponentToSetOfEntities = pyrsistent.typing.PMap[ComponentStr, SetOfEntities]


class EntityComponentSystem(typing.Generic[ComponentTemplate], pyrsistent.PClass):
    _last_unique_id: int = pyrsistent.field(mandatory=True)
    _entities: MapFromEntityToMapFromComponentStrToComponent[ComponentTemplate] = pyrsistent.field(
        initial=pyrsistent.pmap
    )
    _components: MapFromComponentToSetOfEntities = pyrsistent.field(initial=pyrsistent.pmap)


class QueryFunction(typing.Protocol):
    def __call__(self, ecs: EntityComponentSystem[ComponentTemplate], entity: Entity) -> bool:
        ...


def create_ecs() -> EntityComponentSystem[ComponentTemplate]:
    return EntityComponentSystem(_last_unique_id=0)


def add_entity(
    *,
    ecs: EntityComponentSystem[ComponentTemplate],
    components: typing.Optional[IterableOfComponents[ComponentTemplate]] = None,
) -> typing.Tuple[EntityComponentSystem[ComponentTemplate], Entity]:
    unique_id = ecs._last_unique_id  # pylint: disable=protected-access
    new_unique_id = unique_id + 1

    entity = Entity(unique_id=unique_id)
    new_entities = ecs._entities.set(entity, pyrsistent.pmap())  # pylint: disable=protected-access

    ecs = ecs.set(_last_unique_id=new_unique_id, _entities=new_entities)

    if components is not None:
        for component in components:
            ecs = add_component(ecs=ecs, entity=entity, component=component)

    return ecs, entity


def add_component(
    *, ecs: EntityComponentSystem[ComponentTemplate], entity: Entity, component: ComponentTemplate
) -> EntityComponentSystem[ComponentTemplate]:
    component_type_str = type_to_str(type(component))

    entities = ecs._entities  # pylint: disable=protected-access
    entity_components = entities.get(entity, pyrsistent.pmap())
    new_entity_components = entity_components.set(component_type_str, component)
    new_entities = entities.set(entity, new_entity_components)

    components = ecs._components  # pylint: disable=protected-access
    component_entities = components.get(component_type_str, pyrsistent.pset())
    new_component_entities = component_entities.add(entity)
    new_components = components.set(component_type_str, new_component_entities)

    return ecs.set(_entities=new_entities, _components=new_components)


def does_entity_have_component(
    *, ecs: EntityComponentSystem[ComponentTemplate], entity: Entity, component_type: typing.Type[ComponentTemplate]
) -> bool:
    component_type_str = type_to_str(component_type)
    return component_type_str in ecs._entities[entity]  # pylint: disable=protected-access


def get_component_of_entity(
    *, ecs: EntityComponentSystem[ComponentTemplate], entity: Entity, component_type: typing.Type[ComponentTemplate]
) -> typing.Optional[ComponentTemplate]:

    if not does_entity_have_component(ecs=ecs, entity=entity, component_type=component_type):
        return None

    component_type_str = type_to_str(component_type)
    component = ecs._entities[entity][component_type_str]  # pylint: disable=protected-access
    return component


def get_components_of_entity(
    *, ecs: EntityComponentSystem[ComponentTemplate], entity: Entity
) -> MapFromComponentStrToComponent[ComponentTemplate]:
    return ecs._entities[entity]  # pylint: disable=protected-access


def get_entities(*, ecs: EntityComponentSystem[ComponentTemplate]) -> typing.Generator[Entity, None, None]:
    yield from ecs._entities  # pylint: disable=protected-access


def get_entities_with_component(
    *, ecs: EntityComponentSystem[ComponentTemplate], component_type: typing.Type[ComponentTemplate]
) -> typing.Generator[Entity, None, None]:
    component_type_str = type_to_str(component_type)
    yield from ecs._components[component_type_str]  # pylint: disable=protected-access


def query_entities(
    *, ecs: EntityComponentSystem[ComponentTemplate], query_function: QueryFunction
) -> typing.Generator[Entity, None, None]:
    for entity in ecs._entities:  # pylint: disable=protected-access
        if query_function(ecs=ecs, entity=entity):
            yield entity


# Systems
SystemPriority = int
SystemTemplate = typing.TypeVar("SystemTemplate")
SetOfSystems = pyrsistent.typing.PSet[SystemTemplate]
MapFromPriorityToSetOfSystems = pyrsistent.typing.PMap[SystemPriority, SetOfSystems[SystemTemplate]]


class Systems(typing.Generic[SystemTemplate], pyrsistent.PClass):
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


def get_systems(*, systems: Systems[SystemTemplate]) -> typing.Generator[SystemTemplate, None, None]:
    for _, systems_with_given_priority in systems._priority_to_systems.items():  # pylint: disable=protected-access
        for system in systems_with_given_priority:
            yield system


# Systems End
