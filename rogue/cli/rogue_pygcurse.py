import pathlib

from rogue.io.loaders import load_rogue_ecdb_from_input_yaml
from rogue.generic.ecs import create_systems, add_system
from rogue.systems import (
    Systems,
    SystemUnion,
    process_systems,
    PygcurseRenderSystem,
    MovementSystem,
    EnemyAISystem,
    PygameHeroControlSystem,
    CollisionDetectionSystem,
)
from rogue.exceptions import QuitGameException, IgnoreTimeStepException


def create_rogue_systems(*, window_height: int, window_width: int) -> Systems[SystemUnion]:

    systems: Systems[SystemUnion] = create_systems()
    systems = add_system(systems=systems, priority=0, system=PygameHeroControlSystem.create())
    systems = add_system(systems=systems, priority=0, system=EnemyAISystem.create())
    systems = add_system(systems=systems, priority=1, system=CollisionDetectionSystem.create())
    systems = add_system(systems=systems, priority=2, system=MovementSystem.create())
    systems = add_system(
        systems=systems,
        priority=3,
        system=PygcurseRenderSystem.create_from_height_and_width(height=window_height, width=window_width),
    )
    return systems


def rogue_pygcurse(*, input_file_name: pathlib.Path, window_height: int, window_width: int) -> None:

    ecdb = load_rogue_ecdb_from_input_yaml(input_file_name=input_file_name)
    systems = create_rogue_systems(window_height=window_height, window_width=window_width)

    while True:
        try:
            ecdb = process_systems(ecdb=ecdb, systems=systems)
        except QuitGameException:
            return
        except IgnoreTimeStepException:
            continue
