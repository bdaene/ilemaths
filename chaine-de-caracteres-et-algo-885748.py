# See https://www.ilemaths.net/sujet-chaine-de-caracteres-et-algo-885748.html
import cProfile
from functools import reduce
from itertools import chain, groupby
from random import choices, shuffle
from string import ascii_uppercase, digits
from timeit import timeit


def replace_letters(message):
    modified_message, last_digit_index = "", -1
    for i, c in enumerate(message):
        if c.isdigit():
            modified_message += c
            last_digit_index = i
        else:
            modified_message += str(i - last_digit_index)

    return modified_message


def flight(s):
    n, i = len(s), 0
    z = ""
    digits = set("0123456789")

    while i < n:
        j = i
        while j < n and s[j] in digits:
            j += 1
        z += s[i:j]
        i = j
        while j < n and s[j] not in digits:
            j += 1
        z += ''.join(str(k) for k in range(1, j - i + 1))

        if i < j:
            i = j
        else:
            i += 1

    return z


def replace_letters_2(message):
    return ''.join(
        map(
            str,
            chain.from_iterable(
                g if k else (i for i, c in enumerate(g, 1))
                for k, g in groupby(message, digits.__contains__)
            )
        )
    )


def replace_letters_3(message):
    modified_message = []
    current_digits = []
    count = 0
    for c in message:
        if c in digits:
            if count:
                modified_message.append(map(str, range(1, count + 1)))
                count = 0
            current_digits.append(c)
        else:
            if current_digits:
                modified_message.append(current_digits)
                current_digits = []
            count += 1

    if current_digits:
        modified_message.append(current_digits)
    if count:
        modified_message.append(map(str, range(1, count + 1)))

    return ''.join(chain.from_iterable(modified_message))


def nb_digits(n):
    assert (n > 0)
    if n < 10:
        return 1

    b, r = 10, 1
    while b < n:
        b *= 10
        r += 1
    return r + (0, 1)[n % b == 0]


def letters2digits(n):
    assert (n >= 0)
    if n == 0:
        return 1, 0

    def iter_base(base, acc):
        next_base = base * 10
        p = min(next_base, n + 1)
        for i in range(base, p):
            acc = next_base * acc + i
        return next_base, acc

    base, acc = reduce(lambda x, _: iter_base(*x), range(nb_digits(n)), (1, 0))

    return 10 ** nb_digits(acc), acc


def flight_with_acc(s):
    n, i = len(s), 0
    r = 0

    while i < n:
        j = i
        while j < n and s[j].isdigit():
            r = r * 10 + ord(s[j]) - 48
            j += 1

        i = j
        while j < n and not s[j].isdigit():
            j += 1

        pow10, acc = letters2digits(j - i)
        r = r * pow10 + acc

        i = max(j, i + 1)

    return str(r).zfill(n)


def generate_message(nb_letters, nb_digits):
    message = choices(ascii_uppercase, k=nb_letters) + choices(digits, k=nb_digits)
    shuffle(message)
    return ''.join(message)


ALGORITHMS = [replace_letters, flight, replace_letters_2, replace_letters_3, flight_with_acc]


def validate(message='6930A85CDU744ZABR09', expected_result='6930185123744123409'):
    for algorithm in ALGORITHMS:
        assert algorithm(message) == expected_result


def compare_times():
    print('length', *(algorithm.__name__ for algorithm in ALGORITHMS))

    for n in range(6):
        length = 10 ** n
        messages = [generate_message(length // 2, length - length // 2) for _ in range(10)]

        nb_tests = 100000 // length

        times = [
            timeit(stmt=f'list({algorithm.__name__}(message) for message in {messages})',
                   setup=f'from __main__ import {algorithm.__name__}', number=nb_tests)
            for algorithm in ALGORITHMS
        ]

        print(f"{length:>7}", *(f"{t * 100 / nb_tests:>7.3f}" for t in times))

    print()


def profile():
    messages = [generate_message(50000, 50000) for _ in range(100)]
    for algorithm in ALGORITHMS:
        print(algorithm.__name__)
        cProfile.run(statement=f'list({algorithm.__name__}(message) for message in {messages})', sort='cumulative')


def main():
    validate()
    compare_times()
    profile()


if __name__ == "__main__":
    main()
