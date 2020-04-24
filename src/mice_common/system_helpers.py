from typing import (
    Sequence,
    Type,
    MutableSequence,
    Union,
    Any,
    Iterator,
    Iterable,
    Optional,
)
from abc import (
    abstractproperty,
    abstractmethod,
)
from dataclasses import dataclass

from ecs.entity import Storage
from ecs.component import Component


class _Predicate:
    @property
    @abstractproperty
    def comp(self) -> Type[Component]:
        ...

    @abstractmethod
    def filter_func(self, el: Optional[Component]) -> bool:
        ...


@dataclass
class with_none(_Predicate):

    _comp: Type[Component]

    @property
    def comp(self):
        return self._comp

    def filter_func(self, el):
        return True


@dataclass
class not_none(_Predicate):

    _comp: Type[Component]

    @property
    def comp(self):
        return self._comp

    def filter_func(self, el):
        return el is not None


@dataclass
class is_none(_Predicate):

    _comp: Type[Component]

    @property
    def comp(self):
        return self._comp

    def filter_func(self, el):
        return el is None


class Query:

    predicates: Union[Sequence[_Predicate], _Predicate]

    def __init__(self, *args):
        if len(args) == 1:
            [self.predicates] = args
        else:
            self.predicates = args

    def execute(self, storage: Storage) -> Iterator:
        if isinstance(self.predicates, Sequence):
            it = zip(*(storage[p.comp] for p in self.predicates))
            for i, p in enumerate(self.predicates):
                it = filter(lambda x, p=p, i=i: p.filter_func(x[i]), it)  # type: ignore
        else:
            it = filter(self.predicates.filter_func, storage[self.predicates.comp])  # type: ignore
        return it


class QueryBuilder:

    predicates: MutableSequence[_Predicate]

    def __init__(self):
        self.predicates = []

    def add(self, p: Union[_Predicate, Type[Component]]):
        if isinstance(p, _Predicate):
            self.predicates.append(p)
        else:
            self.predicates.append(with_none(p))

    def build(self) -> Query:
        if len(self.predicates) == 0:
            raise RuntimeError("Cannot build query from an empty set of predicates")
        return Query(*self.predicates)


def _flatten(it: Iterable[Any]) -> Iterator[Any]:
    for x in it:
        if isinstance(x, Iterable):
            yield from _flatten(x)
        else:
            yield x
