from typing import Union

import attr


@attr.s(frozen=True, kw_only=True)
class PositionComponent:
    y_axis: int = attr.ib()
    x_axis: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, y_axis: int, x_axis: int) -> "PositionComponent":
        return cls(y_axis=y_axis, x_axis=x_axis)


@attr.s(frozen=True, kw_only=True)
class VelocityComponent:
    x_axis: int = attr.ib()
    y_axis: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, y_axis: int, x_axis: int) -> "VelocityComponent":
        return cls(y_axis=y_axis, x_axis=x_axis)


@attr.s(frozen=True, kw_only=True)
class SizeComponent:
    height: int = attr.ib()
    width: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, height: int, width: int) -> "SizeComponent":
        return cls(height=height, width=width)


@attr.s(frozen=True, kw_only=True)
class AppearanceComponent:
    symbol: str = attr.ib()
    color: str = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, symbol: str, color: str) -> "AppearanceComponent":
        return cls(symbol=symbol, color=color)


@attr.s(frozen=True, kw_only=True)
class MoneyComponent:
    amount: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, amount: int) -> "MoneyComponent":
        return cls(amount=amount)


@attr.s(frozen=True, kw_only=True)
class HealthComponent:
    amount: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, amount: int) -> "HealthComponent":
        return cls(amount=amount)


@attr.s(frozen=True, kw_only=True)
class DamageComponent:
    damage: int = attr.ib()

    @classmethod
    def create_from_attributes(cls, *, damage: int) -> "DamageComponent":
        return cls(damage=damage)


RogueComponentUnion = Union[
    PositionComponent,
    VelocityComponent,
    SizeComponent,
    AppearanceComponent,
    MoneyComponent,
    HealthComponent,
    DamageComponent,
]
