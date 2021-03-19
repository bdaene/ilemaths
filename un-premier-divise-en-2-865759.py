
# See subject at https://www.ilemaths.net/sujet-un-premier-divise-en-2-865759.html

from primes import is_probable_prime, gen_primes_under
from itertools import product


def solve(nb_digits):
    p1 = 10**nb_digits-1
    while not is_probable_prime(p1):
        p1 -= 2
    prefix = p1 * 10**nb_digits
    p2 = 10**nb_digits-1
    while not is_probable_prime(p2) or not is_probable_prime(prefix + p2):
        p2 -= 2
    return prefix + p2


def solve2(nb_digits):
    primes = list(p for p in gen_primes_under(10**nb_digits) if p > 10**(nb_digits-1))
    for p1 in reversed(primes):
        prefix = p1 * 10**nb_digits
        for p2 in reversed(primes):
            if is_probable_prime(prefix + p2):
                yield prefix + p2


def main():
    print(solve(5))
    print(solve(10))

    print(len(list(solve2(5))))


if __name__ == "__main__":
    main()
