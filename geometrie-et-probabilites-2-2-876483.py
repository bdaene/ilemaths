
# See subject at https://www.ilemaths.net/sujet-geometrie-et-probabilites-2-2-876483.html

from random import random
from matplotlib import pyplot
import numpy


def random_area():
    dx, dy = random(), random()
    if dx + dy > 1:
        dx, dy = 1-dy, 1-dx
    ex, ey = random(), random()
    if ex + ey > 1:
        ex, ey = 1-ey, 1-ex

    x = dx + dy*(ex-dx)/(dy-ey)
    y = ey + ex*(dy-ey)/(ex-dx)

    return x, y


# def random_area():
#     x = random()**.5
#     y = random()**.5
#
#     return x, y


def main():
    t = 1000000
    xs, ys, areas = [], [], []
    for _ in range(t):
        x, y = random_area()
        if 0 <= x <= 1 and 0 <= y <= 1:
            xs.append(x)
            ys.append(y)
            areas.append(x*y)
    print(len(areas))
    print(sum(areas)/len(areas))
    print(numpy.corrcoef(xs, ys))

    pyplot.hist(xs, bins=list(b/100 for b in range(101)))
    pyplot.hist(ys, bins=list(b/100 for b in range(101)))
    pyplot.show()

    pyplot.scatter(xs, ys, 0.01, marker='.')
    pyplot.show()

    pyplot.hist(areas, bins=list(b/100 for b in range(101)))
    pyplot.show()


if __name__ == "__main__":
    main()
