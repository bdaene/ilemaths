
# See subject at https://www.ilemaths.net/sujet-combien-de-dispositions-a-partir-de-n-cubes-865463.html

from math import factorial
from time import perf_counter


class Solid:

    def __init__(self, cubes):
        ordered_avatars = frozenset(Solid.gen_avatars(cubes))
        avatars = frozenset(map(frozenset, ordered_avatars))
        self.cubes = tuple(min(map(sorted, avatars)))
        self.number_of_permutations = len(ordered_avatars) // len(avatars)

    def __eq__(self, other):
        return other and self.cubes == other.cubes

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.cubes)

    @staticmethod
    def gen_avatars(cubes):
        for rotation in zip(*map(gen_rotations, cubes)):
            yield Solid.move_to_origin(rotation)

    @staticmethod
    def move_to_origin(cubes):
        min_xs = tuple(min(cube[d] for cube in cubes) for d in range(len(cubes[0])))
        return tuple(tuple(c - min_xs[d] for d, c in enumerate(cube)) for cube in cubes)

    def add_cube(self):
        for cube in self.cubes:
            for new_cube in gen_translations(cube):
                if new_cube not in self.cubes:
                    yield Solid(self.cubes + (new_cube,))


def gen_permutations(sequence):
    """Apply Steinhaus–Johnson–Trotter algorithm to generate all permutations of the sequence"""
    sequence = list(sequence)
    n = len(sequence)
    values = list(range(1, n+1))
    directions = [-1] * n

    while True:
        yield tuple(sequence)

        position, value = None, 0
        for i, v in enumerate(values):
            if v > value and 0 <= i + directions[i] < n and values[i + directions[i]] < v:
                position, value = i, v
        if value == 0:
            return

        i, j = position, position + directions[position]
        values[i], values[j] = values[j], values[i]
        sequence[i], sequence[j] = sequence[j], sequence[i]
        directions[i], directions[j] = directions[j], directions[i]

        for i, v in enumerate(values):
            if v > value:
                directions[i] *= -1


def gen_gray_codes(length):
    codes = [(0,) * length]
    yield tuple(codes[0])
    for n in range(length):
        for code in reversed(codes):
            new_code = code[:n] + (1,) + code[n+1:]
            yield new_code
            codes.append(new_code)


def gen_rotations(sequence):
    n = len(sequence)
    codes = list(tuple(1-c*2 for c in code) for code in gen_gray_codes(n))
    for i, permutation in enumerate(gen_permutations(sequence)):
        for code in codes[i % 2::2]:
            yield tuple(x*c for x, c in zip(permutation, code))


def gen_translations(cube):
    for d in range(len(cube)):
        yield cube[:d] + (cube[d] - 1,) + cube[d+1:]
        yield cube[:d] + (cube[d] + 1,) + cube[d + 1:]


def main(max_nb_cubes, dimensions):
    start = perf_counter()
    origin_cube = Solid([(0,)*dimensions])
    solids = [None, {origin_cube}]
    print(f"{0}: {1} ({1}) {perf_counter()-start:3.3f}s")
    print(f"{1}: {1} ({1}) {perf_counter()-start:3.3f}s")

    for nb_cubes in range(2, max_nb_cubes + 1):
        new_solids = set(new_solid for solid in solids[nb_cubes-1] for new_solid in solid.add_cube())

        number_of_colored_solids = sum(factorial(nb_cubes) // solid.number_of_permutations for solid in new_solids)
        print(f"{nb_cubes}: {len(new_solids)} ({number_of_colored_solids}) {perf_counter()-start:3.3f}s")
        solids.append(new_solids)


if __name__ == "__main__":
    main(10, 1)
    main(10, 2)
    main(8, 3)
    main(6, 4)
    main(5, 5)
