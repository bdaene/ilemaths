
# https://www.ilemaths.net/sujet-cubes-et-algorithme-871835.html

from heapq import heappop, heappush


def solve(n, k):

    # Nodes are (Number of terms, remainder, terms)
    heap = [(0, n, ())]
    while heap:
        _, n, terms = heappop(heap)
        if n == 0:
            # If there is no remainder, we found the solution.
            return terms

        m = int(n**(1/3))   # Maximum term
        if terms:
            # Do not look twice for the same solution.
            m = min(m, terms[-1])

        for i in range(1, m+1):
            heappush(heap, (1+len(terms), n-i**k, terms + (i,)))


def main():
    n = int(input("Entrez un nombre: "))
    print(solve(n, 3))


if __name__ == "__main__":
    main()
