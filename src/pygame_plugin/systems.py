from ecs.system import GeneratorSystem, RunningSystem
from ecs.executor.policy import defer
from mice_common.components import Transform

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

    window_name: str

    def __init__(self, window_name: str):
        super().__init__()
        self.window_name = window_name

    def __iter__(self) -> RunningSystem:
        [window] = self.resources[self.window_name].components
        yield None
        while True:
            print("Filling")
            window.display.fill((255, 0, 0))
            yield defer
            pygame.display.flip()
            print("Flipping")
            yield None


class DrawImages(GeneratorSystem):

    window_name: str

    def __init__(self, window_name: str):
        super().__init__()
        self.window_name = window_name

    def __iter__(self) -> RunningSystem:
        [window] = self.resources[self.window_name].components
        yield None
        while True:
            print("Drawing")
            drawable = zip(self.entity_storage[Image], self.entity_storage[Transform])
            drawable = [d for d in drawable]  # type: ignore
            print(f"Drawables {drawable}")
            drawable = filter(all, drawable)
            drawable = [d for d in drawable]  # type: ignore
            print(f"Drawables after filter {drawable}")
            for img, trans in drawable:
                print("Drawing image...")
                img.rect.center = (trans.x, trans.y)  # type: ignore
                window.display.blit(img.img, img.rect)  # type: ignore
            yield None
