from typing import MutableMapping, Sequence, Optional, Type
from functools import singledispatchmethod  # type: ignore

from ecs.executor import Executor
from ecs.system import System
from ecs import entity
from ecs.entity import Entity
from ecs.component import Component


class World:

    systems: MutableMapping[str, System]
    entity_storage: entity.Storage
    executor: Optional[Executor]
    resources: MutableMapping[str, Entity]

    def __init__(
        self, storage: entity.Storage,
    ):
        self.systems = {}
        self.entity_storage = storage
        self.executor = None

    def start(self):
        try:
            self.loop()
        finally:
            print("STOPPING SYSTEM...")

    def loop(self):
        if self.executor is None:
            raise RuntimeError("Trying to run null executor")
        while True:
            self.executor.run_iteration(self.systems)

    def register_executor(self, executor: Type[Executor]):
        exc = executor(self.entity_storage, self.systems)
        self.executor = exc

    @singledispatchmethod
    def register(self, arg):
        raise NotImplementedError(f"Cannot register {type(arg).__name__}")

    @register.register
    def _(self, system: System):
        self.systems[type(system).__name__] = system

    @register.register  # type: ignore
    def _(self, name: str, system: System):
        self.systems[name] = system

    @register.register  # type: ignore
    def _(self, name: str, components: Sequence[Component]):
        en = self.entity_storage.create_entity(components)
        self.resources[name] = en

    def get_resource(self, name: str) -> Optional[Entity]:
        return self.resources.get(name)
