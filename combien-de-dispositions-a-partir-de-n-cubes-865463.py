
# See subject at https://www.ilemaths.net/sujet-combien-de-dispositions-a-partir-de-n-cubes-865463.html

from math import factorial
from time import perf_counter


class Solid:
    rotations = frozenset((
        lambda x, y, z: (x, y, z),
        lambda x, y, z: (x, -y, -z),
        lambda x, y, z: (-x, y, -z),
        lambda x, y, z: (-x, -y, z),
        lambda x, y, z: (-x, -z, -y),
        lambda x, y, z: (-x, z, y),
        lambda x, y, z: (x, -z, y),
        lambda x, y, z: (x, z, -y),

        lambda x, y, z: (y, z, x),
        lambda x, y, z: (y, -z, -x),
        lambda x, y, z: (-y, z, -x),
        lambda x, y, z: (-y, -z, x),
        lambda x, y, z: (-y, -x, -z),
        lambda x, y, z: (-y, x, z),
        lambda x, y, z: (y, -x, z),
        lambda x, y, z: (y, x, -z),

        lambda x, y, z: (z, x, y),
        lambda x, y, z: (z, -x, -y),
        lambda x, y, z: (-z, x, -y),
        lambda x, y, z: (-z, -x, y),
        lambda x, y, z: (-z, -y, -x),
        lambda x, y, z: (-z, y, x),
        lambda x, y, z: (z, -y, x),
        lambda x, y, z: (z, y, -x),
    ))

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
        for rotation in Solid.rotations:
            yield Solid.move_to_origin(tuple(rotation(*cube) for cube in cubes))

    @staticmethod
    def move_to_origin(cubes):
        min_x = min(x for x, y, z in cubes)
        min_y = min(y for x, y, z in cubes)
        min_z = min(z for x, y, z in cubes)
        return tuple((x - min_x, y - min_y, z - min_z) for x, y, z in cubes)

    def add_cube(self):
        for cube in self.cubes:
            x, y, z = cube
            for dx, dy, dz in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)):
                new_cube = (x+dx, y+dy, z+dz)
                if new_cube not in self.cubes:
                    yield Solid(self.cubes + (new_cube,))


def main(max_nb_cubes):
    start = perf_counter()
    origin_cube = Solid([(0, 0, 0)])
    solids = [set(), {origin_cube}]
    print(f"{0}: {0} ({0}) {perf_counter()-start:3.3f}s")
    print(f"{1}: {1} ({1}) {perf_counter()-start:3.3f}s")

    for nb_cubes in range(2, max_nb_cubes + 1):
        new_solids = set(new_solid for solid in solids[nb_cubes-1] for new_solid in solid.add_cube())

        number_of_colored_solids = sum(factorial(nb_cubes) // solid.number_of_permutations for solid in new_solids)
        print(f"{nb_cubes}: {len(new_solids)} ({number_of_colored_solids}) {perf_counter()-start:3.3f}s")
        solids.append(new_solids)


if __name__ == "__main__":
    main(10)
