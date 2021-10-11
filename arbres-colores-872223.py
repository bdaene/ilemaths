
# https://www.ilemaths.net/sujet-arbres-colores-872223.html


def solve(n):
    """Find the color, the group and the position of the nth tree."""
    # RR VVV RRR VVVV RRRR VVVVV RRRRR ...
    # 12 345 678 9012 3456 78901 23456
    if n < 3:
        return 'R', 1, n

    step = 3
    n -= 3

    while 2 * step <= n:
        n -= 2 * step
        step += 1

    color = 'V' if n < step else 'R'
    group = (step-3)*2 + (2 if n < step else 3)
    position = 1 + (n if n < step else n-step)

    return color, group, position


def main():
    index = int(input())
    color, group, position = solve(index)
    print(f'{index}th tree is {color} and is the {position}th tree of the {group}th group of trees.')


if __name__ == "__main__":
    main()
