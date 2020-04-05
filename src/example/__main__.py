from typing import Tuple, Sequence

from mice import Game, WorldBuilder, register
from mice.system_helpers import SimpleSystem
from mice.components import Image, Transform

# flake8: noqa
import example.systems
import example.resources


@register
class MoveBall(SimpleSystem):
    speed: Tuple[float, float]

    default_args: Sequence[Tuple[float, float]] = [(500, 500)]

    def __init__(self, speed: Tuple[float, float]):
        self.speed = speed
        self.width = 720
        self.height = 480
        self._speed = list(speed)

    def start(self):
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


def main():
    w = WorldBuilder()
    game = Game(w, (720, 480))
    game.start()


if __name__ == "__main__":
    main()
