

# https://www.ilemaths.net/sujet-s-arreter-avant-le-rattrapage-du-retard-874683.html

from random import random
from matplotlib import pyplot
from collections import Counter


def simulate(n=100):
    red, green = n, n
    money = 0
    best = money

    while red or green:
        if random() * (green + red) < green:
            money += 1
            best = max(best, money)
            green -= 1
        else:
            money -= 1
            red -= 1

    return best


def main():
    n, t = 100, 100000
    results = [simulate(n) for _ in range(t)]
    count = Counter(results)
    xs = sorted(count)
    ys = [sum(count[i] for i in count if i >= x) * x / t for x in xs]
    pyplot.plot(xs, ys)
    pyplot.show()


if __name__ == "__main__":
    main()
