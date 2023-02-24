# See https://www.ilemaths.net/sujet-nombres-puissants-882341.html
import itertools
from heapq import heappop, heappush
from multiprocessing import Pool, TimeoutError

from factors import factorize_rho


def gen_powerful():
    heap = [(1, 1, 1)]  # (b2**2 * b3**3, b2, b3)
    squares = [0, 1]
    cubes = [0, 1]
    for b3 in itertools.count(2):

        next_v = b3 ** 3
        cubes.append(next_v)
        for b2 in range(len(squares), int(next_v ** .5) + 1):
            sq = b2 ** 2
            squares.append(sq)
        if next_v == squares[-1]:
            continue

        while heap[0][0] < next_v:
            v, b2_, b3_ = heappop(heap)
            yield v, b2_, b3_
            heappush(heap, ((b2_ + 1) ** 2 * b3_ ** 3, b2_ + 1, b3_))
        heappush(heap, (next_v, 1, b3))


def solve_1():
    powerful = {}
    generator = gen_powerful()
    for delta in itertools.count(1):
        v = None
        for v in powerful:
            if v - delta in powerful:
                break
        else:
            for v, b2, b3 in generator:
                powerful[v] = (b2, b3)
                if v - delta in powerful:
                    break
        b2, b3 = powerful[v]
        b2_, b3_ = powerful[v - delta]
        print(f"{delta} = {v} - {v - delta} = {b2}²{b3}³ - {b2_}²{b3_}³")


def get_pow(t, u, b, i):
    """Get t_i, u_i such that (t+u sqrt(b))^i == t_i + u_i sqrt(b)"""
    t_i, u_i = 1, 0
    while i > 0:
        if i & 1:
            t_i, u_i = t_i * t + u_i * u * b, t_i * u + u_i * t
        i >>= 1
        t, u = t * t + u * u * b, 2 * t * u
    return t_i, u_i


def str_factors(factors):
    return '\xb7'.join(f"{f}^{e}" for f, e in sorted(factors.items()))


def factorize(*numbers, timeout=20):
    with Pool() as pool:
        return pool.map_async(factorize_rho, numbers).get(timeout)


def get_powerful_diff(n):
    # Implementation of http://www.kurims.kyoto-u.ac.jp/EMIS/journals/HOA/IJMMS/Volume9_4/812820.pdf
    m = [n, n, (n // 2) ** 2, -n][n % 4]
    if n in (1, 2):
        alpha, beta, gamma, delta = -3, 0, -1, 2
        t, u = 2, 1
    elif n == 5:
        alpha, beta, gamma, delta = -3, 0, -1, 2
        t, u = 10, 3
    elif n % 4 == 0:
        alpha, beta, gamma, delta = 0, 1, 0, 1
        t, u = n // 2, 1
    else:
        alpha, beta, gamma, delta = 1, 0, 3, -2
        t, u = ((m - 3) // 2) ** 2 - 1, abs((m - 3) // 2)

    a = abs((m - alpha) // 2 + beta)
    b = ((m - gamma) // 2) ** 2 + delta

    i = -t * pow(a * u, -1, b) % b
    if n % 4 == 2 and i % 2 == 1:
        i += b

    # print(a, b, t, u, i)

    t_i, u_i = get_pow(t, u, b, i)
    a_i, c_i = t_i * a + u_i * b, a * u_i + t_i

    if n % 4 == 2:
        p1, p2 = a_i + n // 2, a_i - n // 2
    else:
        p1, p2 = a_i ** 2, c_i ** 2 * b
        if p1 < p2:
            p1, p2 = p2, p1

    # Try to factorize the numbers:
    try:
        if n % 4 == 2:
            p1_f, p2_f = factorize(p1, p2)
        else:
            a_i_f, c_i_f, b_f = factorize(a_i, c_i, b)
            p1_f, p2_f = a_i_f + a_i_f, c_i_f + c_i_f + b_f
            if p1 < p2:
                p1_f, p2_f = p2_f, p1_f
        print(f"{n} = {str_factors(p1_f)} - {str_factors(p2_f)}")
    except TimeoutError:
        print(f"{n} = {p1} - {p2}")


def solve_2():
    for n in itertools.count(1):
        get_powerful_diff(n)


if __name__ == "__main__":
    solve_1()
