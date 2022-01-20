# https://www.ilemaths.net/sujet-et-si-fermat-avait-eu-tort-876941.html

import itertools


def gen_series(*start):
    for n in start:
        yield n

    n2, n1, n0 = start[-3:]
    while True:
        n0, n1, n2 = 82 * (n0 + n1) - n2, n0, n1
        yield n0


def main(nb_equations=None):
    a_series = gen_series(1, 135, 11161)
    b_series = gen_series(2, 138, 11468)
    c_series = gen_series(2, 172, 14258)
    d_series = gen_series(1, -1, 1)

    for a, b, c, d in itertools.islice(zip(a_series, b_series, c_series, d_series), nb_equations):
        assert a ** 3 + b ** 3 == c ** 3 + d
        print(f"{a}³+{b}³ = {c}³{d:+d}")


if __name__ == "__main__":
    main()
