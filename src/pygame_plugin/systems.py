from ecs.system import GeneratorSystem, RunningSystem
from ecs.executor.policy import defer
from ecs.component import Transform

import sys
import pygame

from pygame_plugin.components import Image


class WindowEvents(GeneratorSystem):
    def __iter__(self) -> RunningSystem:
        yield None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            yield None


class DrawWindow(GeneratorSystem):
    def __iter__(self) -> RunningSystem:
        [window] = self.resources["WINDOW"].components
        yield None
        while True:
            window.display.fill((255, 0, 0))
            yield defer
            pygame.display.flip()
            yield None


class DrawImages(GeneratorSystem):
    def __iter__(self) -> RunningSystem:
        [window] = self.resources["WINDOW"].components
        yield None
        while True:
            drawable = zip(self.entity_storage[Image], self.entity_storage[Transform])
            drawable = filter(all, drawable)
            for img, trans in drawable:
                img.rect.center = (trans.x, trans.y)  # type: ignore
                window.display.blit(img.img, img.rect)  # type: ignore
            yield None
