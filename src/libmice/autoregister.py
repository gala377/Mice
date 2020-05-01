from typing import (
    MutableSequence,
    Sequence,
    Type,
    Any,
    Union,
    Tuple,
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
        return system(cls)
    return component(cls)


def system(cls: Type[System]):
    default_args = getattr(cls, "default_args", [])
    default_kwargs = getattr(cls, "default_kwargs", {})
    SystemsRepository.add(cls(*default_args, **default_kwargs))
    return cls


def component(cls: Type[Any]):
    ComponentRepository.add(cls)
    return cls


class ResourceRepository:

    resources: MutableSequence[Tuple[str, Sequence[Any]]] = []

    @classmethod
    def add(cls, name: str, comps: Sequence[Any]):
        print(f"Adding resource {name}")
        cls.resources.append((name, comps))


def resource(name: Union[str, Type[Any]]):
    def inner(cls: Type[Any]):
        _name = (
            name
            if isinstance(name, str)
            else getattr(cls, "name", _camel_case_to_snake_case(cls.__name__))
        )
        comps = getattr(cls, "components", [])
        ResourceRepository.add(_name, comps)
        return cls

    if isinstance(name, str):
        return inner
    return inner(name)


def _camel_case_to_snake_case(name: str) -> str:
    new_name = ""
    for i in range(len(name)):
        if name[i].isupper():
            if i > 0:
                new_name += "_"
            new_name += name[i].lower()
        else:
            new_name += name[i]
    return new_name
