# See https://www.ilemaths.net/sujet-une-grande-famille-de-couples-888054.html

import heapq
from itertools import count, islice
from math import gcd


def gen_primes():
    """Generate an ordered infinite sequence of prime numbers."""
    composites = {}
    for n in count(2):
        if n not in composites:
            yield n
            composites[n * n] = [n]
        else:
            for p in composites[n]:
                composites.setdefault(n + p, []).append(p)
            del composites[n]


def gen_prime_powers():
    """Generate an ordered infinite sequence of prime powers."""
    powers = []
    primes = gen_primes()
    while True:
        next_prime = next(primes)

        while powers and powers[0][0] < next_prime:
            power, prime = powers[0]
            yield power
            heapq.heappushpop(powers, (power * prime, prime))

        heapq.heappush(powers, (next_prime, next_prime))


def find_y(x):
    for (a, b) in gen_proper_divisors(x):
        for (c, d) in gen_proper_divisors(x + 1):
            ad, bc = a * d, b * c
            # (y+1) - y = m(ad) - n(bc) = 1
            d, m, n = gcde(ad, -bc)
            yield (d * n * bc) % (ad * bc)


def gen_proper_divisors(x):
    for d in range(2, int(x ** .5) + 1):
        d_, r = divmod(x, d)
        if r == 0 and gcd(d, d_) == 1:
            yield d, d_
            yield d_, d


def gcde(a, b):
    if a == 0:
        return b, 0, 1
    else:
        d, x, y = gcde(b % a, a)
        return d, y - (b // a) * x, x


def solve():
    last_power = 1

    for power in gen_prime_powers():
        for x in range(last_power + 1, power - 1):
            for y in sorted(find_y(x)):
                yield x, y

        last_power = power


def solve_brute_force():
    for x in count():
        for y in range(x * (x + 1)):
            if (
                    y * (y + 1) % (x * (x + 1)) == 0
                    and y % x != 0
                    and y % (x + 1) != 0
                    and (y + 1) % (x + 1) != 0
                    and (y + 1) % x != 0
            ):
                yield x, y


def verify():
    solutions_brute_force = solve_brute_force()
    solutions = solve()

    for solution_brute_force, solution in zip(solutions_brute_force, solutions):
        print(solution_brute_force, solution)
        if solution_brute_force != solution:
            break


def main():
    for solution in islice(solve(), 1000):
        print(solution)


if __name__ == "__main__":
    main()
