import pygame
import pygame_plugin

from typing import Tuple

from ecs.entity import SOAStorage
from ecs.executor.simple import SimpleExecutor
from ecs.world import World

from mice_common.components import Transform, Time
from mice_common.systems import UpdateTime

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
        wb.add_component(pygame_plugin.components.Window)
        wb.add_component(pygame_plugin.components.Image)
        wb.add_component(Transform)
        wb.add_component(Time)

    def _add_common_systems(self, wb: WorldBuilder):
        wb.add_system(pygame_plugin.systems.DrawWindow(self.WINDOW_RES))
        wb.add_system(pygame_plugin.systems.WindowEvents())
        wb.add_system(pygame_plugin.systems.DrawImages(self.WINDOW_RES))
        wb.add_system(UpdateTime(self.TIMER_RES))

    def start(self):
        if self._world is None:
            raise RuntimeError("World has not been yet initialized")
        self._world.start()
