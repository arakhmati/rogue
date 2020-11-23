import random
import typing

import attr
import pygcurse

from rogue.generic import evolve
from rogue.query_functions import is_enemy
from rogue.ecs import (
    EntityComponentDatabase,
    Systems,
    add_component,
    get_component_of_entity,
    get_entities,
    get_entities_with_component,
    query_entities,
    get_systems,
)
from rogue.components import (
    RogueComponentUnion,
    PositionComponent,
    VelocityComponent,
    AppearanceComponent,
    SizeComponent,
)
from rogue.components import create_velocity_component


# Systems
@attr.s(frozen=True, kw_only=True)
class PygcurseRenderSystem:
    window: pygcurse.PygcurseWindow = attr.ib()


@attr.s(frozen=True, kw_only=True)
class MovementSystem:
    ...


@attr.s(frozen=True, kw_only=True)
class EnemyAISystem:
    ...


SystemUnion = typing.Union[PygcurseRenderSystem, MovementSystem, EnemyAISystem]
# Systems End


def create_pygcurse_render_system(*, height: int, width: int) -> PygcurseRenderSystem:
    window = pygcurse.PygcurseWindow(width=width, height=height)
    return PygcurseRenderSystem(window=window)


def create_movement_system() -> MovementSystem:
    return MovementSystem()


def create_enemy_ai_system() -> EnemyAISystem:
    return EnemyAISystem()


def process_pygcurse_render_system(
    *, system: PygcurseRenderSystem, ecdb: EntityComponentDatabase[RogueComponentUnion]
) -> None:
    for entity in get_entities(ecdb=ecdb):
        position_component = typing.cast(
            typing.Optional[PositionComponent],
            get_component_of_entity(ecdb=ecdb, entity=entity, component_type=PositionComponent),
        )
        assert position_component is not None

        size_component = typing.cast(
            typing.Optional[SizeComponent],
            get_component_of_entity(ecdb=ecdb, entity=entity, component_type=SizeComponent),
        )
        if size_component is not None:

            height, width = size_component.height, size_component.width

            # Left Wall
            start_pos = position_component.x_axis, position_component.y_axis + 1
            end_pos = position_component.x_axis, position_component.y_axis + height - 1
            system.window.drawline(char="|", start_pos=start_pos, end_pos=end_pos, fgcolor="grey")

            # Right Wall
            start_pos = position_component.x_axis + width, position_component.y_axis + 1
            end_pos = position_component.x_axis + width, position_component.y_axis + height - 1
            system.window.drawline(char="|", start_pos=start_pos, end_pos=end_pos, fgcolor="grey")

            # Top Wall
            start_pos = position_component.x_axis, position_component.y_axis
            end_pos = position_component.x_axis + width, position_component.y_axis
            system.window.drawline(char="_", start_pos=start_pos, end_pos=end_pos, fgcolor="grey")

            # Bottom Wall
            start_pos = position_component.x_axis, position_component.y_axis + height
            end_pos = position_component.x_axis + width, position_component.y_axis + height
            system.window.drawline(char="_", start_pos=start_pos, end_pos=end_pos, fgcolor="grey")

            # Inside of the Room
            y_axis = position_component.y_axis + 1
            x_axis = position_component.x_axis + 1
            system.window.fill(char=".", region=(x_axis, y_axis, width - 1, height - 1), fgcolor="grey")

    for entity in get_entities(ecdb=ecdb):

        position_component = typing.cast(
            typing.Optional[PositionComponent],
            get_component_of_entity(ecdb=ecdb, entity=entity, component_type=PositionComponent),
        )
        assert position_component is not None

        appearance_component = typing.cast(
            typing.Optional[AppearanceComponent],
            get_component_of_entity(ecdb=ecdb, entity=entity, component_type=AppearanceComponent),
        )
        if appearance_component is not None:
            system.window.putchar(
                appearance_component.symbol,
                x=position_component.x_axis,
                y=position_component.y_axis,
                fgcolor=appearance_component.color,
            )


def process_movement_system(
    *, system: MovementSystem, ecdb: EntityComponentDatabase[RogueComponentUnion]
) -> EntityComponentDatabase[RogueComponentUnion]:
    assert system  # Hack to make 'system' variable marked as used

    for entity in get_entities_with_component(ecdb=ecdb, component_type=VelocityComponent):

        position_component = typing.cast(
            typing.Optional[PositionComponent],
            get_component_of_entity(ecdb=ecdb, entity=entity, component_type=PositionComponent),
        )
        assert position_component is not None

        velocity_component = typing.cast(
            typing.Optional[VelocityComponent],
            get_component_of_entity(ecdb=ecdb, entity=entity, component_type=VelocityComponent),
        )
        assert velocity_component is not None

        y_axis = position_component.y_axis + velocity_component.y_axis
        x_axis = position_component.x_axis + velocity_component.x_axis

        new_position_component = evolve(position_component, y_axis=y_axis, x_axis=x_axis)
        ecdb = add_component(ecdb=ecdb, entity=entity, component=new_position_component)

    return ecdb


RANDOM_VALUE_TO_YX = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}


def process_enemy_ai_system(
    *, system: EnemyAISystem, ecdb: EntityComponentDatabase[RogueComponentUnion]
) -> EntityComponentDatabase[RogueComponentUnion]:
    assert system  # Hack to make 'system' variable marked as used

    for entity in query_entities(ecdb=ecdb, query_function=is_enemy):
        random_value = random.randint(0, len(RANDOM_VALUE_TO_YX) - 1)
        y_axis, x_axis = RANDOM_VALUE_TO_YX[random_value]

        velocity_component = create_velocity_component(y_axis=y_axis, x_axis=x_axis)
        ecdb = add_component(ecdb=ecdb, entity=entity, component=velocity_component)

    return ecdb


def process_system(
    *, system: SystemUnion, ecdb: EntityComponentDatabase[RogueComponentUnion]
) -> EntityComponentDatabase[RogueComponentUnion]:
    if isinstance(system, PygcurseRenderSystem):
        process_pygcurse_render_system(system=system, ecdb=ecdb)
    elif isinstance(system, MovementSystem):
        ecdb = process_movement_system(system=system, ecdb=ecdb)
    elif isinstance(system, EnemyAISystem):
        ecdb = process_enemy_ai_system(system=system, ecdb=ecdb)
    else:
        raise ValueError(f"Unsupported System {type(system)}!")
    return ecdb


def process_systems(
    *, ecdb: EntityComponentDatabase[RogueComponentUnion], systems: Systems[SystemUnion]
) -> EntityComponentDatabase[RogueComponentUnion]:
    for system in get_systems(systems=systems):
        ecdb = process_system(system=system, ecdb=ecdb)
    return ecdb
