import pathlib
import pprint

import typing

from loguru import logger
import yaml

from rogue.ecs import EntityComponentDatabase, create_ecdb, add_entity
from rogue.components import (
    RogueComponentUnion,
    create_position_component,
    create_size_component,
    create_apperance_component,
    create_velocity_component,
    create_money_component,
    create_health_component,
)

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


def load_rogue_ecdb_from_input_yaml(input_file_name: pathlib.Path,) -> EntityComponentDatabase[RogueComponentUnion]:

    logger.info(f"Input file: {input_file_name}")

    room_config = _load_room_config(input_file_name=input_file_name)
    logger.info(f"Room Config: {pprint.pformat(room_config)}")

    ecdb: EntityComponentDatabase[RogueComponentUnion] = create_ecdb()
    for room in room_config:
        room_coordinates = _parse_coordinates(room["coordinates"])
        room_components: typing.List[RogueComponentUnion] = [
            create_position_component(**room_coordinates),
            create_size_component(**_parse_size(room["size"])),
        ]
        ecdb, _ = add_entity(ecdb=ecdb, components=room_components)
        for item in room["items"]:
            components: typing.List[RogueComponentUnion] = [
                create_position_component(**_parse_coordinates(item["coordinates"], **room_coordinates)),
                create_apperance_component(**_type_to_appearance(item["type"])),
            ]
            if item["type"] == "hero":
                components.append(create_velocity_component(y_axis=0, x_axis=0))
                components.append(create_health_component(amount=100))
                components.append(create_money_component(amount=0))
            elif item["type"] in {"hobgoblin"}:
                components.append(create_velocity_component(y_axis=0, x_axis=0))
                components.append(create_health_component(amount=100))

            ecdb, _ = add_entity(ecdb=ecdb, components=components)

    return ecdb
