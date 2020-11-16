"""
Rogue-specific functions
"""

from collections.abc import Iterable
import typing

from rogue.constants import ENEMY_ENTITY_TYPES
from rogue.types import Entity, EntityComponentSystem, TypeComponent
from rogue.ecs import get_component_of_entity


def is_of_type(
    ecs: EntityComponentSystem, entity: Entity, entity_type: typing.Union[str, typing.Iterable[str]]
) -> bool:
    if not isinstance(entity_type, Iterable):
        entity_type = (entity_type,)

    type_component = typing.cast(
        TypeComponent, get_component_of_entity(ecs=ecs, entity=entity, component_type=TypeComponent)
    )
    return type_component.entity_type in entity_type


def is_hero(ecs: EntityComponentSystem, entity: Entity) -> bool:
    return is_of_type(ecs=ecs, entity=entity, entity_type="hero")


def is_enemy(ecs: EntityComponentSystem, entity: Entity) -> bool:
    return is_of_type(ecs=ecs, entity=entity, entity_type=ENEMY_ENTITY_TYPES)
