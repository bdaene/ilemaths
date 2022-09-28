# See https://www.ilemaths.net/sujet-nombres-puissants-882341.html
import itertools
from heapq import heappop, heappush


def gen_powerful():
    heap = [(1, 1, 1)]  # (b2**2 * b3**3, b2, b3)
    last_v = 0
    for b3 in itertools.count(2):
        next_v = b3 ** 3
        while heap[0][0] < next_v:
            v, b2_, b3_ = heappop(heap)
            if v > last_v:
                last_v = v
                yield v, b2_, b3_
            heappush(heap, ((b2_ + 1) ** 2 * b3_ ** 3, b2_ + 1, b3_))
        heappush(heap, (next_v, 1, b3))


def main():
    powerful = {}
    generator = gen_powerful()
    for delta in itertools.count():
        for v, (b2, b3) in powerful.items():
            if v - delta in powerful:
                b2_, b3_ = powerful[v-delta]
                print(f"{b2}²{b3}³ - {b2_}²{b3_}³ = {delta}")
                break
        else:
            for v, b2, b3 in generator:
                powerful[v] = (b2, b3)
                if v - delta in powerful:
                    b2_, b3_ = powerful[v-delta]
                    print(f"{b2}²{b3}³ - {b2_}²{b3_}³ = {delta}")
                    break


if __name__ == "__main__":
    main()
