import sys
import pygame

from typing import Sequence, Mapping, Any

from ecs.system import GeneratorSystem, RunningSystem
from ecs.executor.policy import defer
from libmice.common.components import Transform
from libmice.autoregister import register

from pygame_plugin.components import Image



class DrawWindow(GeneratorSystem):

    window_name: str

    def __init__(self, window_name: str):
        super().__init__()
        self.window_name = window_name

    def __iter__(self) -> RunningSystem:
        [window] = self.resources[self.window_name].components
        yield None
        while True:
            window.display.fill((0, 0, 0))
            yield defer
            pygame.display.flip()
            yield None
