"""
Rogue-specific filter functions
"""

from typing import cast

from rogue.generic.ecs import ComponentTemplate, MapFromComponentTypeToOptionalComponent
from rogue.components import TypeComponent, ComponentUnion


def _is_of_type(components: MapFromComponentTypeToOptionalComponent[ComponentTemplate], entity_type: str) -> bool:

    rogue_components = cast(MapFromComponentTypeToOptionalComponent[ComponentUnion], components)
    entity_type_component = rogue_components[TypeComponent]

    actual_entity_type = cast(TypeComponent, entity_type_component).entity_type

    if entity_type == actual_entity_type:
        return True
    if entity_type == "enemy" and actual_entity_type in {"hobgoblin"}:
        return True
    return False


def is_hero(components: MapFromComponentTypeToOptionalComponent[ComponentTemplate]) -> bool:
    return _is_of_type(components=components, entity_type="hero")


def is_enemy(components: MapFromComponentTypeToOptionalComponent[ComponentTemplate]) -> bool:
    return _is_of_type(components=components, entity_type="enemy")
