from typing import Tuple

from ecs.world import World
from ecs.executor import SimpleExecutor
from ecs.entity import SOAStorage
from ecs.component import Transform, Time
from ecs.systems import UpdateTime
from ecs.system import GeneratorSystem

import pygame
import pygame_plugin


class MoveBall(GeneratorSystem):
    speed: Tuple[float, float]

    def __init__(self, speed: Tuple[float, float]):
        self.speed = speed

    def __iter__(self):
        ball = self.resources["BALL"]
        timer = self.resources["TIMER"]
        width = 720
        height = 480
        [pos] = filter(lambda x: isinstance(x, Transform), ball.components)
        [timer] = self.resources["TIMER"].components
        speed = list(self.speed)
        # print(f"GOT BALLS POSITION ITS {pos}")
        yield None
        while True:
            pos.x += speed[0] * timer.delta  # type: ignore
            pos.y += speed[1] * timer.delta  # type: ignore
            if pos.x < 0 or pos.x > width:
                speed[0] = -speed[0]
            if pos.y < 0 or pos.y > height:
                speed[1] = -speed[1]
            yield None


def main():
    w = World(storage=SOAStorage())

    w.register(pygame_plugin.systems.WindowEvents())
    w.register(pygame_plugin.systems.DrawWindow())
    w.register(pygame_plugin.systems.DrawImages())
    w.register(MoveBall((500, 200)))
    w.register(UpdateTime("TIMER"))

    w.register_component(pygame_plugin.components.Window)
    w.register_component(pygame_plugin.components.Image)
    w.register_component(Transform)
    w.register_component(Time)

    w.plug(lambda: pygame.init())

    w.register("WINDOW", [pygame_plugin.components.Window(720, 480)])
    w.register(
        "BALL",
        [pygame_plugin.components.Image("resources/intro_ball.gif"), Transform(0, 0)],
    )
    w.register(
        "TIMER", [Time()],
    )

    w.register_executor(SimpleExecutor)

    w.start()


if __name__ == "__main__":
    main()
