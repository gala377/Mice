from abc import (
    ABC,
    abstractmethod,
)
import time
import multiprocessing as mp
import logging
import multiprocessing as mc
from multiprocessing.pool import AsyncResult
from typing import (
    Mapping,
    MutableMapping,
    Tuple,
    Callable,
    Any,
    Generator,
)

from ecs.system import System
from ecs import entity


LOGGER = logging.getLogger(__name__)


class ResumePolicy:
    ...


class AsyncWait(ResumePolicy):

    # should be Callable[..., Any] but mypy thinks its a method
    # and doesn't allow any assignments
    func: Any
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class Executor(ABC):
    @abstractmethod
    def run_iteration(
        self, systems: Mapping[str, System], entity_storage: entity.Storage,
    ) -> None:
        ...


SystemState = Generator[ResumePolicy, Any, Any]


class SimpleExecutor(Executor):

    systems: MutableMapping[str, SystemState]
    stopped_systems: MutableMapping[str, AsyncResult]
    pool: mc.pool.Pool

    def __init__(self):
        super().__init__()
        self.systems = {}
        self.stopped_systems = {}
        self.pool = mp.Pool()

    def run_iteration(
        self, systems: Mapping[str, System], entity_storage: entity.Storage,
    ):
        for name, (system, iterator) in self.active_systems(systems).items():
            LOGGER.debug("[%s]: Running %s system.", time.time(), name)
            system.update(entity_storage)
            res = next(iterator)
            self.match_yield(name, res)
            if len(self.stopped_systems) > 0:
                self.pool_waiting()
            LOGGER.debug("[%s]: Finnished", time.time())

    def active_systems(
        self, systems: Mapping[str, System],
    ) -> Mapping[str, Tuple[System, SystemState]]:
        return {
            name: (instance, self.systems[name])
            for name, instance in systems.items()
            if name not in self.stopped_systems
        }

    def match_yield(self, system_name: str, yieldk: ResumePolicy) -> bool:
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
