from ecs.world import World
from ecs import systems


def main():
    w = World()
    w.register(systems.HelloWorld(1))
    w.register(systems.WaitAsync(5.0))
    w.register(systems.Wait(1.0))
    w.start()


if __name__ == "__main__":
    main()
