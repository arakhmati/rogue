"""
Rogue-specific query functions
"""

from typing import Iterable

from rogue.generic.ecs import ComponentTemplate
from rogue.generic.functions import type_of_value_to_str

ENTITY_TYPE_TO_COMPONENTS = {
    "hero": {"AppearanceComponent", "PositionComponent", "VelocityComponent", "MoneyComponent", "HealthComponent"},
    "enemy": {"AppearanceComponent", "PositionComponent", "VelocityComponent", "HealthComponent"},
}


def is_of_type(components: Iterable[ComponentTemplate], entity_type: str) -> bool:
    component_types_as_str = {type_of_value_to_str(component) for component in components}
    expected_component_types_as_str = ENTITY_TYPE_TO_COMPONENTS.get(entity_type, set())
    return component_types_as_str == expected_component_types_as_str


def is_hero(components: Iterable[ComponentTemplate]) -> bool:
    return is_of_type(components=components, entity_type="hero")


def is_enemy(components: Iterable[ComponentTemplate]) -> bool:
    return is_of_type(components=components, entity_type="enemy")
