
# See subject at https://www.ilemaths.net/sujet-esperance-865365.html

from functools import cache
from math import comb
import sys

sys.setrecursionlimit(10000)


def solve(nb_coins):

    @cache
    def f_b(b, n):
        if b <= 0 or n <= 0:
            return 0
        return f_b(b-1, n) + comb(n+b-2, b-1) + f_b(n, b-1)

    @cache
    def f_n(b, n):
        if n <= 0 or b <= 0:
            return 0
        return f_n(b, n-1) + comb(n+b-2, n-1) + f_b(b, n-1)

    return 2 * f_b(nb_coins, nb_coins)


def main():
    n = 125
    count = solve(n)
    print(count, count/comb(2*n, n), count-n*comb(2*n, n))


if __name__ == "__main__":
    main()
