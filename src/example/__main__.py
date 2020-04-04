from typing import Tuple, Sequence

from mice import Game, WorldBuilder, register
from mice.system_helpers import GeneratorSystem
from mice.components import Image, Transform

# flake8: noqa
import example.systems
import example.resources


@register
class MoveBall(GeneratorSystem):

    speed: Tuple[float, float]

    default_args: Sequence[Tuple[float, float]] = [(500, 500)]

    def __init__(self, speed: Tuple[float, float]):
        self.speed = speed

    def __iter__(self):
        ball = self.resources["ball"]
        width = 720
        height = 480
        [pos] = filter(lambda x: isinstance(x, Transform), ball.components)
        [timer] = self.resources[Game.TIMER_RES].components
        speed = list(self.speed)
        # print(f"GOT BALLS POSITION ITS {pos}")
        yield None
        while True:
            pos.x += speed[0] * timer.delta
            pos.y += speed[1] * timer.delta
            if pos.x < 0 or pos.x > width:
                speed[0] = -speed[0]
            if pos.y < 0 or pos.y > height:
                speed[1] = -speed[1]
            yield None


def main():
    w = WorldBuilder()
    game = Game(w, (720, 480))
    game.start()


if __name__ == "__main__":
    main()