import weakref

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import (
    Union,
    Type,
    Sequence,
    Optional,
    MutableMapping,
    MutableSequence,
)

from ecs.component import Component


@dataclass
class GenId:

    id: int = 0
    gen: int = 0


@dataclass
class Entity:

    id: GenId
    components: Sequence[Component]
    _storage: weakref.ProxyType  # Storage weakref

    def __del__(self):
        if self._storage is not None:
            self._storage.remove_entity(self.id)


StorageKey = Union[GenId, Type[Component]]


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

    def __init__(self):
        self.components = {}
        self.free_ids = set()
        self.last_id = 0

    def register(self, comp: Type[Component]):
        if comp in self.components:
            return
        self.components[comp] = []

    def create_entity(self, comps: Sequence[Component]) -> Entity:
        id = GenId(id=self.last_id)
        self.last_id += 1
        for comp in comps:
            self.components[type(comp)].append(comp)
        print(
            f"Creating entity with componetnts {[map(lambda x: x.__class__.__name__, comps)]}"
        )
        lists_to_resize = [
            val for key, val in self.components.items() if key not in comps
        ]
        for val in lists_to_resize:
            val.append(None)

        return Entity(id, comps, weakref.proxy(self))

    def remove_entity(self, id: GenId):
        self.free_ids.add(id.id)

    def get_entity(self, id: GenId) -> Optional[Entity]:
        if id.id in self.free_ids:
            return None
        components: MutableSequence[Component] = []
        for _, val in self.components.items():
            if len(val) < id.id:
                return None
            comp = val[id.id]
            if comp is not None:
                components.append(comp)
        return Entity(id, components, weakref.proxy(self))

    def get_component(self, comp: Type[Component]) -> Sequence[Optional[Component]]:
        comps = self.components.get(comp, [])
        comps = [c for i, c in enumerate(comps) if i not in self.free_ids]
        return comps
