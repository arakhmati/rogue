from typing import Type, Union

import attr

from rogue.components import ComponentUnion


@attr.s(frozen=True, kw_only=True)
class AddComponentAction:
    component: ComponentUnion = attr.ib()


@attr.s(frozen=True, kw_only=True)
class RemoveComponentAction:
    component_type: Type[ComponentUnion] = attr.ib()


ActionUnion = Union[AddComponentAction, RemoveComponentAction]
