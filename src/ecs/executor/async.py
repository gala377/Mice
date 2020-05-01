import logging
import time
import multiprocessing as mp
from typing import (
    MutableMapping,
    Mapping,
    Tuple,
    Callable,
    Any,
    Optional,
    MutableSequence,
)
from multiprocessing.pool import AsyncResult

from ecs.system import System, RunningSystem
from ecs.executor.abc import Executor
from ecs.executor.policy import ResumePolicy, AsyncWait, Defer
from ecs import entity


LOGGER = logging.getLogger(__name__)

"""
TODO: Old executor, needs imporvements
"""
class Async(Executor):

    systems: MutableMapping[str, RunningSystem]
    stopped_systems: MutableMapping[str, AsyncResult]
    pool: mp.pool.Pool

    defered_systems: MutableSequence[str]

    def __init__(
        self,
        storage: entity.Storage,
        systems: Mapping[str, System],
        res: Mapping[str, entity.Entity],
    ):
        self.systems = {n: s.init(storage, res) for n, s in systems.items()}
        self.stopped_systems = {}
        self.pool = mp.Pool()
        self.defered_systems = []

    def run_iteration(self, systems: Mapping[str, System]):
        for name, (_, iterator) in self.active_systems(systems).items():
            LOGGER.debug("[%s]: Running %s system.", time.time(), name)
            res = next(iterator)
            self.match_yield(name, res)
            if len(self.stopped_systems) > 0:
                self.pool_waiting()
            LOGGER.debug("[%s]: Finnished", time.time())
        for name in self.defered_systems:
            next(self.systems[name])
        self.defered_systems.clear()

    def active_systems(
        self, systems: Mapping[str, System],
    ) -> Mapping[str, Tuple[System, RunningSystem]]:
        return {
            name: (instance, self.systems[name])
            for name, instance in systems.items()
            if name not in self.stopped_systems
        }

    def match_yield(self, system_name: str, yieldk: Optional[ResumePolicy]) -> bool:
        """
        Schedules system based on the yielded value.
        
        Returns:
            True if system should be scheduled for the next iteration.
            Flase if the system should be paused.

        TODO:
            Can be sped up. Instead of checking `isinstance` check
            for tag being an int or smth.
        """
        if isinstance(yieldk, AsyncWait):
            self.async_wait(system_name, yieldk.func, *yieldk.args, **yieldk.kwargs)
            return False
        if isinstance(yieldk, Defer):
            self.defered_systems.append(system_name)
            return False
        return True

    def async_wait(self, system: str, op: Callable, *args: Any, **kwargs: Any):
        res = self.pool.apply_async(op, args=args, kwds=kwargs)
        self.stopped_systems[system] = res

    def pool_waiting(self):
        resume = []
        for name, op in self.stopped_systems.items():
            if op.ready():
                LOGGER.debug("[%s][World]: Resuming system %s", time.time(), name)
                res = self.systems[name].send(op.get())
                if self.match_yield(name, res):
                    resume.append(name)
        for name in resume:
            del self.stopped_systems[name]

    def stop_all(self):
        try:
            print("Stopping systems...")
            for s in self.systems.values():
                s.close()
            print("All stopped")
            print("Stopping thread poll...")
            self.pool.close()
            self.pool.join()
        except Exception as e:
            print(f"Cought exception during stopping systems: {e}")
            print("Terminating thread pool")
            self.pool.terminate()
            print("Terminated")
