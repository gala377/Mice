import sys
import pygame

from typing import Sequence, Mapping, Any

from ecs.system import GeneratorSystem, RunningSystem
from ecs.executor.policy import defer
from libmice.common.components import Transform
from libmice.autoregister import register

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



