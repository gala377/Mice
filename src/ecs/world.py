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
from ecs.executor import Executor
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
    entity_storage: entity.Storage
    executor: Executor

    def __init__(
        self, storage: entity.Storage, systems: Mapping[str, System], executor: Executor
    ):
        self.systems = systems
        self.entity_storage = storage
        self.executor = executor

    def start(self):
        try:
            self.loop()
        finally:
            print("STOPPING SYSTEM...")

    def loop(self):
        while True:
            self.executor.run_iteration(
                self.systems, self.entity_storage,
            )
