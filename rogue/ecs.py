"""
Generic Entity-Component-System code

In this file, access to private members of EntityComponentSystem[Component] class is allowed.
"""

import typing

import pyrsistent

from rogue.types import (
    EntityComponentSystem,
    Entity,
    # Components
    ComponentTemplate,
    MapFromComponentStrToComponent,
    IterableOfComponents,
    # Systems
    Priority,
    System,
    # Other
    QueryFunction,
)
from rogue.generic import type_to_str


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


def add_system(
    *, ecs: EntityComponentSystem[ComponentTemplate], system: System, priority: Priority
) -> EntityComponentSystem[ComponentTemplate]:
    assert priority >= 0, "Priority must be a positive number!"

    systems = ecs._systems  # pylint: disable=protected-access
    systems_with_given_priority = systems.get(priority, pyrsistent.pset())
    new_systems_with_given_priority = systems_with_given_priority.add(system)
    new_systems = systems.set(priority, new_systems_with_given_priority)
    return ecs.set(_systems=new_systems)


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


def get_systems(*, ecs: EntityComponentSystem[ComponentTemplate]) -> typing.Generator[System, None, None]:
    for _, systems in ecs._systems.items():  # pylint: disable=protected-access
        for system in systems:
            yield system
