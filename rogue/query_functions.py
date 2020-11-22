"""
Rogue-specific query functions
"""

from rogue.types import Entity, EntityComponentSystem
from rogue.ecs import get_components_of_entity


def is_of_type(ecs: EntityComponentSystem, entity: Entity, entity_type: str) -> bool:

    entity_components = get_components_of_entity(ecs=ecs, entity=entity)

    if entity_type == "hero":
        return set(entity_components.keys()) == {
            "AppearanceComponent",
            "PositionComponent",
            "VelocityComponent",
            "MoneyComponent",
            "HealthComponent",
        }
    if entity_type == "enemy":
        return set(entity_components.keys()) == {
            "AppearanceComponent",
            "PositionComponent",
            "VelocityComponent",
            "HealthComponent",
        }
    return False


def is_hero(ecs: EntityComponentSystem, entity: Entity) -> bool:
    return is_of_type(ecs=ecs, entity=entity, entity_type="hero")


def is_enemy(ecs: EntityComponentSystem, entity: Entity) -> bool:
    return is_of_type(ecs=ecs, entity=entity, entity_type="enemy")
