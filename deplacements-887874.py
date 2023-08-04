# See https://www.ilemaths.net/sujet-deplacements-887874.html
from math import log

import numpy
from itertools import product
from matplotlib import pyplot


def canonize(coordinates):
    return tuple(sorted(map(abs, coordinates)))


def solve(limit, dimensions):
    variables = sorted(set(canonize(coordinates) for coordinates in product(range(limit), repeat=dimensions)))
    variable_to_index = {variable: index for index, variable in enumerate(variables)}

    equations = numpy.zeros((len(variables), len(variables)))

    for variable in variables:
        row = variable_to_index[variable]
        equations[row, row] += 1
        for dimension in range(dimensions):
            for direction in (-1, 1):
                new_variable = variable[:dimension] + (variable[dimension] + direction,) + variable[dimension + 1:]
                new_variable = canonize(new_variable)
                if (col := variable_to_index.get(new_variable)) is not None:
                    equations[row, col] -= 1 / (2 * dimensions)

    expected_moves = numpy.linalg.solve(equations, numpy.ones((len(variables), 1)))

    # print(variables)
    # print(equations)
    # print(expected_moves)

    return {variable: expected_moves[index,0] for variable, index in variable_to_index.items()}


def main():
    for d in range(1, 5):
        ls, points = [], []
        for l in range(1, 21):
            ls.append(l)
            # points.append(solve(l, d)[(0,)*d]/(l**2*(1+(d-1)*0.17)))
            points.append(solve(l, d)[(0,)*d])
        print(points)
        pyplot.plot(ls, points, '.', label=f"Dimension = {d}")

    pyplot.title(f"Expected moves before walk to the limit")
    pyplot.xlabel(f"Limit")
    pyplot.ylabel(f"E(moves)")
    pyplot.legend()
    pyplot.show()


if __name__ == "__main__":
    main()

