# See https://www.ilemaths.net/sujet-fractions-egyptiennes-880929.html

from fractions import Fraction
from math import ceil

seen = set()


def solve(ds, splits):
    ds_ = sorted(ds)
    if tuple(ds_) in seen:
        return
    else:
        seen.add(tuple(ds_))
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
    for n, splits_ in splits.items():
        if splits_:
            print(f"{n}: " + ", ".join(sorted((f"{sorted(split)}" for split in splits_), key=lambda s: (len(s), s))))
    print(sum(map(len, splits.values())))

    solutions = []
    best = 0
    for solution in solve({2, 3, 6}, splits):
        length = len(solution)
        solutions = solutions[:length]
        solutions += [None] * (length - len(solutions))
        solutions.append(solution)
        if length >= best:
            best = length
            print(f"{best:2} {solution}")
            # for n, s in enumerate(solutions[1:], 1):
            #     print(f"{n:2} {s}")


if __name__ == "__main__":
    main()
