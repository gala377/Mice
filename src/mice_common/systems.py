import time
from typing import TypeVar, Mapping, Sequence, Any
from ecs.system import (
    GeneratorSystem,
    IteratorSystem,
)
from ecs.executor.policy import AsyncWait

from mice_common.autoregister import register


@register
class UpdateTime(GeneratorSystem):

    res_name: str

    def __init__(self, res_name: str):
        super().__init__()
        self.res_name = res_name

    def __iter__(self):
        [timer] = self.resources[self.res_name].components
        timer.update()
        yield None
        while True:
            timer.update()
            yield None

    default_args: Sequence[Any] = ["timer"]
    default_kwargs: Mapping[str, Any] = {}


class Wait(IteratorSystem):

    wait_time: float

    def __init__(self, wait_time: float):
        self.wait_time = wait_time

    def __next__(self):
        print("Night night")
        time.sleep(self.wait_time)
        print("Waky waky")

    def close(self):
        ...


T = TypeVar("T")


def async_wait(wait_time: float, ret_val: T) -> T:
    time.sleep(wait_time)
    return ret_val


class WaitAsync(GeneratorSystem):

    wait_time: float

    def __init__(self, wait_time: float):
        self.wait_time = wait_time

    def __iter__(self):
        i = 0
        while True:
            print("Async nigh nigh")
            ret = yield AsyncWait(async_wait, self.wait_time, i)
            print(f"Async waky waky with value {ret}")
            i = ret + 1


class HelloWorld(GeneratorSystem):

    i: int

    def __init__(self, start_from=0):
        self.i = start_from

    def __iter__(self):
        while True:
            print(f"Hello this is my #{self.i} iteration!")
            self.i += 1
            yield

    default_args: Sequence[int] = [0]
    default_kwargs: Mapping[str, Any] = {}
