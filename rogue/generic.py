import typing

import attr

InstanceType = typing.TypeVar("InstanceType")


def is_attr_class(instance: InstanceType) -> bool:
    return hasattr(instance, "__attrs_attrs__")


def evolve(instance: InstanceType, **changes: typing.Any) -> InstanceType:
    if is_attr_class(instance):
        return attr.evolve(instance, **changes)
    raise ValueError(f"No implementation of evolve for {type(instance)}")


def type_to_str(klass: typing.Type[typing.Any]) -> str:
    return klass.__name__
