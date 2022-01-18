
# See subject at https://www.ilemaths.net/sujet-combien-de-dispositions-a-partir-de-n-cubes-865463.html

from math import factorial
from time import perf_counter
from functools import cache


class Solid:

    even_permutations = [[()]]
    odd_permutations = [[]]
    gray_codes: list[list[tuple[int, ...]]] = [[()]]

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
    def create_permutations(dimension):
        for d in range(len(Solid.even_permutations)-1, dimension):
            even_permutations = []
            odd_permutations = []
            for permutation in Solid.even_permutations[d]:
                for i in range(0, d + 1):
                    if (d-i) % 2 == 0:
                        even_permutations.append(permutation[:i] + (d,) + permutation[i:])
                    else:
                        odd_permutations.append(permutation[:i] + (d,) + permutation[i:])
            for permutation in Solid.odd_permutations[d]:
                for i in range(0, d + 1):
                    if (d - i) % 2 == 1:
                        even_permutations.append(permutation[:i] + (d,) + permutation[i:])
                    else:
                        odd_permutations.append(permutation[:i] + (d,) + permutation[i:])
            Solid.even_permutations.append(even_permutations)
            Solid.odd_permutations.append(odd_permutations)

    @staticmethod
    def create_gray_codes(dimension):
        for d in range(len(Solid.gray_codes)-1, dimension):
            codes = [(1,) + code for code in Solid.gray_codes[d]]
            codes += [(-1,) + code for code in reversed(Solid.gray_codes[d])]
            Solid.gray_codes.append(codes)

    @staticmethod
    def gen_avatars(cubes):
        for rotation in zip(*map(Solid.get_rotations, cubes)):
            yield Solid.move_to_origin(rotation)

    @staticmethod
    def move_to_origin(cubes):
        min_xs = tuple(min(cube[d] for cube in cubes) for d in range(len(cubes[0])))
        return tuple(tuple(c - min_xs[d] for d, c in enumerate(cube)) for cube in cubes)

    def add_cube(self):
        for cube in self.cubes:
            for new_cube in Solid.gen_translations(cube):
                if new_cube not in self.cubes:
                    yield Solid(self.cubes + (new_cube,))

    def add_dimension(self):
        return Solid(tuple(cube + (0,) for cube in self.cubes))

    @staticmethod
    @cache
    def get_rotations(cube):
        d = len(cube)
        rotations = []
        for permutation in Solid.even_permutations[d]:
            for code in Solid.gray_codes[d][::2]:
                rotations.append(tuple(cube[permutation[i]] * code[i] for i in range(len(cube))))
        for permutation in Solid.odd_permutations[d]:
            for code in Solid.gray_codes[d][1::2]:
                rotations.append(tuple(cube[permutation[i]] * code[i] for i in range(len(cube))))
        return tuple(rotations)

    @staticmethod
    def gen_translations(cube):
        for d in range(len(cube)):
            yield cube[:d] + (cube[d] - 1,) + cube[d+1:]
            yield cube[:d] + (cube[d] + 1,) + cube[d + 1:]


def main(max_nb_cubes, dimensions):
    start = perf_counter()
    Solid.create_permutations(dimensions)
    Solid.create_gray_codes(dimensions)
    origin_cube = Solid([(0,)])
    solids = {origin_cube}
    print(f"Solids in dimension {dimensions}:")
    print(f"{1}: {1} ({1}) {perf_counter()-start:3.3f}s")

    for nb_cubes in range(2, max_nb_cubes + 1):
        solids = set(new_solid for solid in solids for new_solid in solid.add_cube())
        if nb_cubes <= dimensions:
            solids = set(solid.add_dimension() for solid in solids)

        number_of_colored_solids = sum(factorial(nb_cubes) // solid.number_of_permutations for solid in solids)
        print(f"{nb_cubes}: {len(solids)} ({number_of_colored_solids}) {perf_counter()-start:3.3f}s")


if __name__ == "__main__":
    main(10, 1)
    main(10, 2)
    main(8, 3)
    main(7, 4)
    main(6, 5)
    main(6, 6)
    main(6, 7)
