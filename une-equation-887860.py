from math import log2

from matplotlib import pyplot


def find_roots(a):
    """Find solutions to x**2 + a = 0 (2**k)."""
    if a % 2 == 0:
        t = (a & -a).bit_length() - 1
        if t == 1:
            yield 1, 2, {0}
        else:
            t -= t%2
            for k, m, xs in find_roots(a >> t):
                yield k + t, m << t, {x << (t//2) for x in xs}

        return

    yield 0, 1, {0}
    if -a % 2 == 1:
        yield 1, 2, {1}
    else:
        return
    if -a % 4 == 1:
        yield 2, 4, {1, 3}

    k, m = 3, 8
    if -a % m != 1:
        return
    xs = {1, 3, 5, 7}

    while True:
        yield k, m, xs

        xs_ = set()
        k += 1
        m <<= 1

        for x in xs:
            n = (x ** 2 + a) >> (k - 1)
            if n & 1:
                continue
            xs_.add(x % m)
            xs_.add(-x % m)
            x *= (m >> 1) + 1
            x %= m
            xs_.add(x % m)
            xs_.add(-x % m)

        xs = xs_


def main(a=23, limit=1000):
    ns = []
    ms = []
    for k, m, xs in find_roots(a):
        for x in xs:
            n = x ** 2 + a
            if n == m:
                print(f"{x:>4}**2 + {a:>4} = 2**{k:>2}")
            # if n < (m >> 15) ** 2:
            # print(k, m, x, n)

            ns.append(log2(n))
            ms.append(log2(m))

        if k >= limit:
            break

    # pyplot.plot([1, ms[-1]], [1, ms[-1]], 'r', linewidth=0.5, label=f"$\\mathregular{{x^2+{a}=2^y}}$")
    # pyplot.plot([1, ms[-1]], [2, 2 * ms[-1]], 'r', linewidth=0.1, label=f"$\\mathregular{{x^2+{a}=2^{{2y}}}}$")
    # pyplot.scatter(ms, ns, s=0.5)
    # pyplot.xlabel(f"$\\mathregular{{y}}$")
    # pyplot.ylabel(f"$\\mathregular{{\\log_2(x^2+{a})}}$")
    # pyplot.legend()
    # pyplot.title(f"$\\mathregular{{x^2+{a} \\equiv 0  (2^y)}}$")


if __name__ == "__main__":
    for a in range(1, 5000):
        main(a)
    # pyplot.show()
