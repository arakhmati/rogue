from typing import (
    Generator,
    Deque,
)
from collections import deque

import attr
import pygame

from rogue.generic.ecs import EntityComponentDatabase
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
from rogue.systems.control_systems.functions import get_hero_entity, maybe_equip_next_weapon, maybe_drink_potion


@attr.s(frozen=True, kw_only=True, hash=False, cmp=False)
class PygameHeroControlSystem(YieldChangesSystemTrait):
    events: Deque[pygame.event.Event] = attr.ib(default=deque())

    @classmethod
    def create(cls) -> "PygameHeroControlSystem":
        return cls()

    def __hash__(self) -> int:
        return 0

    def __call__(self, *, ecdb: EntityComponentDatabase[ComponentUnion]) -> Generator[ActionUnion, None, None]:

        hero_entity = get_hero_entity(ecdb=ecdb)

        self.events.extend(pygame.event.get())
        while len(self.events) > 0:
            event = self.events.popleft()

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
                yield from maybe_equip_next_weapon(ecdb=ecdb, entity=hero_entity)
                return
            elif event.key == pygame.K_p:
                yield from maybe_drink_potion(ecdb=ecdb, entity=hero_entity)
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
