from typing import (
    cast,
    Generator,
)

import attr
import pygame
from toolz import first

from rogue.filter_functions import is_hero
from rogue.generic.ecs import (
    EntityComponentDatabase,
    query_entities,
    Entity,
    get_component,
)
from rogue.generic.functions import evolve
from rogue.components import (
    ComponentUnion,
    VelocityComponent,
    InventoryComponent,
    EquipmentComponent,
    TypeComponent,
)
from rogue.systems.common.actions import (
    ActionUnion,
    AddComponentAction,
)
from rogue.systems.common.traits import YieldChangesSystemTrait
from rogue.exceptions import QuitGameException, IgnoreTimeStepException
from rogue.types import WEAPON_TYPES


def _get_hero_entity(*, ecdb: EntityComponentDatabase[ComponentUnion]) -> Entity:
    hero_entity: Entity
    hero_entity, _ = first(query_entities(ecdb=ecdb, filter_function=is_hero))
    return hero_entity


def _equip_up_next_weapon(
    *, ecdb: EntityComponentDatabase[ComponentUnion], entity: Entity
) -> Generator[ActionUnion, None, None]:
    inventory_component = cast(
        InventoryComponent, get_component(ecdb=ecdb, entity=entity, component_type=InventoryComponent),
    )
    equipment_component = cast(
        EquipmentComponent, get_component(ecdb=ecdb, entity=entity, component_type=EquipmentComponent),
    )

    item_entity: Entity
    for item_entity in inventory_component.entities:
        if (
            cast(TypeComponent, get_component(ecdb=ecdb, entity=item_entity, component_type=TypeComponent)).entity_type
            in WEAPON_TYPES
        ):
            break
    else:
        return

    if len(equipment_component.entities) > 0:
        assert len(equipment_component.entities) == 1
        current_item_entity = first(equipment_component.entities)
        inventory_component = evolve(
            inventory_component, entities=inventory_component.entities.add(current_item_entity)
        )
        equipment_component = evolve(
            equipment_component, entities=equipment_component.entities.remove(current_item_entity)
        )

    inventory_component = evolve(inventory_component, entities=inventory_component.entities.remove(item_entity))
    equipment_component = evolve(equipment_component, entities=equipment_component.entities.add(item_entity))

    yield AddComponentAction(entity=entity, component=inventory_component)
    yield AddComponentAction(entity=entity, component=equipment_component)


@attr.s(frozen=True, kw_only=True)
class PygameHeroControlSystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "PygameHeroControlSystem":
        return cls()

    def __call__(self, *, ecdb: EntityComponentDatabase[ComponentUnion]) -> Generator[ActionUnion, None, None]:

        hero_entity = _get_hero_entity(ecdb=ecdb)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise QuitGameException

            if event.type != pygame.KEYDOWN:
                raise IgnoreTimeStepException

            hero_velocity_y, hero_velocity_x = 0, 0

            if event.key == pygame.K_LEFT:
                hero_velocity_x = -1
            elif event.key == pygame.K_RIGHT:
                hero_velocity_x = 1
            elif event.key == pygame.K_UP:
                hero_velocity_y = -1
            elif event.key == pygame.K_DOWN:
                hero_velocity_y = 1
            elif event.key == pygame.K_e:
                yield from _equip_up_next_weapon(ecdb=ecdb, entity=hero_entity)
                return
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise QuitGameException
            else:
                raise IgnoreTimeStepException

            if hero_velocity_y != 0 or hero_velocity_x != 0:
                velocity_component = VelocityComponent.create_from_attributes(
                    y_axis=hero_velocity_y, x_axis=hero_velocity_x
                )
                yield AddComponentAction(entity=hero_entity, component=velocity_component)
                return

        raise IgnoreTimeStepException
