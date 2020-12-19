from typing import Tuple

import pathlib

from rogue.io.loaders import load_rogue_ecdb_from_input_yaml
from rogue.generic.ecs import Systems, create_systems, add_system, process_systems
from rogue.systems import (
    SystemUnion,
    process_system,
    process_action,
    PygcurseRenderSystem,
    MovementSystem,
    EnemyAISystem,
    PynputHeroControlSystem,
    CollisionDetectionSystem,
)
from rogue.exceptions import QuitGameException, IgnoreTimeStepException


def create_rogue_systems(*, window_height: int, window_width: int) -> Tuple[Systems[SystemUnion], PygcurseRenderSystem]:

    systems: Systems[SystemUnion] = create_systems()
    systems = add_system(systems=systems, priority=0, system=PynputHeroControlSystem.create())
    systems = add_system(systems=systems, priority=0, system=EnemyAISystem.create())
    systems = add_system(systems=systems, priority=1, system=CollisionDetectionSystem.create())
    systems = add_system(systems=systems, priority=2, system=MovementSystem.create())
    render_system = PygcurseRenderSystem.create_from_height_and_width(height=window_height, width=window_width)
    systems = add_system(systems=systems, priority=3, system=render_system,)
    return systems, render_system


def rogue_pygcurse(*, input_file_name: pathlib.Path, window_height: int, window_width: int) -> None:

    ecdb = load_rogue_ecdb_from_input_yaml(input_file_name=input_file_name)
    systems, render_system = create_rogue_systems(window_height=window_height, window_width=window_width)

    # Render the initial state
    render_system(ecdb=ecdb)

    while True:
        try:
            ecdb = process_systems(
                ecdb=ecdb, systems=systems, process_system=process_system, process_action=process_action
            )
        except QuitGameException:
            return
        except IgnoreTimeStepException:
            continue
