from typing import (
    ClassVar,
    Union,
    Type,
    Sequence,
    Iterator,
)

from ecs.component import Component
from ecs.system import SimpleSystem

from libmice.systems.query import (
    _Predicate,
    QueryBuilder,
    Query,
)


_QueryItem = Union[Type[Component], _Predicate]


class AbstractSystem(SimpleSystem):
    """
    Designated base class for system classes.

    `AbstractSystem` class builds on top of a `SimpleSystem`
    class from the mices `ecs` package without changing its
    interface. That means that `create`, `start` and `update`
    methods can still be overloaded without calling `super` methods.

    `AbstractSystem` is query-aware extension. It builds component iterator
    from the `query` class variable, which is then available
    from `components` property.

    The goal is to allow simple systems to iterate over components
    they are interested in without directly interacting with the
    entity storage.
    """

    query: ClassVar[Sequence[_QueryItem]]

    __query: Query

    def _init(self, storage, resources):
        """
        Builds query object before invoking `super`.

        This function is overloaded instead of `create` so that
        the user won't have to make super call at the start of
        his own overload.
        """
        qb = QueryBuilder()
        for p in self.query:
            qb.add(p)
        self.__query = qb.build()
        super()._init(storage, resources)

    @property
    def components(self) -> Iterator[Sequence[Component]]:
        return self.__query.execute(self.entity_storage)


class _Meta(type):
    def __getitem__(self, *predicates) -> Type:
        if isinstance(predicates[0], Sequence):
            predicates = predicates[0]

        class AnonSystem(AbstractSystem):
            print(f"Predicates are {predicates}")
            query = predicates

        return AnonSystem


class System(metaclass=_Meta):
    """
    AbstractSystem class factory providing alternative interface
    to setting `query` class variable.

    AbstractSystem:
    ```
    class A(AbstractSystem):
        query = (A, B, C)
    ```
    
    System:
    ```
    class A(System[A, B, C]):
        ...
    ```
    """

    ...
