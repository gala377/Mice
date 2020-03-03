from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    NewType,
    Iterator,
    Iterable,
    Callable,
    Any,
    Mapping,
    Tuple,
)

from ecs import entity


class YieldKind:
    ...


class Ok(YieldKind):
    ...


ok = Ok()


class AsyncWait(YieldKind):

    func: Callable
    args: Tuple[Any]
    kwargs: Mapping[str, Any]

    def __init__(self, func: Callable, *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class System(ABC):
    def update(self, storage: entity.Storage):
        return

    def __iter__(self) -> Iterator[YieldKind]:
        return self

    @abstractmethod
    def __next__(self) -> YieldKind:
        ...


class GeneratorSystem(System):
    @abstractmethod
    def __iter__(self) -> Iterator[YieldKind]:
        ...

    def __next__(self):
        return None
