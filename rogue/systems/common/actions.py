from typing import Type, Union

import attr

from rogue.generic.ecs import Entity
from rogue.components import ComponentUnion


@attr.s(frozen=True, kw_only=True)
class RemoveEntityAction:
    entity: Entity = attr.ib()


@attr.s(frozen=True, kw_only=True)
class AddComponentAction:
    component: ComponentUnion = attr.ib()


@attr.s(frozen=True, kw_only=True)
class RemoveComponentAction:
    component_type: Type[ComponentUnion] = attr.ib()


ActionUnion = Union[RemoveEntityAction, AddComponentAction, RemoveComponentAction]
