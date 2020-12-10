import abc
from typing import (
    Tuple,
    Generator,
)

import attr

from rogue.generic.ecs import (
    EntityComponentDatabase,
    Entity,
)
from rogue.components import ComponentUnion
from rogue.systems.common.actions import ActionUnion


@attr.s(frozen=True, kw_only=True)
class NoReturnSystemTrait(abc.ABC):
    @abc.abstractmethod
    def __call__(self, *, ecdb: EntityComponentDatabase[ComponentUnion]) -> None:
        ...


@attr.s(frozen=True, kw_only=True)
class YieldChangesSystemTrait:
    @abc.abstractmethod
    def __call__(
        self, *, ecdb: EntityComponentDatabase[ComponentUnion]
    ) -> Generator[Tuple[Entity, ActionUnion], None, None]:
        ...
