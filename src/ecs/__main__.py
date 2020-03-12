from ecs.world import World
from ecs import systems
from ecs.executor import SimpleExecutor
from ecs.entity import SOAStorage


def main():
    sys_l = [systems.HelloWorld(1), systems.WaitAsync(5.0), systems.Wait(1.0)]
    sys_d = {s.__class__.__name__: s for s in sys_l}
    w = World(storage=SOAStorage(), systems=sys_d, executor=SimpleExecutor())
    w.start()


if __name__ == "__main__":
    main()
