from typing import (
    Tuple,
    Sequence,
)

from mice import system
from mice.common.components import Transform, Time


@system()
class MoveBall:

    speed: Tuple[float, float]
    default_args: Sequence[Tuple[float, float]] = [(600, 500)]

    def __init__(self, speed: Tuple[float, float]):
        self.speed = speed
        self.width = 720
        self.height = 480
        self._speed = list(speed)

    def create(self):
        self.pos = self.resources.ball[Transform]
        self.timer = self.resources.timer[Time]

    def update(self):
        self.pos.x += self._speed[0] * self.timer.delta
        self.pos.y += self._speed[1] * self.timer.delta
        if self.pos.x < 0 or self.pos.x > self.width:
            self._speed[0] = -self._speed[0]
        if self.pos.y < 0 or self.pos.y > self.height:
            self._speed[1] = -self._speed[1]
        yield None
