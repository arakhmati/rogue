import typing

import attr


@attr.s(frozen=True, kw_only=True)
class PositionComponent:
    y_axis: int = attr.ib()
    x_axis: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class VelocityComponent:
    x_axis: int = attr.ib()
    y_axis: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class SizeComponent:
    height: int = attr.ib()
    width: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class AppearanceComponent:
    symbol: str = attr.ib()
    color: str = attr.ib()


@attr.s(frozen=True, kw_only=True)
class MoneyComponent:
    amount: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class HealthComponent:
    amount: int = attr.ib()


@attr.s(frozen=True, kw_only=True)
class DamageComponent:
    damage: int = attr.ib()


RogueComponentUnion = typing.Union[
    PositionComponent,
    VelocityComponent,
    SizeComponent,
    AppearanceComponent,
    MoneyComponent,
    HealthComponent,
    DamageComponent,
]


# Create functions
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
