import pytest

from mice_common.system_helpers import (
    not_none,
    is_none,
    with_none,
    Query,
    _flatten,
)


class A: ...
class B: ...

@pytest.fixture
def storage():
    return {
        A: [1, 2, 3, None, 5, None, 7],
        B: [1, None, 3, None, 5, 6, 7],
    }


def test_flatten_doesnt_change_flat_list():
    x = [x for x in range(10)]
    fd = [e for e in _flatten(iter(x))]
    assert x == fd

def test_flatten_doesnt_change_flat_tuple():
    x = [x for x in range(10)]
    fd = [e for e in _flatten(iter(x))]
    assert x == fd

def test_flatten_on_embedded_collections():
    x = [[[[1], 2, 3], (4, 5, ([[6]]), 7)], 8]
    flattened = [x for x in _flatten(iter(x))]
    assert flattened == [1, 2, 3, 4, 5, 6, 7, 8]

def assert_lists_are_same(l_1, l_2):
    print(f"X is {l_1=}")
    assert len(l_1) == len(l_2)
    for x, y in zip(l_1, l_2):
        assert x == y

@pytest.mark.parametrize("key", [A, B])
def test_with_none_predicate_for_single_class(storage, key):
    out = [x for x in Query(with_none(key)).execute(storage)]
    assert_lists_are_same(out, storage[key])

def test_with_none_predicate_for_multiple_classes(storage):
    out = [x for x in Query(with_none(A), with_none(B)).execute(storage)]
    assert_lists_are_same(out, [x for x in zip(storage[A], storage[B])])

@pytest.mark.parametrize("key", [A, B])
def test_not_none_predicate_for_single_class(storage, key):
    it = [x for x in Query(not_none(key)).execute(storage)]
    assert_lists_are_same(it, [x for x in filter(lambda x: x is not None, storage[key])])

def test_not_none_predicate_for_multiple_classes(storage):
    out = [x for x in Query(not_none(A), not_none(B)).execute(storage)]
    assert_lists_are_same(out, [x for x in filter(all, zip(storage[A], storage[B]))])

@pytest.mark.parametrize("key", [A, B])
def test_is_none_predicate_for_single_class(storage, key):
    out = [x for x in Query(is_none(key)).execute(storage)]
    assert_lists_are_same(out, [x for x in filter(lambda x: x is None, storage[key])])

def test_is_none_predicate_for_multiple_classes(storage):
    out = [x for x in Query(is_none(A), is_none(B)).execute(storage)]
    assert_lists_are_same(
        out,
        [
            x for x in filter(
                lambda x: x[0] is None and x[1] is None,
                zip(storage[A], storage[B]))
        ])


def test_not_none_with_none_predicate_comb(storage):
    out = [x for x in Query(not_none(A), with_none(B)).execute(storage)]
    assert_lists_are_same(
        out,
        [
            x for x in filter(
                lambda x: x[0] is not None,
                zip(storage[A], storage[B]) )
        ])