import pygame

from typing import (
    Tuple,
    Sequence,
)

from mice import (
    Game,
    system,
    resource_system,
)
from mice.common.components import Transform

from example.components import (
    Grid,
    DebugView,
)


@resource_system
class MoveBall:

    speed: Tuple[float, float]
    default_args: Sequence[Tuple[float, float]] = [(500, 500)]

    def __init__(self, speed: Tuple[float, float]):
        self.speed = speed
        self.width = 720
        self.height = 480
        self._speed = list(speed)

    def create(self):
        ball = self.resources["ball"]
        [self.pos] = filter(lambda x: isinstance(x, Transform), ball.components)
        [self.timer] = self.resources[Game.TIMER_RES].components

    def update(self):
        self.pos.x += self._speed[0] * self.timer.delta
        self.pos.y += self._speed[1] * self.timer.delta
        if self.pos.x < 0 or self.pos.x > self.width:
            self._speed[0] = -self._speed[0]
        if self.pos.y < 0 or self.pos.y > self.height:
            self._speed[1] = -self._speed[1]
        yield None


@system(Grid, DebugView)
class GridView:

    window_name: str
    grid_name: str

    default_args = [Game.WINDOW_RES, "grid"]

    def __init__(self, wn: str, gn: str):
        super().__init__()
        self.window_name = wn
        self.grid_name = gn

    def create(self):
        [self.window] = self.resources[self.window_name].components

    def update(self):
        for grid, _ in self.components:
            for i in range((self.window.height // grid.size) + 1):
                pygame.draw.line(
                    self.window.display,
                    (0, 255, 0),
                    (0, i * grid.size),
                    (self.window.width, i * grid.size),
                )
            for i in range((self.window.width // grid.size) + 1):
                pygame.draw.line(
                    self.window.display,
                    (0, 0, 255),
                    (i * grid.size, 0),
                    (i * grid.size, self.window.height),
                )
        yield None
