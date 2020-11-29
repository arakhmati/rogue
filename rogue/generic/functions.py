from typing import (
    Any,
    Type,
    TypeVar,
)

import attr

InstanceType = TypeVar("InstanceType")


def is_attr_class(instance: InstanceType) -> bool:
    return hasattr(instance, "__attrs_attrs__")


def evolve(instance: InstanceType, **changes: Any) -> InstanceType:
    if is_attr_class(instance):
        return attr.evolve(instance, **changes)
    raise ValueError(f"No implementation of evolve for {type(instance)}")


def type_to_str(klass: Type[Any]) -> str:
    return klass.__name__


TemplateClass = TypeVar("TemplateClass")
