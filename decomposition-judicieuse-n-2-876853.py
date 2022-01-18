
# See subject at https://www.ilemaths.net/sujet-decomposition-judicieuse-n-2-876853.html


def solve(d, n):
    """Find the maximum of prod(a[k]/d) such that sum(a[k]) = n"""
    k, best = 1, None
    while True:
        # We decompose n in a sum of k+1 consecutive terms (from a to a+k) minus r = (a+i) for some i, 0 <= i < k.
        a = (2*(n+k-1) - k*(k+1))//(2*k)
        r = (k+1)*(2*a+k)//2 - n

        # product = math.factorial(a+k) // math.factorial(a-1) // r     # Not efficient because k << a
        product = 1
        for i in range(a, a+k+1):
            if i != r:
                product *= i

        if best is None or product >= best[0] * d ** (k - best[1]):
            best = (product, k, a, r)
        else:
            break

        k += 1

    return best


def main():
    print(f"{'d':>4} {'n':>6} {'k':>3} {'a':>5} {'r':>5} {'n/kd':>5} {'p/d^k':>13} {'p'}")
    for d, n in (
            (1, 10000),
            (5, 39),
            (6, 42),
            (5, 76),
            (5, 80),
            (100, 10000),
            (4000, 100000),
            (8, 2002),
            (80, 2002),
            (16, 80),
            (7, 50),
            (9, 75),
            (10, 90),
            (80, 4004),
            (105, 8000),
            (876, 999000),
            # (334, 2800000),   # Cannot convert (p / d ** k) in float
    ):
        p, k, a, r = solve(d, n)
        # print(k, a, r, p)
        print(f"{d:4} {n:6} {k:3} {a:5} {r:5} {n / (k * d):.3f} {p / d ** k:<13e} {p}")


if __name__ == "__main__":
    main()
