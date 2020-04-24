from typing import Type
from libmice import autoregister


import ecs
import libmice


def system(*predicates: Type):
    if len(predicates) == 1 and issubclass(predicates[0], ecs.system.System):
        return autoregister.system(predicates[0])

    def wrap(cls: Type):
        class Anon(cls, libmice.systems.abc.System[predicates]):  # typing: ignore
            ...

        Anon.__name__ = cls.__name__
        Anon.__doc__ = cls.__doc__
        Anon.__qualname__ = cls.__qualname__
        cls = autoregister.system(Anon)
        return cls

    return wrap


def resource_system(cls: Type):
    class Anon(cls, ecs.system.SimpleSystem):
        ...

    Anon.__name__ = cls.__name__
    Anon.__doc__ = cls.__doc__
    Anon.__qualname__ = cls.__qualname__
    cls = autoregister.system(Anon)
    return cls
