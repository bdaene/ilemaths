
# See subject at https://www.ilemaths.net/sujet-hache-menu-864981.html

from math import gcd

with open('pi.txt') as pi_file:
    pi_decimals = tuple(map(int, pi_file.readline()[2:-1]))


def get_nb_axes(t):
    n = 0
    while (t+n+1) % (2*pi_decimals[n]+1) != 0:
        n += 1
    return n


def main():
    decimals = pi_decimals[:pi_decimals.index(0)]

    allowed_times, mod = {0}, 1
    for decimal in range(1, 10):
        m = decimal * 2 + 1
        forbidden_times = set(-i % m for i, d_ in enumerate(decimals, 1) if d_ == decimal)

        d = gcd(m, mod)
        allowed_times = set(time + i*mod for time in allowed_times for i in range(m//d) if (time + i*mod) % m not in forbidden_times)
        mod *= m//d
        print(mod, allowed_times)

    print(mod, min(allowed_times), len(allowed_times))
    print(sorted(allowed_times)[:20])


if __name__ == "__main__":
    main()
