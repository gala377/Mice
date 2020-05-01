from abc import ABC, abstractmethod
from typing import MutableMapping, Mapping
from ecs.system import System
from ecs import entity


class Executor(ABC):
    @abstractmethod
    def __init__(
        self,
        storage: entity.Storage,
        systems: Mapping[str, System],
        resources: Mapping[str, entity.Entity],
    ):
        ...

    @abstractmethod
    def run_iteration(self, systems: MutableMapping[str, System]) -> None:
        ...

    @abstractmethod
    def stop_all(self):
        ...
