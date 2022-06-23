# See https://www.ilemaths.net/sujet-fractions-egyptiennes-880929.html

from fractions import Fraction
from math import ceil


def solve(ds, splits):
    ds_ = sorted(ds)
    yield ds_
    for d in reversed(ds_):
        ds.remove(d)
        for split in splits.get(d, set()):
            if ds.isdisjoint(split):
                yield from solve(ds | split, splits)
        ds.add(d)


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
    splits = {d: sorted((split for split in gen_splits(Fraction(1, d), max_splits, d + 1, max_denominator)),
                        key=lambda s: sorted(s, reverse=True))
              for d in range(1, max_denominator // 2 + 1)}
    print(sum(map(len, splits.values())))

    best = 0
    for solution in solve({1}, splits):
        if len(solution) > best:
            best = len(solution)
            print(f"{best:2} {solution}")


if __name__ == "__main__":
    main()
