import sys
import pygame


from ecs.system import GeneratorSystem, RunningSystem
from libmice.autoregister import register


@register
class WindowEvents(GeneratorSystem):
    def __iter__(self) -> RunningSystem:
        yield None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            yield None
