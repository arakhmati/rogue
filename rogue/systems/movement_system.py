from typing import (
    cast,
    Optional,
    Generator,
    List,
    Type,
)

import attr

from rogue.generic.functions import evolve
from rogue.generic.ecs import (
    EntityComponentDatabase,
    query_entities,
)
from rogue.components import (
    ComponentUnion,
    PositionComponent,
    VelocityComponent,
)
from rogue.systems.common.traits import YieldChangesSystemTrait
from rogue.systems.common.actions import (
    ActionUnion,
    AddComponentAction,
)
from rogue.systems.common.constants import ZERO_VELOCITY_COMPONENT


@attr.s(frozen=True, kw_only=True)
class MovementSystem(YieldChangesSystemTrait):
    @classmethod
    def create(cls) -> "MovementSystem":
        return cls()

    def __call__(self, *, ecdb: EntityComponentDatabase[ComponentUnion]) -> Generator[ActionUnion, None, None]:

        component_types: List[Type[ComponentUnion]] = [PositionComponent, VelocityComponent]
        for entity, components in query_entities(ecdb=ecdb, component_types=component_types):
            position_component = cast(Optional[PositionComponent], components[PositionComponent])
            velocity_component = cast(Optional[VelocityComponent], components[VelocityComponent])

            if position_component is None:
                continue

            if velocity_component is None:
                continue

            y_axis = position_component.y_axis + velocity_component.y_axis
            x_axis = position_component.x_axis + velocity_component.x_axis

            new_position_component: PositionComponent = evolve(position_component, y_axis=y_axis, x_axis=x_axis)
            yield AddComponentAction(entity=entity, component=new_position_component)
            yield AddComponentAction(entity=entity, component=ZERO_VELOCITY_COMPONENT)
