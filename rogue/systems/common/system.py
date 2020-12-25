from typing import Union, Generator

from rogue.generic.ecs import (
    EntityComponentDatabase,
    remove_entity,
    add_component,
    remove_component,
)
from rogue.components import ComponentUnion
from rogue.systems.common.actions import (
    ActionUnion,
    RemoveEntityAction,
    AddComponentAction,
    RemoveComponentAction,
)

from rogue.systems.collision_detection_system import CollisionDetectionSystem
from rogue.systems.enemy_ai_system import EnemyAISystem
from rogue.systems.movement_system import MovementSystem
from rogue.systems.pygame_hero_control_system import PygameHeroControlSystem
from rogue.systems.pygcurse_render_system import PygcurseRenderSystem
from rogue.systems.pynput_hero_control_system import PynputHeroControlSystem
from rogue.systems.panda3d_render_system import Panda3dRenderSystem
from rogue.systems.common.traits import NoReturnSystemTrait, YieldChangesSystemTrait

SystemUnion = Union[
    PygcurseRenderSystem,
    MovementSystem,
    EnemyAISystem,
    PygameHeroControlSystem,
    CollisionDetectionSystem,
    PynputHeroControlSystem,
    Panda3dRenderSystem,
]


def process_action(
    ecdb: EntityComponentDatabase[ComponentUnion], action: ActionUnion
) -> EntityComponentDatabase[ComponentUnion]:
    if isinstance(action, AddComponentAction):
        ecdb = add_component(ecdb=ecdb, entity=action.entity, component=action.component)
    elif isinstance(action, RemoveComponentAction):
        ecdb = remove_component(ecdb=ecdb, entity=action.entity, component_type=action.component_type)
    elif isinstance(action, RemoveEntityAction):
        ecdb = remove_entity(ecdb=ecdb, entity=action.entity)
    else:
        raise ValueError(f"Unrecognized Action: {action}")
    return ecdb


def process_system(
    *, ecdb: EntityComponentDatabase[ComponentUnion], system: SystemUnion,
) -> Generator[ActionUnion, None, None]:
    if isinstance(system, NoReturnSystemTrait):
        system(ecdb=ecdb)
    elif isinstance(system, YieldChangesSystemTrait):
        yield from system(ecdb=ecdb)
    else:
        raise ValueError(f"System of type {type(system)} does not support any of the system traits!")
