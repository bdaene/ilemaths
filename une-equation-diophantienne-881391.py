
# See https://www.ilemaths.net/sujet-une-equation-diophantienne-881391.html

def solve(a):
    p = 2*a
    m = 12*a**p
    b, c, bp, cp = 1, 2, 1, 2**p
    while b < c:
        if bp + m < cp:
            b += 1
            bp = b**p
        else:
            if bp + m == cp:
                yield b, c
            c += 1
            cp = c**p


def main():
    for a in range(1, 1000):
        for b, c in solve(a):
            print(f"{2*c}^{2*a} - {2*b}^{2*a} = 12({2*a})^{2*a}")


if __name__ == "__main__":
    main()
