from abc import ABC, abstractmethod
from typing import Mapping
from ecs.system import System
from ecs import entity


class Executor(ABC):
    @abstractmethod
    def __init__(self, storage: entity.Storage, systems: Mapping[str, System]):
        ...

    @abstractmethod
    def run_iteration(self, systems: Mapping[str, System]) -> None:
        ...
