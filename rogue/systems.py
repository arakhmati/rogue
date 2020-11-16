import random

import pygcurse

from rogue.generic import evolve
from rogue.query_functions import is_enemy
from rogue.types import (
    EntityComponentSystem,
    # Components
    PositionComponent,
    VelocityComponent,
    AppearanceComponent,
    SizeComponent,
    # Systems
    System,
    PygcurseRenderSystem,
    MovementSystem,
    EnemyAISystem,
)
from rogue.ecs import (
    add_component,
    get_component_of_entity,
    get_entities,
    get_entities_with_component,
    query_entities,
    get_systems,
)
from rogue.components import create_velocity_component


def create_pygcurse_render_system(*, height: int, width: int) -> PygcurseRenderSystem:
    window = pygcurse.PygcurseWindow(width=width, height=height)
    return PygcurseRenderSystem(window=window)


def create_movement_system() -> MovementSystem:
    return MovementSystem()


def create_enemy_ai_system() -> EnemyAISystem:
    return EnemyAISystem()


def process_pygcurse_render_system(*, system: PygcurseRenderSystem, ecs: EntityComponentSystem) -> None:
    for entity in get_entities(ecs=ecs):
        position_component = get_component_of_entity(ecs=ecs, entity=entity, component_type=PositionComponent)
        assert position_component is not None

        size_component = get_component_of_entity(ecs=ecs, entity=entity, component_type=SizeComponent)
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

    for entity in get_entities(ecs=ecs):
        position_component = get_component_of_entity(ecs=ecs, entity=entity, component_type=PositionComponent)
        assert position_component is not None

        appearance_component = get_component_of_entity(ecs=ecs, entity=entity, component_type=AppearanceComponent)
        if appearance_component is not None:
            system.window.putchar(
                appearance_component.symbol,
                x=position_component.x_axis,
                y=position_component.y_axis,
                fgcolor=appearance_component.color,
            )


def process_movement_system(*, system: MovementSystem, ecs: EntityComponentSystem) -> EntityComponentSystem:
    assert system  # Hack to make 'system' variable marked as used

    for entity in get_entities_with_component(ecs=ecs, component_type=VelocityComponent):
        position_component = get_component_of_entity(ecs=ecs, entity=entity, component_type=PositionComponent)
        assert position_component is not None

        velocity_component = get_component_of_entity(ecs=ecs, entity=entity, component_type=VelocityComponent)
        assert velocity_component is not None

        y_axis = position_component.y_axis + velocity_component.y_axis
        x_axis = position_component.x_axis + velocity_component.x_axis

        new_position_component = evolve(position_component, y_axis=y_axis, x_axis=x_axis)
        ecs = add_component(ecs=ecs, entity=entity, component=new_position_component)

    return ecs


RANDOM_VALUE_TO_YX = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}


def process_enemy_ai_system(*, system: EnemyAISystem, ecs: EntityComponentSystem) -> EntityComponentSystem:
    assert system  # Hack to make 'system' variable marked as used

    for entity in query_entities(ecs=ecs, query_function=is_enemy):
        random_value = random.randint(0, len(RANDOM_VALUE_TO_YX) - 1)
        y_axis, x_axis = RANDOM_VALUE_TO_YX[random_value]

        velocity_component = create_velocity_component(y_axis=y_axis, x_axis=x_axis)
        ecs = add_component(ecs=ecs, entity=entity, component=velocity_component)

    return ecs


def process_system(*, system: System, ecs: EntityComponentSystem) -> EntityComponentSystem:
    if isinstance(system, PygcurseRenderSystem):
        process_pygcurse_render_system(system=system, ecs=ecs)
    elif isinstance(system, MovementSystem):
        ecs = process_movement_system(system=system, ecs=ecs)
    elif isinstance(system, EnemyAISystem):
        ecs = process_enemy_ai_system(system=system, ecs=ecs)
    else:
        raise ValueError(f"Unsupported System {type(system)}!")
    return ecs


def process_ecs(*, ecs: EntityComponentSystem) -> EntityComponentSystem:
    for system in get_systems(ecs=ecs):
        ecs = process_system(system=system, ecs=ecs)
    return ecs