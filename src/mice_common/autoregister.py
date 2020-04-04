from typing import (
    MutableSequence,
    Type,
    Any,
)

from ecs.system import System


class SystemsRepository:

    systems: MutableSequence[System] = []

    @classmethod
    def add(cls, sys):
        cls.systems.append(sys)


class ComponentRepository:

    components: MutableSequence[Type[Any]] = []

    @classmethod
    def add(cls, comp):
        cls.components.append(comp)


def register(cls: Type[Any]):
    if issubclass(cls, System):
        return register_system(cls)
    return register_component(cls)


def register_system(cls: Type[System]):
    default_args = getattr(cls, "default_args", [])
    default_kwargs = getattr(cls, "default_kwargs", {})
    SystemsRepository.add(cls(*default_args, **default_kwargs))  # type: ignore
    return cls


def register_component(cls: Type[Any]):
    ComponentRepository.add(cls)
    return cls
