import pathlib

import pygame
from toolz import first

from rogue.io.loaders import load_rogue_ecdb_from_input_yaml
from rogue.generic.ecs import (
    add_system,
    add_component,
    query_entities,
    create_systems,
)
from rogue.systems import (
    Systems,
    SystemUnion,
    process_systems,
    create_pygcurse_render_system,
    create_movement_system,
    create_enemy_ai_system,
)
from rogue.components import create_velocity_component

from rogue.query_functions import is_hero


def rogue_pygcurse(*, input_file_name: pathlib.Path, window_height: int, window_width: int) -> None:

    ecdb = load_rogue_ecdb_from_input_yaml(input_file_name=input_file_name)

    systems: Systems[SystemUnion] = create_systems()
    systems = add_system(systems=systems, priority=0, system=create_enemy_ai_system())
    systems = add_system(systems=systems, priority=1, system=create_movement_system())
    systems = add_system(
        systems=systems, priority=2, system=create_pygcurse_render_system(height=window_height, width=window_width)
    )

    hero = first(query_entities(ecdb=ecdb, query_function=is_hero))

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
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
                    return
                else:
                    continue

                ecdb = add_component(
                    ecdb=ecdb,
                    entity=hero,
                    component=create_velocity_component(y_axis=hero_velocity_y, x_axis=hero_velocity_x),
                )
                ecdb = process_systems(ecdb=ecdb, systems=systems)
