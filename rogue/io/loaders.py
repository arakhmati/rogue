import pathlib
import pprint

from typing import (
    Any,
    Dict,
    List,
    Tuple,
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
from rogue.types import TypeEnum, STRING_TO_TYPE_ENUM, ENEMY_TYPES

RoomConfig = Dict[Any, Any]


def _load_room_config(*, input_file_name: pathlib.Path) -> RoomConfig:
    with open(input_file_name) as input_file:
        room_config: RoomConfig = yaml.safe_load(input_file)
    return room_config


def _parse_coordinates(*, coordinates: str) -> Tuple[int, int]:
    y_axis, x_axis = (int(number) for number in coordinates.split(","))
    return y_axis, x_axis


def _parse_room_coordinates(*, coordinates: str) -> Dict[str, int]:
    y_axis, x_axis = _parse_coordinates(coordinates=coordinates)
    return {"y_axis": y_axis, "x_axis": x_axis}


def _parse_entity_coordinates(
    *, coordinates: str, entity_type: TypeEnum, room_height: int, room_width: int, room_y_axis: int, room_x_axis: int
) -> Dict[str, int]:
    parsed_y_axis, parsed_x_axis = _parse_coordinates(coordinates=coordinates)

    if entity_type == TypeEnum.Door:
        assert parsed_y_axis == 0 or parsed_y_axis == room_height or parsed_x_axis == 0 or parsed_x_axis == room_width
    else:
        assert 0 < parsed_y_axis < room_height
        assert 0 < parsed_x_axis < room_width

    y_axis = parsed_y_axis + room_y_axis
    x_axis = parsed_x_axis + room_x_axis

    return {"y_axis": y_axis, "x_axis": x_axis}


def _parse_size(*, size: str) -> Dict[str, int]:
    height, width = (int(number) for number in size.split(","))
    return {"height": height, "width": width}


def _load_entity_specific_components(entity_type: TypeEnum, item: Dict[str, Any]) -> List[ComponentUnion]:
    components: List[ComponentUnion] = []
    if entity_type == TypeEnum.Hero:
        components.append(VelocityComponent.create_from_attributes(y_axis=0, x_axis=0))
        components.append(HealthComponent.create_from_attributes(amount=100))
        components.append(MoneyComponent.create_from_attributes(amount=0))
        components.append(InventoryComponent.create_from_attributes(entities=[]))
        components.append(EquipmentComponent.create_from_attributes(entities=[]))
    elif entity_type in ENEMY_TYPES:
        components.append(VelocityComponent.create_from_attributes(y_axis=0, x_axis=0))
        components.append(HealthComponent.create_from_attributes(amount=100))
        components.append(InventoryComponent.create_from_attributes(entities=[]))
        components.append(EquipmentComponent.create_from_attributes(entities=[]))
    elif entity_type == TypeEnum.Gold:
        components.append(MoneyComponent.create_from_attributes(amount=item["amount"]))
    elif entity_type == TypeEnum.Potion:
        components.append(HealthComponent.create_from_attributes(amount=item["amount"]))
    return components


def load_rogue_ecdb_from_input_yaml(input_file_name: pathlib.Path) -> EntityComponentDatabase[ComponentUnion]:

    logger.info(f"Input file: {input_file_name}")

    room_config = _load_room_config(input_file_name=input_file_name)
    logger.info(f"Room Config: {pprint.pformat(room_config)}")

    ecdb: EntityComponentDatabase[ComponentUnion] = create_ecdb()
    for room in room_config:
        room_coordinates = _parse_room_coordinates(coordinates=room["coordinates"])
        room_size = _parse_size(size=room["size"])
        room_components: List[ComponentUnion] = [
            PositionComponent.create_from_attributes(**room_coordinates),
            SizeComponent.create_from_attributes(**room_size),
            TypeComponent.create_from_attributes(entity_type=TypeEnum.Room),
        ]
        ecdb, _ = add_entity(ecdb=ecdb, components=room_components)
        for item in room["items"]:
            entity_type = STRING_TO_TYPE_ENUM[item["type"]]
            entity_coordinates = _parse_entity_coordinates(
                coordinates=item["coordinates"],
                entity_type=entity_type,
                room_height=room_size["height"],
                room_width=room_size["width"],
                room_y_axis=room_coordinates["y_axis"],
                room_x_axis=room_coordinates["x_axis"],
            )
            components: List[ComponentUnion] = [
                PositionComponent.create_from_attributes(**entity_coordinates),
                TypeComponent.create_from_attributes(entity_type=entity_type),
            ]

            entity_specific_components = _load_entity_specific_components(entity_type=entity_type, item=item)
            components.extend(entity_specific_components)

            ecdb, _ = add_entity(ecdb=ecdb, components=components)

    return ecdb
