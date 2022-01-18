
# https://www.ilemaths.net/sujet-cubes-et-algorithme-871835.html

from bisect import bisect_left, bisect_right
from collections import defaultdict
from heapq import heappop, heappush


def solve(n, k):

    powers = []
    i = 0
    while (p := i**k) <= n:
        powers.append(p)
        i += 1

    # Nodes are (cost, remainder, -terms)
    heap: list[tuple[int, int, tuple[int, ...]]]
    heap = [(1, n, ())]
    best = 9
    while heap:
        # print(heap)
        cost, n, terms = heappop(heap)
        if cost > best:
            return

        if n == 0:
            best = cost
            # If there is no remainder, we found a solution.
            yield tuple(-term for term in terms)
            continue

        min_term = bisect_left(powers, (n/(best - len(terms))))
        max_term = bisect_right(powers, n)
        if terms:
            max_term = min(max_term, 1-terms[-1])
        for term, power in enumerate(powers[min_term:max_term], min_term):
            cost = len(terms) + (n+power-1)//power
            heappush(heap, (cost, n - power, terms + (-term,)))


def solve2(n, k):
    # Find all solutions with a number of terms of 4 or less
    sums = {}
    i = 0
    while (ik := i**k) <= n:
        j = 0
        while (jk := j**k) <= n - ik and j <= i:
            sums[ik + jk] = (i, j)
            j += 1
        i += 1
    print(len(sums))
    for s in sums:
        if n-s in sums:
            yield sorted(sums[s] + sums[n-s], reverse=True)


def solve3(n, k):
    # Find all solutions with a number of terms of 4 or less for k == 3 and n % 63 == 60
    assert k == 3
    assert n % 63 == 60

    max_term = int(n**(1/3) * 1.00000001)

    powers = defaultdict(dict)
    for i in range(max_term):
        p = i ** k
        powers[p % 63][p] = (i,)

    for a, b, c, d in ((36, 8, 8, 8), (0, 62, 62, 62), (27, 35, 62, 62)):
        print(a, b, c, d)
        s = {p_c + p_d: i_c + i_d for p_c, i_c in powers[c].items() for p_d, i_d in powers[d].items()}
        print(len(s))
        for p_a, i_a in powers[a].items():
            for p_b, i_b in powers[b].items():
                if n - p_a - p_b in s:
                    yield i_a + i_b + s[n - p_a - p_b]


def main():
    n = int(input("Entrez un nombre: "))
    k = 3
    for terms in solve(n, k):
        print(' + '.join(f'{term}^{k}' for term in terms) + f' = {sum(term**k for term in terms)}')


if __name__ == "__main__":
    main()
