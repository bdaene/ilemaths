# See https://www.ilemaths.net/sujet-trouver-un-seul-numero-887480.html
from itertools import combinations, permutations
from string import ascii_letters

"""
Cards have a face value and a back value. There is 't' cards.
The goal of the player is to find the back value of at least one card. The goal of the engine is to prevent it.
At each turn the player choose 'p' cards and the engine gives the back value of one of them.

For a given p, there is limit g(p) such that for all t >= g(p) the player can win no matter what the engine does.
For example g(2) = 4.

For example, for p = 2 and t = 3, the engine can propose:
ab -> 0     
ac -> 1
bc -> 2

But for p = 2 and t = 4, the engine has no solution:
ab -> 0
ac -> 1 (if 0 then a = 0)
ad -> 2 (0 => a = 0, 1 => a = 1)
bc -> 3 (0 => b = 0, 1 => c = 1, 2 impossible because in ad)
bd -> ? (0 => b = 0, 1 impossible, 2 => d = 2, 3 => b = 3)
cd -> ? (0 impossible, 1 => c = 1, 2 => d = 2, 3 => c = 3) 
"""


def apply_guess(possibilities, guess, value):
    for possibility in possibilities:
        if any(possibility[i] == value for i in guess):
            yield possibility


def solve(t, guesses):
    possibilities = permutations(range(t))
    for guess, value in guesses:
        possibilities = apply_guess(possibilities, guess, value)

    # Remove possibilities with common back value
    possibilities = tuple(possibilities)
    i = 1
    while i < len(possibilities):
        compatible_possibilities = tuple(p for p in possibilities[i:]
                                         if all(p_i != p0_i for p_i, p0_i in zip(p, possibilities[i - 1])))
        possibilities = possibilities[:i] + compatible_possibilities
        i += 1
    return possibilities


def gen_guesses(t, p, permutation=None):
    a = tuple(range(t))

    if permutation:
        b = tuple(permutation)
        assert tuple(sorted(b)) == a
    else:
        b = []
        for i in range(0, len(a), 3):
            b.extend(a[i + 1:i + 3])
            b.append(a[i])
        if len(a) % 3 == 1:
            b[-1], b[-2] = b[-2], b[-1]
        b = tuple(b)

    assert all(a_i != b_i for a_i, b_i in zip(a, b))

    for guess in combinations(a, p):
        a_i = set(a[g] for g in guess)
        b_i = set(b[g] for g in guess)
        yield guess, min(a_i & b_i)


def main():
    t, p = 9, 4

    guesses = tuple(gen_guesses(t, p))
    for guess, value in guesses:
        guess = ''.join(ascii_letters[g] for g in guess)
        print(f"{guess} -> {value}")

    possibilities = solve(t=t, guesses=guesses)

    for possibility in possibilities:
        print(possibility)


if __name__ == "__main__":
    main()
