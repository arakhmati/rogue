"""
Rogue-specific filter functions
"""

from typing import cast, Union


import pyrsistent
from pyrsistent.typing import PSet

from rogue.generic.ecs import ComponentTemplate, MapFromComponentTypeToComponent
from rogue.components import TypeComponent
from rogue.types import TypeEnum, ENEMY_TYPES


def _is_of_type(
    components: MapFromComponentTypeToComponent[ComponentTemplate],
    queried_entity_type: Union[TypeEnum, PSet[TypeEnum]],
) -> bool:

    if not isinstance(queried_entity_type, pyrsistent.PSet):
        queried_entity_type = pyrsistent.s(queried_entity_type)

    entity_type_component = components[TypeComponent]

    actual_entity_type = cast(TypeComponent, entity_type_component).entity_type

    return actual_entity_type in queried_entity_type


def is_hero(components: MapFromComponentTypeToComponent[ComponentTemplate]) -> bool:
    return _is_of_type(components=components, queried_entity_type=TypeEnum.Hero)


def is_enemy(components: MapFromComponentTypeToComponent[ComponentTemplate]) -> bool:
    return _is_of_type(components=components, queried_entity_type=ENEMY_TYPES)
