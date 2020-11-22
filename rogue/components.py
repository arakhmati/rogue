from rogue.types import (
    PositionComponent,
    VelocityComponent,
    SizeComponent,
    AppearanceComponent,
    MoneyComponent,
    HealthComponent,
)


def create_position_component(*, y_axis: int, x_axis: int) -> PositionComponent:
    return PositionComponent(y_axis=y_axis, x_axis=x_axis)


def create_velocity_component(*, y_axis: int, x_axis: int) -> VelocityComponent:
    return VelocityComponent(y_axis=y_axis, x_axis=x_axis)


def create_size_component(*, height: int, width: int) -> SizeComponent:
    return SizeComponent(height=height, width=width)


def create_apperance_component(*, symbol: str, color: str) -> AppearanceComponent:
    return AppearanceComponent(symbol=symbol, color=color)


def create_money_component(*, amount: int) -> MoneyComponent:
    return MoneyComponent(amount=amount)


def create_health_component(*, amount: int) -> HealthComponent:
    return HealthComponent(amount=amount)
