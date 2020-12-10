from typing import (
    Tuple,
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
)
from rogue.components import (
    ComponentUnion,
    VelocityComponent,
)
from rogue.systems.common.actions import (
    ActionUnion,
    AddComponentAction,
)
from rogue.systems.common.traits import YieldChangesSystemTrait
from rogue.exceptions import QuitGameException, IgnoreTimeStepException


@attr.s(frozen=True, kw_only=True)
class PygameHeroControlSystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "PygameHeroControlSystem":
        return cls()

    def __call__(
        self, *, ecdb: EntityComponentDatabase[ComponentUnion]
    ) -> Generator[Tuple[Entity, ActionUnion], None, None]:

        # Query the hero once
        hero = first(first(query_entities(ecdb=ecdb, filter_function=is_hero)))

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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise QuitGameException
            else:
                raise IgnoreTimeStepException

            velocity_component = VelocityComponent.create_from_attributes(
                y_axis=hero_velocity_y, x_axis=hero_velocity_x
            )
            yield hero, AddComponentAction(component=velocity_component)
            return

        raise IgnoreTimeStepException
