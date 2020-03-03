import time
import multiprocessing as mp

from multiprocessing.pool import AsyncResult
from typing import (
    Iterable,
    Mapping,
    Tuple,
    Iterator,
    Sequence,
    Callable,
    Any,
)

import ecs
from ecs.system import (
    System,
    YieldKind,
    AsyncWait,
    ok,
)
from ecs import entity

SystemState = Tuple[System, Iterator[YieldKind]]

class World:

    systems: Mapping[str, SystemState]
    stopped_systems: Mapping[str, AsyncResult]
    entity_storage: entity.Storage

    def __init__(self):
        self.systems = {}
        self.stopped_systems = {}
        self.entity_storage = entity.SOAStorage()
        self.pool = mp.Pool()
    
    def register(self, system: System, name: str = None):
        if name is None:
            name = system.__class__.__name__
        self.systems[name] = (system, iter(system))

    def start(self):
        try:
            self.loop()
        finally:
            print("STOPPING SYSTEM...")

    def loop(self):
        while True:
            for name, (system, iterator) in self.active_systems.items():
                print(f"[{time.time()}][World]: Running {name} system.")
                system.update(self.entity_storage)
                res = next(iterator)
                # print(f"RES IS {res}: is AsyncWait? {isinstance(res, mices.system.AsyncWait)}")
                # print(f"Type magic {type(res) == AsyncWait} And subclass {issubclass(type(res), AsyncWait)}")
                # print(f"WTF {type(res)}, {AsyncWait}")
                self.match_yield(name, res)
                if len(self.stopped_systems) > 0:
                    self.pool_waiting()
                print(f"[{time.time()}][World]: Finnished")

    @property
    def active_systems(self) -> Mapping[str, SystemState]:
        return { 
            name: state 
            for name, state in self.systems.items() 
            if name not in self.stopped_systems
        }

    def match_yield(self, system_name: str, yieldk: YieldKind) -> bool:
        """
        Schedules system based on the yielded value.
        
        Returns:
            True if system should be scheduled for the next iteration.
            Flase if the system should be paused.
        """
        if isinstance(yieldk, AsyncWait):
            self.async_wait(
                system_name,
                yieldk.func,
                *yieldk.args,
                **yieldk.kwargs)
            return False
        return True

    def async_wait(self, system: str, op: Callable, *args: Any, **kwargs: Any):
        res = self.pool.apply_async(op, args=args, kwds=kwargs)
        self.stopped_systems[system] = res

    def pool_waiting(self):
        resume = []
        for name, op in self.stopped_systems.items():
            if op.ready():
                print(f"[{time.time()}][World]: Resuming system {name}")
                res = self.systems[name][1].send(op.get())
                if self.match_yield(name, res):
                    resume.append(name)
        for name in resume:
            del self.stopped_systems[name]
