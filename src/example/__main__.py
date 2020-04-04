from typing import Tuple, Sequence

from mice import Game, WorldBuilder
from ecs.system import GeneratorSystem
from pygame_plugin.components import Image
from mice_common.components import Transform

# flake8: noqa
import example.systems

from example.resources import add_resources
from mice_common.autoregister import register


@register
class MoveBall(GeneratorSystem):

    speed: Tuple[float, float]

    default_args: Sequence[Tuple[float, float]] = [(500, 500)]

    def __init__(self, speed: Tuple[float, float]):
        self.speed = speed

    def __iter__(self):
        ball = self.resources["BALL"]
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
    w.add_resource("BALL", [Image("resources/intro_ball.gif"), Transform(0, 0)])

    add_resources(w)
    game = Game(w, (720, 480))
    game.start()


if __name__ == "__main__":
    main()
