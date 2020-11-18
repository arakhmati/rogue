import pathlib
import pprint

import typing

from loguru import logger
import yaml

from rogue.types import EntityComponentSystem
from rogue.components import (
    create_type_component,
    create_position_component,
    create_size_component,
    create_apperance_component,
)
from rogue.ecs import create_ecs, add_entity

RoomConfig = typing.Dict[typing.Any, typing.Any]


def _load_room_config(*, input_file_name: pathlib.Path) -> RoomConfig:
    with open(input_file_name) as input_file:
        room_config: RoomConfig = yaml.safe_load(input_file)
    return room_config


def _parse_coordinates(coordinates: str, y_axis: int = 0, x_axis: int = 0) -> typing.Dict[str, int]:
    parsed_y, parsed_x = (int(number) for number in coordinates.split(","))
    parsed_y += y_axis
    parsed_x += x_axis
    return {"y_axis": parsed_y, "x_axis": parsed_x}


def _parse_size(size: str) -> typing.Dict[str, int]:
    height, width = (int(number) for number in size.split(","))
    return {"height": height, "width": width}


def _type_to_appearance(item_type: str) -> typing.Dict[str, str]:
    item_type_to_appearance = {
        "hero": ("#", "purple"),
        "sword": ("(", "green"),
        "hobgoblin": ("H", "red"),
        "potion": ("!", "blue"),
        "gold": ("*", "gold"),
        "door": ("+", "grey"),
    }

    symbol, color = item_type_to_appearance[item_type]

    return {
        "symbol": symbol,
        "color": color,
    }


def load_rogue_entities_and_components_from_input_yaml(input_file_name: pathlib.Path) -> EntityComponentSystem:

    logger.info(f"Input file: {input_file_name}")

    room_config = _load_room_config(input_file_name=input_file_name)
    logger.info(f"Room Config: {pprint.pformat(room_config)}")

    ecs = create_ecs()
    for room in room_config:
        room_coordinates = _parse_coordinates(room["coordinates"])
        ecs, _ = add_entity(
            ecs=ecs,
            components=[
                create_position_component(**room_coordinates),
                create_size_component(**_parse_size(room["size"])),
                create_type_component(entity_type="room"),
            ],
        )
        for item in room["items"]:
            ecs, _ = add_entity(
                ecs=ecs,
                components=[
                    create_position_component(**_parse_coordinates(item["coordinates"], **room_coordinates)),
                    create_apperance_component(**_type_to_appearance(item["type"])),
                    create_type_component(entity_type=item["type"]),
                ],
            )

    return ecs
