import random
from typing import Generator

import attr

from rogue.filter_functions import is_enemy
from rogue.generic.ecs import (
    EntityComponentDatabase,
    query_entities,
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


@attr.s(frozen=True, kw_only=True)
class EnemyAISystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "EnemyAISystem":
        return cls()

    RANDOM_VALUE_TO_YX = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0),
    }

    def __call__(self, *, ecdb: EntityComponentDatabase[ComponentUnion]) -> Generator[ActionUnion, None, None]:
        for entity, _ in query_entities(ecdb=ecdb, filter_function=is_enemy):
            random_value = random.randint(0, len(EnemyAISystem.RANDOM_VALUE_TO_YX) - 1)
            y_axis, x_axis = EnemyAISystem.RANDOM_VALUE_TO_YX[random_value]

            velocity_component = VelocityComponent.create_from_attributes(y_axis=y_axis, x_axis=x_axis)
            yield AddComponentAction(entity=entity, component=velocity_component)
