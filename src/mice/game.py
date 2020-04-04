import pygame
import pygame_plugin

from typing import Tuple

from ecs.entity import SOAStorage
from ecs.executor.simple import SimpleExecutor
from ecs.world import World

from mice_common.components import Time
from mice_common.autoregister import ComponentRepository, SystemsRepository

from mice.world_builder import WorldBuilder


class Game:

    TIMER_RES = "TIMER"
    WINDOW_RES = "WINDOW"

    _world: World

    def __init__(self, wb: WorldBuilder, window_size: Tuple[int, int]):
        wb.set_storage(SOAStorage())
        wb.set_executor(SimpleExecutor)
        wb.add_plugin(lambda: pygame.init())
        self._add_common_components(wb)
        self._add_common_resources(wb, window_size)
        self._add_common_systems(wb)
        self._world = wb.build()

    def _add_common_resources(self, wb: WorldBuilder, ws: Tuple[int, int]):
        wb.add_resource(self.TIMER_RES, [Time()])
        wb.add_resource(
            self.WINDOW_RES, [pygame_plugin.components.Window(ws[0], ws[1])]
        )

    def _add_common_components(self, wb: WorldBuilder):
        for c in ComponentRepository.components:
            print(f"Registering component {c.__name__}")
            wb.add_component(c)

    def _add_common_systems(self, wb: WorldBuilder):
        wb.add_system(pygame_plugin.systems.DrawWindow(self.WINDOW_RES), add_front=True)
        print("Addind systems...")
        for s in SystemsRepository.systems:
            print(f"Registering system {s.__class__.__name__}")
            wb.add_system(s)

    def start(self):
        if self._world is None:
            raise RuntimeError("World has not been yet initialized")
        self._world.start()
