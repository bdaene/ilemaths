# See https://www.ilemaths.net/sujet-sorcieres-mathematiciennes-888294.html

from collections import defaultdict
from functools import cache


def gen_sums(n, m=1):
    """Generate all the tuples with sum n (and min element m)."""
    if m > n:
        return

    for c in range(m, n // 2 + 1):
        for cs in gen_sums(n - c, c):
            yield (c,) + cs

    yield (n,)


def product(cats):
    p = 1
    for cat in cats:
        p *= cat
    return p


def get_signature(cats, max_exp=2):
    return (product(cats),) + tuple(sum(cat ** e for cat in cats) for e in range(max_exp + 1))


@cache
def get_solutions(bus, max_exp=2):
    """Get all solutions for a given bus number.

    The signature tuple (age=product, count=count, bus=sum, dragons=sum of square, ...) is solution if there are
    multiple cats that match this signature.
    """
    sorted_cats = defaultdict(list)
    for cats in gen_sums(bus):
        sorted_cats[get_signature(cats, max_exp=max_exp)].append(cats)

    return {s: cs for s, cs in sorted_cats.items()
            if len(cs) > 1}


def bisect(predicate, low=1, high=None):
    """Find the first index where the predicate is True.

    It is assumed that the predicate is False for indexes < index and True for indexes >= index.
    """
    assert not predicate(low)
    if high is None:
        high = low * 2
        while not (predicate(high)):
            high *= 2

    while low + 1 < high:
        mid = (low + high) // 2
        if predicate(mid):
            high = mid
        else:
            low = mid

    return high


def solve(max_exp=2):
    """The bus number is the one where exactly one solution exists."""
    min_bus = bisect(lambda bus: len(get_solutions(bus, max_exp=max_exp)) >= 1)
    max_bus = bisect(lambda bus: len(get_solutions(bus, max_exp=max_exp)) >= 2)

    for bus in range(min_bus, max_bus):
        yield get_solutions(bus, max_exp=max_exp)


if __name__ == "__main__":
    for solutions in solve(max_exp=2):
        print(solutions)
