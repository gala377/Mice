import pytest

from libmice.systems.query import (
    not_none,
    is_none,
    with_none,
    Query,
)


class A:
    ...

class B:
    ...

class C:
    ...


@pytest.fixture
def storage():
    return {
        A: [1, 2, 3, None, 5, None, 7],
        B: [1, None, 3, None, 5, 6, 7],
        C: [1, 2, 3, 4, 5, 6, 7],
    }


@pytest.mark.parametrize("key", [A, B])
def test_with_none_predicate_for_single_class(storage, key):
    out = [x for x in Query(with_none(key)).execute(storage)]
    assert out == storage[key]


def test_with_none_predicate_for_multiple_classes(storage):
    out = [x for x in Query(with_none(A), with_none(B)).execute(storage)]
    exp = [x for x in zip(storage[A], storage[B])]
    assert out == exp


@pytest.mark.parametrize("key", [A, B])
def test_not_none_predicate_for_single_class(storage, key):
    it = [x for x in Query(not_none(key)).execute(storage)]
    exp = [x for x in filter(lambda x: x is not None, storage[key])]
    assert it == exp


def test_not_none_predicate_for_multiple_classes(storage):
    out = [x for x in Query(not_none(A), not_none(B)).execute(storage)]
    exp = [x for x in filter(all, zip(storage[A], storage[B]))]
    assert out == exp


@pytest.mark.parametrize("key", [A, B])
def test_is_none_predicate_for_single_class(storage, key):
    out = [x for x in Query(is_none(key)).execute(storage)]
    exp = [x for x in filter(lambda x: x is None, storage[key])]
    assert out == exp


def test_is_none_predicate_for_multiple_classes(storage):
    out = [x for x in Query(is_none(A), is_none(B)).execute(storage)]
    exp = [
        x for x in filter(
            lambda x: x[0] is None and x[1] is None, zip(storage[A], storage[B])
        )]
    assert out == exp


def test_not_none_with_none_predicate_comb(storage):
    out = [x for x in Query(not_none(A), with_none(B)).execute(storage)]
    exp = [x for x in filter(lambda x: x[0] is not None, zip(storage[A], storage[B]))]
    assert out == exp


def test_multiple_predicates_query_result_is_flat(storage):
    out = [
        x for x in Query(
            with_none(A),
            with_none(B),
            with_none(C)
        ).execute(storage)
    ]
    exp = [x for x in zip(storage[A], storage[B], storage[C])]
    assert out == exp