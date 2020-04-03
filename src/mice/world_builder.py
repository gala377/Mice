from typing import (
    Callable,
    MutableSequence,
    Tuple,
    Sequence,
    Type,
    Optional,
)

from ecs.component import Component
from ecs.executor.abc import Executor
from ecs.entity import Storage
from ecs.system import System
from ecs.world import World


class WorldBuilder:

    _systems: MutableSequence[System]
    _components: MutableSequence[Type[Component]]
    _resources: MutableSequence[Tuple[str, Sequence[Component]]]
    _plugins: MutableSequence[Callable]
    _executor: Optional[Type[Executor]]
    _storage: Optional[Storage]

    def __init__(self):
        self._systems = []
        self._components = []
        self._resources = []
        self._plugins = []
        self._executor = None
        self._storage = None

    def add_system(self, system: System, add_front: bool = False):
        if add_front:
            self._systems = [system] + self._systems  # type: ignore
        else:
            self._systems.append(system)

    def add_component(self, comp: Type[Component]):
        self._components.append(comp)

    def add_resource(self, name: str, comps: Sequence[Component]):
        self._resources.append((name, comps))

    def add_plugin(self, plug: Callable):
        self._plugins.append(plug)

    def set_executor(self, executor: Type[Executor]):
        self._executor = executor

    def set_storage(self, storage: Storage):
        self._storage = storage

    def build(self) -> World:
        if self._storage is None or self._executor is None:
            raise RuntimeError("Storage or Executor for the world" "has not been set.")
        w = World(storage=self._storage)
        for s in self._systems:
            w.register(s)
        for c in self._components:
            w.register_component(c)
        for p in self._plugins:
            w.plug(p)
        for name, r in self._resources:
            w.register(name, r)
        w.register_executor(self._executor)
        return w
