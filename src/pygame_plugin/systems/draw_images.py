import sys
import pygame

from typing import Sequence, Mapping, Any

from ecs.system import GeneratorSystem, RunningSystem
from ecs.executor.policy import defer
from libmice.common.components import Transform
from libmice.autoregister import register

from pygame_plugin.components import Image


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
                img.rect.center = (trans.x, trans.y)
                window.display.blit(img.img, img.rect)
            yield None
