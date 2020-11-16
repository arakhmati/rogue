from rogue.constants import ENTITY_TYPES
from rogue.types import (
    TypeComponent,
    PositionComponent,
    VelocityComponent,
    SizeComponent,
    AppearanceComponent,
)


def create_type_component(*, entity_type: str) -> TypeComponent:
    assert entity_type in ENTITY_TYPES, f"'{entity_type}' is not in ENTITY_TYPES"
    return TypeComponent(entity_type=entity_type)


def create_position_component(*, y_axis: int, x_axis: int) -> PositionComponent:
    return PositionComponent(y_axis=y_axis, x_axis=x_axis)


def create_velocity_component(*, y_axis: int, x_axis: int) -> VelocityComponent:
    return VelocityComponent(y_axis=y_axis, x_axis=x_axis)


def create_size_component(*, height: int, width: int) -> SizeComponent:
    return SizeComponent(height=height, width=width)


def create_apperance_component(*, symbol: str, color: str) -> AppearanceComponent:
    return AppearanceComponent(symbol=symbol, color=color)
