# See https://www.ilemaths.net/sujet-algorithme-de-deplacement-888006.html
from itertools import islice

import numpy
from matplotlib import pyplot, animation, colors


def get_move_probability(size, obstacles):
    up = numpy.ones(size)
    up[0, :] = 0
    down = numpy.ones(size)
    down[-1, :] = 0
    left = numpy.ones(size)
    left[:, 0] = 0
    right = numpy.ones(size)
    right[:, -1] = 0

    for row, col in obstacles:
        if row < size[0] - 1:
            up[row + 1, col] = 0
        if row > 0:
            down[row - 1, col] = 0
        if col < size[1] - 1:
            left[row, col + 1] = 0
        if col > 0:
            right[row, col - 1] = 0

    total = up + down + left + right
    up /= total
    down /= total
    left /= total
    right /= total

    return up, down, left, right


def gen_states(size, obstacles, start, end):
    state = numpy.zeros(size)
    state[start] = 1

    up, down, left, right = get_move_probability(size, obstacles)

    while True:
        yield state
        state[end] = 0

        state_ = numpy.zeros(size)
        state_[:-1, :] += state[1:, :] * up[1:, :]
        state_[1:, :] += state[:-1, :] * down[:-1, :]
        state_[:, :-1] += state[:, 1:] * left[:, 1:]
        state_[:, 1:] += state[:, :-1] * right[:, :-1]

        state = state_


def animate_states(size, state_generator):
    figure, axes = pyplot.subplots()
    image = axes.imshow(numpy.zeros(size), norm=colors.LogNorm(vmin=0.001, vmax=1))

    def animate(t):
        state = next(state_generator)
        image.set_data(state)
        return image

    anim = animation.FuncAnimation(figure, animate)
    pyplot.show()


def draw_move_density(end, state_generator, max_move=4000):
    density = list(islice((state[end] for state in state_generator), max_move))

    figure, axes = pyplot.subplots()
    axes.plot(density, '.')
    # axes.set_yscale('log')

    pyplot.show()


def compute_expected_moves(end, state_generator, max_moves=10000):
    expected_moves = sum(move * state[end] for move, state in enumerate(islice(state_generator, max_moves)))
    print(expected_moves)
    return expected_moves


def solve_system(size, obstacles, start, end):
    index = [(row, col) for row in range(size[0]) for col in range(size[1]) if (row, col) not in obstacles]
    index_map = {cell: i for i, cell in enumerate(index)}

    a = numpy.zeros((len(index), len(index)))
    b = numpy.zeros(len(index))
    for i, (row, col) in enumerate(index):
        if (row, col) == end:
            a[i, i] = 1
            b[i] = 0
            continue

        total = 0
        for cell in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if (j := index_map.get(cell)) is not None:
                total += 1
                a[i, j] = -1
        a[i, i] += total
        b[i] = total

    x = numpy.linalg.solve(a, b)

    print(x[index_map[start]])

    expected_moves = numpy.zeros(size)
    for cell in obstacles:
        expected_moves[cell] = float('nan')
    for i, cell in enumerate(index):
        expected_moves[cell] = x[i]

    figure, axes = pyplot.subplots()
    colors = axes.imshow(expected_moves)
    figure.colorbar(colors, ax=axes)
    pyplot.show()

    return expected_moves[start]


def main():
    size = (10, 10)
    obstacles = [(8, 2), (2, 3), (5, 3), (10, 4), (3, 6), (7, 6), (10, 6), (2, 9), (4, 10),
                 (6, 9), (10, 9)]
    start = (10, 1)
    end = (1, 10)

    # 0 indexing
    obstacles = [(row - 1, col - 1) for row, col in obstacles]
    start = (start[0] - 1, start[1] - 1)
    end = (end[0] - 1, end[1] - 1)

    state_generator = gen_states(size, obstacles, start, end)

    animate_states(size, gen_states(size, obstacles, start, end))
    draw_move_density(end, gen_states(size, obstacles, start, end))
    compute_expected_moves(end, gen_states(size, obstacles, start, end))
    solve_system(size, obstacles, start, end)


if __name__ == "__main__":
    main()
