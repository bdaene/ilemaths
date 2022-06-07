
# See subject at https://www.ilemaths.net/sujet-de-un-a-dix-sept-879849.html

from itertools import combinations
from fractions import Fraction


def has_sum(tokens, target_sum):
    sums = {0}
    for token in tokens:
        new_sums = set()
        for s in sums:
            new_sum = token + s
            if new_sum == target_sum:
                return True
            if new_sum <= target_sum:
                new_sums.add(new_sum)
        sums |= new_sums
    return False


def main(taken_tokens=5, tokens=17, target_sum=18):
    total, reussite = 0, 0
    for subset in combinations(range(1, tokens + 1), taken_tokens):
        total += 1
        reussite += has_sum(subset, target_sum)
    return Fraction(reussite, total)


if __name__ == "__main__":
    for n in range(1, 11):
        result = main(n)
        print(f"{n:2} {str(result):11} {float(result):.3f}")
