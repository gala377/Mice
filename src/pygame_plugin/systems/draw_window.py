import pygame

from ecs.system import GeneratorSystem, RunningSystem
from ecs.executor.policy import defer

from pygame_plugin.components import Window


class DrawWindow(GeneratorSystem):
    def __iter__(self) -> RunningSystem:
        window = self.resources.window[Window]
        yield None
        while True:
            window.display.fill((0, 0, 0))
            yield defer
            pygame.display.flip()
            yield None
