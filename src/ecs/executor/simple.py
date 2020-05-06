import logging
from typing import (
    MutableMapping,
    Mapping,
    Tuple,
    Optional,
    MutableSet,
)

from ecs.system import System, RunningSystem
from ecs.executor.abc import Executor
from ecs.executor.policy import (
    ResumePolicy,
    Defer,
    Restart,
    Terminate,
    Pause,
    Unpause,
    Start,
)
from ecs import entity


LOGGER = logging.getLogger(__name__)


class SimpleExecutor(Executor):

    systems: MutableMapping[str, RunningSystem]

    defered_systems: MutableSet[str]
    paused_systems: MutableSet[str]
    systems_to_restart: MutableSet[str]

    def __init__(
        self,
        storage: entity.Storage,
        systems: Mapping[str, System],
        res: Mapping[str, entity.Entity],
    ):
        self.systems = {n: s.init(storage, res) for n, s in systems.items()}
        self.defered_systems = set()
        self.paused_systems = set()
        self.storage = storage
        self.resources = res

    def run_iteration(self, systems: MutableMapping[str, System]):
        for name, (_, iterator) in self.active_systems(systems).items():
            res = next(iterator)
            self.match_yield(name, res, systems)
        for name in self.defered_systems:
            next(self.systems[name])
        self.defered_systems.clear()

    def active_systems(
        self, systems: Mapping[str, System],
    ) -> Mapping[str, Tuple[System, RunningSystem]]:
        return {
            name: (instance, self.systems[name])
            for name, instance in systems.items()
            if name not in self.paused_systems
        }

    def match_yield(
        self,
        system_name: str,
        yieldk: Optional[ResumePolicy],
        systems: MutableMapping[str, System],
    ):
        if yieldk is None:
            return
        tag = yieldk.tag()
        if tag == Defer.TAG:
            self.defered_systems.add(system_name)
        elif tag == Restart.TAG:
            self.systems[system_name] = self.systems[system_name].run()
        elif tag == Pause.TAG:
            self.paused_systems.add(system_name)
        elif tag == Unpause.TAG:
            self.paused_systems.remove(yieldk.system)
            if yieldk.with_args is not None:
                res = self.systems[yieldk.system].send(*yieldk.with_args)
                self.match_yield(yieldk.system, res, systems)
        elif tag == Start.TAG:
            if yieldk.system_name in self.systems:
                raise RuntimeError(
                    f"Tried to create system with name {yieldk.system_name} which already exists"
                )
            systems[yieldk.system_name] = yieldk.system_instance
            self.systems[yieldk.system_name] = yieldk.system_instance.init(
                self.storage, self.resources
            )
        elif tag == Terminate.TAG:
            del self.systems[system_name]
            del systems[system_name]
        else:
            raise RuntimeError("Resume policy not supported on SimpleExecutor")

    def stop_all(self):
        print("Stopping systems...")
        for s in self.systems.values():
            s.close()
        print("All stopped")
