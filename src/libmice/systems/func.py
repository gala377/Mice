from typing import Type
from libmice import autoregister


import ecs
import libmice


def system(*predicates: Type, register=True):
    if len(predicates) == 1 and issubclass(predicates[0], ecs.system.System):
        if register:
            return autoregister.system(predicates[0])
        else:
            return False
    if len(predicates) == 0:
        return resource_system(register)

    def wrap(cls: Type):
        class Anon(cls, libmice.systems.abc.System[predicates]):  # typing: ignore
            ...

        Anon.__name__ = cls.__name__
        Anon.__doc__ = cls.__doc__
        Anon.__qualname__ = cls.__qualname__
        if register:
            cls = autoregister.system(Anon)
        return cls

    return wrap


def resource_system(cls, register=True):
    if not isinstance(register, bool):
        print("resource_system without bool")

        class Anon(cls, ecs.system.SimpleSystem):
            ...

        Anon.__name__ = cls.__name__
        Anon.__doc__ = cls.__doc__
        Anon.__qualname__ = cls.__qualname__

        autoregister.system(Anon)
        return Anon

    print("resource system with bool")

    def wrapper(cls):
        class Anon(cls, ecs.system.SimpleSystem):
            ...

        Anon.__name__ = cls.__name__
        Anon.__doc__ = cls.__doc__
        Anon.__qualname__ = cls.__qualname__
        if register:
            autoregister.system(Anon)
        return Anon

    return wrapper
