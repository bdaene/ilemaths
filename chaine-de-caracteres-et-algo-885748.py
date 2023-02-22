# See https://www.ilemaths.net/sujet-chaine-de-caracteres-et-algo-885748.html
import cProfile
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


def generate_message(nb_letters, nb_digits):
    message = choices(ascii_uppercase, k=nb_letters) + choices(digits, k=nb_digits)
    shuffle(message)
    return ''.join(message)


def test(length, func):
    message = generate_message(length // 2, length - length // 2)
    nb_tests = 10000000 // length

    for _ in range(nb_tests):
        func(message)


def main():
    assert replace_letters('6930A85CDU744ZABR09') == '6930185123744123409'
    assert flight('6930A85CDU744ZABR09') == '6930185123744123409'

    for n in range(7):
        length = 10 ** n
        message = generate_message(length // 2, length - length // 2)

        nb_tests = 1000000 // length
        t1 = timeit(stmt=f'replace_letters("{message}")', setup='from __main__ import replace_letters', number=nb_tests)
        t2 = timeit(stmt=f'flight("{message}")', setup='from __main__ import flight', number=nb_tests)

        print(f"{length:>7}", f"{t1 * 1000 / nb_tests:>7.3f}", f"{t2 * 1000 / nb_tests:>7.3f}")

    cProfile.run(statement='test(10000, replace_letters)')
    cProfile.run(statement='test(10000, flight)')


if __name__ == "__main__":
    main()
