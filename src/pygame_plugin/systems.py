from typing import Sequence, Mapping, Any

from ecs.system import GeneratorSystem, RunningSystem
from ecs.executor.policy import defer
from mice_common.components import Transform
from mice_common.autoregister import register

import sys
import pygame

from pygame_plugin.components import Image


@register
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
            window.display.fill((0, 0, 0))
            yield defer
            pygame.display.flip()
            yield None


@register
class DrawImages(GeneratorSystem):

    window_name: str
    default_args: Sequence[str] = ["WINDOW"]
    default_kwargs: Mapping[str, Any] = {}

    def __init__(self, window_name: str):
        super().__init__()
        self.window_name = window_name

    def __iter__(self) -> RunningSystem:
        [window] = self.resources[self.window_name].components
        yield None
        while True:
            drawable = zip(self.entity_storage[Image], self.entity_storage[Transform])
            drawable = filter(all, drawable)
            for img, trans in drawable:
                img.rect.center = (trans.x, trans.y)  # type: ignore
                window.display.blit(img.img, img.rect)  # type: ignore
            yield None
