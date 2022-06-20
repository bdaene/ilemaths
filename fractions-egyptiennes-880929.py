# See https://www.ilemaths.net/sujet-fractions-egyptiennes-880929.html

from fractions import Fraction
from heapq import heappop, heappush
from math import ceil

from primes import gen_primes_under

MAX_DENOMINATOR = 24 + 1
PRIMES = set(gen_primes_under(MAX_DENOMINATOR))
LENGTH = 10 + 1


def solve(ds, splits):
    heap = [(-len(ds), max(ds), ds)]

    while heap:
        _, _, ds = heappop(heap)
        yield sorted(ds)
        for d in ds:
            for split in splits.get(d, set()):
                if ds.isdisjoint(split):
                    ds_ = ds - {d} | split
                    heappush(heap, (-len(ds_), max(ds_), ds_))


def gen_splits(fraction, max_splits, min_d, max_d):
    if fraction == 0:
        yield frozenset()
        return

    if max_splits < 1:
        return

    for d in range(max(min_d, ceil(1 / fraction)), max_d + 1):
        for split in gen_splits(fraction - Fraction(1, d), max_splits - 1, d + 1, max_d):
            yield split | {d}


def main():
    max_denominator = 99
    max_splits = 3
    splits = {d: set(split for split in gen_splits(Fraction(1, d), max_splits, d + 1, max_denominator))
              for d in range(1, max_denominator // 2)}

    best = 0
    for solution in solve({1}, splits):
        if len(solution) > best:
            best = len(solution)
            print(f"{best:2} {solution}")


if __name__ == "__main__":
    main()
