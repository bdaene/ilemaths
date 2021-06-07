
# See https://www.ilemaths.net/sujet-3-points-non-alignes-869501.html

from math import gcd


def solve(n):
    """Place the 2xn pawns on a nxn grid such that no 3 pawns are aligned"""

    pawns = [0] * (2*n)  # Pawn i is in column i%n and row pawns[i] with pawns[i+n] > pawns[i]
    lines = [frozenset()] + [None] * (2*n-1)  # Lines[i] is the forbidden lines before pawn i is placed.

    i = 0
    while i < 2*n:
        if pawns[i] >= n:
            i -= 1
            pawns[i] += 1
        else:
            new_lines = frozenset(get_line(pawns[i], i % n, pawns[j], j % n) for j in range(i))
            if lines[i] & new_lines:
                pawns[i] += 1
            else:
                i += 1
                if i < 2*n:
                    pawns[i] = 0 if i < n else pawns[i-n] + 1
                    lines[i] = lines[i-1] | new_lines

    return pawns


def get_line(a, b, c, d):
    """Get the canonical form my - nx = k of the line going through (a,b) and (c,d)"""
    dx, dy = c-a, d-b
    k = dx*b - dy*a
    g = gcd(dx, dy, k)
    if k < 0:
        g = -g
    return dx//g, dy//g, k//g


def show_grid(n, pawns):
    grid = [['.'] * n for _ in range(n)]
    for col, row in enumerate(pawns):
        grid[row][col % n] = '0'

    print(n)
    print('\n'.join(' '.join(row) for row in grid))


def main():
    for n in range(2, 11):
        solution = solve(n)
        if solution:
            show_grid(n, solution)


if __name__ == "__main__":
    main()
