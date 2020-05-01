from abc import abstractmethod, ABC
from typing import Generator, Any, Optional, Mapping
from types import SimpleNamespace

from ecs import entity
from ecs.entity import Entity
from ecs.executor.policy import ResumePolicy

RunningSystem = Generator[Optional[ResumePolicy], Any, Any]


class System(ABC):

    __entity_storage: entity.Storage
    __resources: Mapping[str, Entity]
    __res_proxy: object

    def init(
        self, storage: entity.Storage, resources: Mapping[str, Entity]
    ) -> RunningSystem:
        self._init(storage, resources)
        return self.run()

    def _init(self, storage: entity.Storage, resources: Mapping[str, Entity]):
        self.__entity_storage = storage
        self.__resources = resources
        self.__res_proxy = SimpleNamespace()
        for res, en in self.__resources.items():
            setattr(self.__res_proxy, res, en)

    @property
    def entity_storage(self):
        return self.__entity_storage

    @property
    def resources(self):
        return self.__res_proxy

    @abstractmethod
    def run(self) -> RunningSystem:
        ...


class GeneratorSystem(System):
    def run(self):
        return iter(self)

    @abstractmethod
    def __iter__(self) -> RunningSystem:
        ...


class SimpleSystem(GeneratorSystem):
    def _init(self, storage, resources):
        super()._init(storage, resources)
        self.create()

    def create(self):
        ...

    def start(self):
        ...

    @abstractmethod
    def update(self) -> RunningSystem:
        ...

    def __iter__(self) -> RunningSystem:
        self.start()
        yield None
        while True:
            yield from self.update()


class IteratorSystem(GeneratorSystem, RunningSystem):
    def __iter__(self) -> RunningSystem:
        return self

    @abstractmethod
    def __next__(self) -> Optional[ResumePolicy]:
        ...

    def send(self, val: Any):
        raise NotImplementedError("IteratorSystem doesn't implement send method")

    def throw(self, typ, val=None, tb=None):
        err = NotImplementedError("IteratorSystem doesn't implement throw method")
        if val is None:
            if tb is None:
                raise err from typ
            val = typ()
        if tb is not None:
            val = val.with_traceback(tb)
        raise err from val

    def close(self):
        raise NotImplementedError("IteratorSystem doesn't implement close method")
