from ecs.world import World
from ecs import systems
from ecs.executor import SimpleExecutor
from ecs.entity import SOAStorage


def main():
    w = World(storage=SOAStorage())

    w.register(systems.HelloWorld(1))
    w.register(systems.Wait(1.0))
    w.register(systems.WaitAsync(5.0))

    w.register_executor(SimpleExecutor)

    w.start()


if __name__ == "__main__":
    main()
