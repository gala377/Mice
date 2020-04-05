from typing import (
    Any,
    MutableSet,
    Optional,
    List,
    Iterator,
    Callable,
)

from dataclasses import dataclass


@dataclass
class GenId:

    id: int = 0
    gen: int = 0


@dataclass
class GenIdArrayEntry:

    val: Optional[Any]
    gen: int


@dataclass
class AllocatorEntry:

    is_alive: bool = False
    gen: int = 0


class AllocationError(Exception):
    ...


class NotEnoughSpace(AllocationError):
    ...


class Allocator:

    allocated: List[AllocatorEntry]
    free_ids: MutableSet[int]

    SCALE_FACTOR: float = 1.3

    def __init__(self, *, capacity=2):
        self.free_ids = {i for i in range(capacity)}
        self.allocated = [AllocatorEntry() for i in range(capacity)]

    def allocate(self) -> GenId:
        try:
            idx = self.free_ids.pop()
            gen_id = self.allocated[idx]
            gen_id.gen += 1
            gen_id.is_alive = True
            return GenId(idx, gen_id.gen)
        except KeyError:
            raise NotEnoughSpace

    def deallocate(self, id: GenId):
        try:
            entry = self._entry(id)
            entry.is_alive = False
            self.free_ids.add(id.id)
        except KeyError:
            return

    def is_valid(self, id: GenId) -> bool:
        try:
            self._entry(id)
            return True
        except KeyError:
            return False

    def valid_ids(self) -> Iterator[GenId]:
        yield from (
            GenId(i, entry.gen)
            for i, entry in enumerate(self.allocated)
            if entry.is_alive
        )

    def autoresize(self) -> int:
        old_size = len(self.allocated)
        new_size = int(old_size * self.SCALE_FACTOR)
        for i in range(old_size, new_size):
            self.allocated.append(AllocatorEntry())
            self.free_ids.add(i)
        return new_size - old_size

    def _entry(self, id: GenId) -> AllocatorEntry:
        if id.id in self.free_ids:
            raise KeyError("Entry is in free ids")
        if id.id >= len(self.allocated):
            raise KeyError("Index is higher than the allocated space")
        entry = self.allocated[id.id]
        if entry.gen != id.gen:
            raise KeyError("Generations doesn't match")
        return entry

    def __len__(self) -> int:
        return len(self.allocated)


def resize_by(it: List[Any], val: Callable[[], Any], scale_factor: float):
    new_size = int(len(it) * scale_factor)
    for i in range(len(it), new_size):
        it.append(val())
