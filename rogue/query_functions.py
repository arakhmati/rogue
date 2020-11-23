"""
Rogue-specific query functions
"""

from rogue.ecs import Entity, EntityComponentDatabase, ComponentTemplate
from rogue.ecs import get_components_of_entity


def is_of_type(ecdb: EntityComponentDatabase[ComponentTemplate], entity: Entity, entity_type: str) -> bool:

    entity_components = get_components_of_entity(ecdb=ecdb, entity=entity)

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


def is_hero(ecdb: EntityComponentDatabase[ComponentTemplate], entity: Entity) -> bool:
    return is_of_type(ecdb=ecdb, entity=entity, entity_type="hero")


def is_enemy(ecdb: EntityComponentDatabase[ComponentTemplate], entity: Entity) -> bool:
    return is_of_type(ecdb=ecdb, entity=entity, entity_type="enemy")
