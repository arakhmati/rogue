import pathlib
import pprint

from typing import (
    Any,
    Dict,
    List,
)

from loguru import logger
import yaml

from rogue.generic.ecs import EntityComponentDatabase, create_ecdb, add_entity
from rogue.components import (
    ComponentUnion,
    PositionComponent,
    SizeComponent,
    TypeComponent,
    VelocityComponent,
    MoneyComponent,
    HealthComponent,
    InventoryComponent,
    EquipmentComponent,
)

RoomConfig = Dict[Any, Any]


def _load_room_config(*, input_file_name: pathlib.Path) -> RoomConfig:
    with open(input_file_name) as input_file:
        room_config: RoomConfig = yaml.safe_load(input_file)
    return room_config


def _parse_coordinates(coordinates: str, y_axis: int = 0, x_axis: int = 0) -> Dict[str, int]:
    parsed_y, parsed_x = (int(number) for number in coordinates.split(","))
    parsed_y += y_axis
    parsed_x += x_axis
    return {"y_axis": parsed_y, "x_axis": parsed_x}


def _parse_size(size: str) -> Dict[str, int]:
    height, width = (int(number) for number in size.split(","))
    return {"height": height, "width": width}


def load_rogue_ecdb_from_input_yaml(input_file_name: pathlib.Path,) -> EntityComponentDatabase[ComponentUnion]:

    logger.info(f"Input file: {input_file_name}")

    room_config = _load_room_config(input_file_name=input_file_name)
    logger.info(f"Room Config: {pprint.pformat(room_config)}")

    ecdb: EntityComponentDatabase[ComponentUnion] = create_ecdb()
    for room in room_config:
        room_coordinates = _parse_coordinates(room["coordinates"])
        room_components: List[ComponentUnion] = [
            PositionComponent.create_from_attributes(**room_coordinates),
            SizeComponent.create_from_attributes(**_parse_size(room["size"])),
            TypeComponent.create_from_attributes(entity_type="room"),
        ]
        ecdb, _ = add_entity(ecdb=ecdb, components=room_components)
        for item in room["items"]:
            components: List[ComponentUnion] = [
                PositionComponent.create_from_attributes(**_parse_coordinates(item["coordinates"], **room_coordinates)),
                TypeComponent.create_from_attributes(entity_type=item["type"]),
            ]
            if item["type"] == "hero":
                components.append(VelocityComponent.create_from_attributes(y_axis=0, x_axis=0))
                components.append(HealthComponent.create_from_attributes(amount=100))
                components.append(MoneyComponent.create_from_attributes(amount=0))
                components.append(InventoryComponent.create_from_attributes(entities=[]))
                components.append(EquipmentComponent.create_from_attributes(entities=[]))
            elif item["type"] in {"hobgoblin"}:
                components.append(VelocityComponent.create_from_attributes(y_axis=0, x_axis=0))
                components.append(HealthComponent.create_from_attributes(amount=100))
                components.append(InventoryComponent.create_from_attributes(entities=[]))
                components.append(EquipmentComponent.create_from_attributes(entities=[]))
            elif item["type"] in {"gold"}:
                components.append(MoneyComponent.create_from_attributes(amount=item["amount"]))

            ecdb, _ = add_entity(ecdb=ecdb, components=components)

    return ecdb
