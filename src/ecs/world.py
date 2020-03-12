from typing import Mapping

from ecs.executor import (
    Executor,
    System,
)
from ecs import entity


class World:

    systems: Mapping[str, System]
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
