
# See subject at https://www.ilemaths.net/sujet-aurais-je-ma-place-859535.html

from random import randint, choice


def simulate(n):
    available_seats = set(range(n))

    available_seats.remove(randint(0, n-1))

    count = 0
    for i in range(1, n-1):
        if i in available_seats:
            available_seats.remove(i)
        else:
            count += 1
            seat = choice(list(available_seats))
            available_seats.remove(seat)

    if n-1 in available_seats:
        return True, count
    else:
        return False, count + 1


def main():
    n = 10
    t = 100000
    total = 0
    count_ = 0
    for _ in range(t):
        available, count = simulate(n)
        total += count
        if not available:
            count_ += 1

    print(count_/t)
    print(total/t)
    print(sum(1/i for i in range(2, n+1)))


if __name__ == "__main__":
    main()
