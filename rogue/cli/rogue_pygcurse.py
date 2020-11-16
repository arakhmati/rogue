import pathlib

import pygame
from toolz import first

from rogue.serialization.loaders import load_rogue_entities_and_components_from_input_yaml
from rogue.ecs import (
    add_system,
    add_component,
    query_entities,
)
from rogue.systems import process_ecs, create_pygcurse_render_system, create_movement_system, create_enemy_ai_system
from rogue.components import create_velocity_component

from rogue.query_functions import is_hero


def rogue_pygcurse(*, input_file_name: pathlib.Path, window_height: int, window_width: int) -> None:

    ecs = load_rogue_entities_and_components_from_input_yaml(input_file_name=input_file_name)
    ecs = add_system(ecs=ecs, priority=0, system=create_enemy_ai_system())
    ecs = add_system(ecs=ecs, priority=1, system=create_movement_system())
    ecs = add_system(
        ecs=ecs, priority=2, system=create_pygcurse_render_system(height=window_height, width=window_width)
    )

    hero = first(query_entities(ecs=ecs, query_function=is_hero))

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

                ecs = add_component(
                    ecs=ecs,
                    entity=hero,
                    component=create_velocity_component(y_axis=hero_velocity_y, x_axis=hero_velocity_x),
                )
                ecs = process_ecs(ecs=ecs)
