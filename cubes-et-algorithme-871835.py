
# https://www.ilemaths.net/sujet-cubes-et-algorithme-871835.html

from heapq import heappop, heappush
import sys
from functools import cache
from bisect import bisect
from collections import defaultdict


def solve(n, k):

    powers = [0]
    while powers[-1] < n:
        powers.append(len(powers)**k)
    powers_ = set(powers)

    @cache
    def get_cost(remainder):
        return 0 if remainder == 0 else 1 if remainder in powers_ else 2

    # Nodes are (cost, remainder, terms)
    heap = [(get_cost(n), n, ())]
    while heap:
        _, n, terms = heappop(heap)
        if n == 0:
            # If there is no remainder, we found the solution.
            yield terms
            return

        m = bisect(powers, n) - 1   # Maximum term
        if terms:
            # Do not look twice for the same solution.
            m = min(m, terms[-1])

        for i in range(1, m+1):
            r = n-i**k
            heappush(heap, (len(terms)+1+get_cost(r), r, terms + (i,)))


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
    for terms in solve3(n, k):
        print(' + '.join(f'{term}^{k}' for term in terms) + f' = {sum(term**k for term in terms)}')


if __name__ == "__main__":
    main()
