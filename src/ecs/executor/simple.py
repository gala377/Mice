import logging
import time
import multiprocessing as mp
from typing import MutableMapping, Mapping, Tuple, Callable, Any, Optional
from multiprocessing.pool import AsyncResult

from ecs.system import System, RunningSystem
from ecs.executor.abc import Executor
from ecs.executor.policy import ResumePolicy, AsyncWait
from ecs import entity


LOGGER = logging.getLogger(__name__)


class SimpleExecutor(Executor):

    systems: MutableMapping[str, RunningSystem]
    stopped_systems: MutableMapping[str, AsyncResult]
    pool: mp.pool.Pool

    def __init__(self, storage: entity.Storage, systems: Mapping[str, System]):
        self.systems = {n: s.init(storage) for n, s in systems.items()}
        self.stopped_systems = {}
        self.pool = mp.Pool()

    def run_iteration(self, systems: Mapping[str, System]):
        for name, (system, iterator) in self.active_systems(systems).items():
            LOGGER.debug("[%s]: Running %s system.", time.time(), name)
            res = next(iterator)
            self.match_yield(name, res)
            if len(self.stopped_systems) > 0:
                self.pool_waiting()
            LOGGER.debug("[%s]: Finnished", time.time())

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
        """
        if isinstance(yieldk, AsyncWait):
            self.async_wait(system_name, yieldk.func, *yieldk.args, **yieldk.kwargs)
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
