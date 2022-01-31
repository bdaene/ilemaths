# https://www.ilemaths.net/sujet-demineur-revisite-877247.html

from itertools import product


def solve(m):
    solutions = {}
    for start in product((True, False), repeat=m):
        grid = [start]

        valid_lengths, current_length = [], 1
        while True:
            count = [(grid[-1][i]
                      + (grid[-2][i] if current_length > 1 else 0)
                      + (grid[-1][i - 1] if i > 0 else 0)
                      + (grid[-1][i + 1] if i < m - 1 else 0))
                     for i in range(m)]

            if all(c % 2 == 1 for c in count):
                valid_lengths.append(current_length)

            next_column = tuple(c % 2 == 0 for c in count)
            if next_column == start and all(c == 0 for c in grid[-1]):
                break

            grid.append(next_column)
            current_length += 1

        show_grid(grid)
        print(current_length, valid_lengths)
        solutions.setdefault(current_length, set())
        solutions[current_length] |= set(valid_lengths)

    return solutions


def show_grid(grid):
    m, n = len(grid[0]), len(grid)
    print('\n'.join(''.join('#' if grid[j][i] else ' ' for j in range(n)) for i in range(m)))


def main():
    solutions = solve(3)
    print(solutions)


if __name__ == "__main__":
    main()
