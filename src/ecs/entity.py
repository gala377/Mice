import weakref

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import (
    Union,
    NewType,
    Type,
    Sequence,
    Mapping,
    Optional,
)

from ecs.component import Component


@dataclass
class GenId:

    identifier: int = 0
    generation: int = 0


@dataclass
class Entity:

    id: GenId
    components: Sequence[Component]
    _storage: weakref.ProxyType  # Storage weakref

    def __del__(self):
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
    def get_component(self, comp: Type[Component]) -> Sequence[Type[Component]]:
        ...

    @abstractmethod
    def create_entity(self, comp: Sequence[Component]) -> Entity:
        ...

    @abstractmethod
    def remove_entity(self, id: GenId):
        ...


class SOAStorage(Storage):
    """
    TODO: Generational id reaasignment
    """

    components = Mapping[Type[Component], Sequence[Component]]

    def __init__(self):
        self.components = {}
        self.free_ids = set()
        self.last_id = 0

    def register(self, comp: Type[Component]):
        if comp in self.components:
            return
        self.components[comp] = []

    def create_entity(self, comps: Sequence[Component]) -> Entity:
        id = GenId(identifier=self.last_id)
        self.last_id += 1
        for comp in comps:
            self.components[comp].append(comp)

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
            return
        components = []
        for _, val in self.components.items():
            if len(val) < id.id:
                return
            components.append(val[id.id])
        return Entity(id, components)

    def get_component(self, comp: Type[Component]) -> Sequence[Component]:
        comps = self.components.get(comp, default=[])
        comps = [c for i, c in enumerate(comps) if i not in self.free_ids]
        return comps
