# See https://www.ilemaths.net/sujet-triangles-rectanles-semblabes-888012.html

from sympy import Symbol, I, solve, im, re


def main():
    # ax, bx, cx = Symbol('ax', real=True), Symbol('bx', real=True), Symbol('cx', real=True)
    # ay, by, cy = Symbol('ay', real=True), Symbol('by', real=True), Symbol('cy', real=True)
    # a, b, c = ax + I * ay, bx + I * by, cx + I * cy

    a, b, c = Symbol('a', complex=True), Symbol('b', complex=True), Symbol('c', complex=True)

    print([a, b, c])

    d = (c - I * (a - c)).simplify()
    e = (a + I * (c - a)).simplify()
    h = (a - I * (b - a)).simplify()
    i = (b + I * (a - b)).simplify()
    m = (b - I * (c - b)).simplify()
    n = (c + I * (b - c)).simplify()

    print([d, e, h, i, m, n])

    f = (e - I * (h - e)).simplify()
    g = (h + I * (e - h)).simplify()
    k = (i - I * (m - i)).simplify()
    l = (m + I * (i - m)).simplify()
    p = (n - I * (d - n)).simplify()
    q = (d + I * (n - d)).simplify()

    print([f, g, k, l, p, q])

    u, v, w = Symbol('u', real=True), Symbol('v', real=True), Symbol('w', real=True)
    lp = ((p + l) / 2 + u * (p - l) / 4).simplify()
    qf = ((q + f) / 2 + v * (f - q) / 4).simplify()
    gk = ((g + k) / 2 + w * (k - g) / 4).simplify()

    print([lp, qf, gk])


if __name__ == "__main__":
    main()
