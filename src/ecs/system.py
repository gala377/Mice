from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterator

from ecs import entity
from ecs.executor import ResumePolicy


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
