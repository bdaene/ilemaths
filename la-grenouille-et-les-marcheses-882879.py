# See https://www.ilemaths.net/sujet-la-grenouille-et-les-marcheses-882879.html#msg8090441

import numpy


def main():
    transition = numpy.full((11, 11), 0.)

    for m in range(0, 9):
        transition[m, m + 1] = 2 / 3
        transition[m, m + 2] = 1 / 3

    transition[9][10] = 1.

    start = numpy.full((11,), 0.)
    start[0] = 1.

    expected = numpy.dot(start, numpy.dot(transition, numpy.linalg.matrix_power(transition - numpy.identity(11), -2)))

    print(expected[10])


if __name__ == "__main__":
    main()
