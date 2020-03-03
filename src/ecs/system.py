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
from executor import ResumePolicy


class System(ABC):
    def update(self, storage: entity.Storage):
        return

    def __iter__(self) -> Iterator[ResumePolicy]:
        return self

    @abstractmethod
    def __next__(self) -> ResumePolicy:
        ...


class GeneratorSystem(System):
    @abstractmethod
    def __iter__(self) -> Iterator[ResumePolicy]:
        ...

    def __next__(self):
        return None
