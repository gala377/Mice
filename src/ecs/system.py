from abc import abstractmethod, ABC
from typing import Generator, Any, Optional, Mapping

from ecs import entity
from ecs.entity import Entity
from ecs.executor.policy import ResumePolicy


RunningSystem = Generator[Optional[ResumePolicy], Any, Any]


class System(ABC):

    entity_storage: entity.Storage
    resources: Mapping[str, Entity]

    def init(
        self, storage: entity.Storage, resources: Mapping[str, Entity]
    ) -> RunningSystem:
        self.entity_storage = storage
        self.resources = resources
        return self.run()

    @abstractmethod
    def run(self) -> RunningSystem:
        ...


class GeneratorSystem(System):
    def run(self):
        return iter(self)

    @abstractmethod
    def __iter__(self) -> RunningSystem:
        ...


class SimpleSystem(GeneratorSystem, RunningSystem):
    def __iter__(self) -> RunningSystem:
        return self

    @abstractmethod
    def __next__(self) -> Optional[ResumePolicy]:
        ...

    def send(self, val: Any):
        raise NotImplementedError("SimpleSytem doesn't implement send method")

    def throw(self, typ, val=None, tb=None):
        err = NotImplementedError("SimpleSystem doesn't implement throw method")
        if val is None:
            if tb is None:
                raise err from typ
            val = typ()
        if tb is not None:
            val = val.with_traceback(tb)
        raise err from val

    def close(self):
        raise NotImplementedError("SimpleSystem doesn't implement close method")
