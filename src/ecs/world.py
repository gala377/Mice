from typing import MutableMapping, Sequence, Optional, Type, Callable
from functools import singledispatchmethod  # type: ignore

from ecs.executor import Executor
from ecs.system import System
from ecs import entity
from ecs.entity import Entity
from ecs.component import Component


class World:

    """
    Order of registering:
        Executor has to go last
        Components have to be registered before resources
    """

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
        self.resources = {}

    def start(self):
        try:
            self.loop()
        finally:
            print("STOPPING SYSTEM...")
            if self.executor is not None:
                self.executor.stop_all()
            print("STOPPED ALL SYSTEMS...")

    def loop(self):
        if self.executor is None:
            raise RuntimeError("Trying to run null executor")
        while True:
            self.executor.run_iteration(self.systems)

    def register_executor(self, executor: Type[Executor]):
        exc = executor(self.entity_storage, self.systems, self.resources)
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

    def register_component(self, comp: Type[Component]):
        self.entity_storage.register(comp)

    def get_resource(self, name: str) -> Optional[Entity]:
        return self.resources.get(name)

    def plug(self, func: Callable):
        func()
