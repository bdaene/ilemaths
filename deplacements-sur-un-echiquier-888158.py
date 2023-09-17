import multiprocessing
import random
from itertools import count

import numpy

# See https://www.ilemaths.net/sujet-deplacements-sur-un-echiquier-888158.html


# Chess grid are represented by a numpy array of 8x8 boolean where True means there is a pawn in that place.
# We are trying to find a grid where a queen has the longest shortest path between any square of the grid.

RNG = numpy.random.default_rng()


def print_grid(grid):
    print('\n'.join(' '.join('X' if cell else '.' for cell in row) for row in grid))


def get_adjacency(grid: numpy.ndarray):
    """Get the adjacency matrix of the grid for a queen.

    get_adjacency(grid)[i, j] is True if and only if there is a queen move from cell i to j.
    Cells are numbered in numpy.ravel default order.
    """
    open_cells = ~grid
    adjacency = numpy.diag(open_cells.ravel())

    grid_right = open_cells.copy()
    for k in range(1, 8):
        grid_right[:, :-1] &= grid_right[:, 1:]
        grid_right[:, -1] = False
        adjacency |= numpy.diag(grid_right.ravel()[:-k], k=k)

    grid_down = open_cells.copy()
    for k in range(1, 8):
        grid_down[:-1, :] &= grid_down[1:, :]
        grid_down[-1, :] = False
        adjacency |= numpy.diag(grid_down.ravel()[:-8 * k], k=8 * k)

    grid_descending = open_cells.copy()
    for k in range(1, 8):
        grid_descending[:-1, :-1] &= grid_descending[1:, 1:]
        grid_descending[-1, :] = False
        grid_descending[:, -1] = False
        adjacency |= numpy.diag(grid_descending.ravel()[:-9 * k], k=9 * k)

    grid_ascending = open_cells.copy()
    for k in range(1, 8):
        grid_ascending[1:, :-1] &= grid_ascending[:-1, 1:]
        grid_ascending[0, :] = False
        grid_ascending[:, -1] = False
        adjacency |= numpy.diag(grid_ascending.ravel()[7 * k:], k=-7 * k)

    adjacency |= adjacency.transpose()

    return adjacency


def get_diameter(grid):
    """Get the diameter of the grid.

    The diameter of a grid is the longest of the shortest paths for a queen for all pair of cells in the grid.
    """
    adjacency = get_adjacency(grid)

    distance = adjacency.astype(numpy.uint8)
    distance = distance[~grid.ravel(), :]
    distance = distance[:, ~grid.ravel()]
    distance[distance == 0] = 127
    numpy.fill_diagonal(distance, 0)

    for k in range(distance.shape[0]):
        numpy.minimum(distance, distance[:, k:k + 1] + distance[k:k + 1, :], out=distance)

    distance[distance == 127] = 0

    return distance.max()


def crossover(population, fitness, nb_children):
    """Create a new population from the current population.

     The parents are selected proportionally to their fitness.
     """
    new_population = numpy.full((nb_children, 8, 8), False)
    noise = RNG.random(new_population.shape) < .5

    for child in range(nb_children):
        parents = random.choices(range(population.shape[0]), weights=fitness, k=2)
        new_population[child] = numpy.where(noise[child], population[parents[0]], population[parents[1]])

    return new_population


def mutate(population, p):
    """Mutate each gene in a whole population with a probability p."""
    noise = RNG.random(population.shape) < p
    population ^= noise


def get_score(grid):
    return get_diameter(grid), -grid.sum()


def get_fitness(population, generation, worker_pool):
    scores = numpy.array(worker_pool.map(get_score, population), dtype=float)
    fitness = 64 * scores[:, 0] + (1 - 1 / (1 + generation / 100)) * scores[:, 1]
    return 2 ** ((fitness - fitness.min()) / (fitness.max() - fitness.min()))


def main(population_size=200, pawn_probability=0.5, survivors=10):
    population = RNG.random((population_size, 8, 8)) < pawn_probability

    best_score = (0, -64)
    with multiprocessing.Pool() as worker_pool:
        for generation in count():
            population = numpy.unique(population, axis=0)
            fitness = get_fitness(population, generation, worker_pool)
            order = fitness.argsort()

            best_grid = population[order[-1]]
            score = get_score(best_grid)
            if score > best_score:
                best_score = score
                print(f"Generation: {generation}")
                print_grid(best_grid)
                print(score)
                print()

            children = crossover(population[order[survivors:]], fitness[order[survivors:]],
                                 nb_children=population_size - survivors)
            mutate(children, 1/64)
            population = numpy.concatenate((population[order[-survivors:]], children))


def validate(grid: str | numpy.ndarray):
    if isinstance(grid, str):
        grid = numpy.array(grid.split()).reshape(8, 8) == 'X'
    print(get_score(grid))


if __name__ == "__main__":
    main()
