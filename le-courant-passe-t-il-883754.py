# See https://www.ilemaths.net/sujet-le-courant-passe-t-il-883754.html


def get_current(configuration):
    current = 0b1111

    for _ in range(3):
        stage = configuration & 0b111
        current = (((current >> 1) & stage) | (current & ~stage & 0b111) << 1) & 0b1111
        configuration >>= 3

    return current


def show(configuration):
    lines = ['|', '|', '|']
    for _ in range(3):
        stage = configuration & 0b111
        configuration >>= 3
        for i in range(3):
            lines[i] += '/' if stage & 1 else '\\'
            stage >>= 1
    print('|\n'.join(lines)+'|')


def main():
    count = 1 << 9
    for configuration in range(1 << 9):
        current = get_current(configuration)
        if not current:
            print(configuration)
            show(configuration)
            count -= 1
    print(f"{count}:{(1<<9)-count}:{1<<9}")


if __name__ == "__main__":
    main()
