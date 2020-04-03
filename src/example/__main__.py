from typing import Tuple
from ecs.system import GeneratorSystem

from mice.game import Game
from mice.world_builder import WorldBuilder

from mice_common.components import Transform

from pygame_plugin.components import Image


class MoveBall(GeneratorSystem):

    speed: Tuple[float, float]

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
    w.add_system(MoveBall((250, 290)))
    game = Game(w, (720, 480))
    game.start()


if __name__ == "__main__":
    main()
