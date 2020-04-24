import pygame
import pygame_plugin

from typing import Tuple

from ecs.entity import SOAStorage
from ecs.executor.simple import SimpleExecutor
from ecs.world import World

import libmice.common.components
import libmice.common.resources

# flake8: noqa
import libmice.common.systems

from libmice.autoregister import (
    ComponentRepository,
    SystemsRepository,
    ResourceRepository,
)

from mice.world_builder import WorldBuilder


class Game:

    TIMER_RES = "timer"
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
        wb.add_resource(
            self.WINDOW_RES, [pygame_plugin.components.Window(ws[0], ws[1])]
        )
        print("Registering components...")
        for rn, rc in ResourceRepository.resources:
            print(f"Registering resource {rn}")
            wb.add_resource(rn, rc)

    def _add_common_components(self, wb: WorldBuilder):
        for c in ComponentRepository.components:
            print(f"Registering component {c.__name__}")
            wb.add_component(c)

    def _add_common_systems(self, wb: WorldBuilder):
        wb.add_system(pygame_plugin.systems.DrawWindow(self.WINDOW_RES), add_front=True)
        print("g systems...")
        for s in SystemsRepository.systems:
            print(f"Registering system {s.__class__.__name__}")
            wb.add_system(s)

    def start(self):
        if self._world is None:
            raise RuntimeError("World has not been yet initialized")
        self._world.start()
