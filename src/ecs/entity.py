import weakref

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import (
    Type,
    Sequence,
    Optional,
    MutableMapping,
    MutableSequence,
)

from ecs.component import Component
from ecs.genid import GenId, Allocator, NotEnoughSpace


@dataclass
class Entity:

    id: GenId
    components: Sequence[Component]
    _storage: weakref.ReferenceType  # Storage weakref

    def __del__(self):
        if self._storage() is not None:
            self._storage().remove_entity(self.id)  # type: ignore


class Storage(ABC):
    @abstractmethod
    def register(self, comp: Type[Component]):
        ...

    @abstractmethod
    def get_entity(self, id: GenId) -> Optional[Entity]:
        ...

    @abstractmethod
    def get_component(self, comp: Type[Component]) -> Sequence[Optional[Component]]:
        ...

    @abstractmethod
    def create_entity(self, comp: Sequence[Component]) -> Entity:
        ...

    @abstractmethod
    def remove_entity(self, id: GenId):
        ...

    def __getitem__(self, comp: Type[Component]) -> Sequence[Optional[Component]]:
        return self.get_component(comp)


class SOAStorage(Storage):

    components: MutableMapping[Type[Component], MutableSequence[Optional[Component]]]
    allocator: Allocator

    INITIAL_CAPACITY: int = 10

    def __init__(self):
        self.components = {}
        self.allocator = Allocator(capacity=self.INITIAL_CAPACITY)

    def register(self, comp: Type[Component]):
        if comp in self.components:
            return
        self.components[comp] = [None] * self.INITIAL_CAPACITY

    def create_entity(self, comps: Sequence[Component]) -> Entity:
        try:
            idx = self.allocator.allocate()
            for c in comps:
                self.components[type(c)][idx.id] = c
            entity = self.get_entity(idx)
            if entity is None:
                raise RuntimeError("Couldn't fetch just allocated entity")
            return entity
        except NotEnoughSpace:
            resized_by = self.allocator.autoresize()
            print(f"Resized by {resized_by}")
            self._resize_components_arrays(resized_by)
            return self.create_entity(comps)

    def remove_entity(self, id: GenId):
        if self.allocator.is_valid(id):
            for _, array in self.components.items():
                array[id.id] = None
            self.allocator.deallocate(id)

    def get_entity(self, id: GenId) -> Optional[Entity]:
        if not self.allocator.is_valid(id):
            return None
        comps = [
            array[id.id]
            for _, array in self.components.items()
            if array[id.id] is not None
        ]
        return Entity(id, comps, weakref.ref(self))

    def get_component(self, comp: Type[Component]) -> Sequence[Optional[Component]]:
        comps = self.components.get(comp, [])
        comps = [comps[id.id] for id in self.allocator.valid_ids()]
        return comps

    def _resize_components_arrays(self, by: int = 1):
        for _, array in self.components.items():
            array.extend(None for _ in range(by))
