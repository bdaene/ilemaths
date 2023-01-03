# See https://www.ilemaths.net/sujet-suite-u-n-1-1-1-u-n-n-884964.html

import numpy
from matplotlib import pyplot


# u_{n+1} = (1+1/u_{n})^n
# w = log(u)
# w_{n+1} = log(u_{n+1}) = n*log(1 + 1/u_{n}) = n*log1p(1/u_{n}) = n*log1p(exp(-w_{n})
# w_{n} = -log(exp(w_{n+1}/n)-1)

def get_wn(w1, n):
    w = w1
    for n in range(1, n):
        w = n * numpy.log1p(numpy.exp(-w))
    return w


def get_w1(wn, n):
    w = wn
    for n in reversed(range(1, n)):
        w = -numpy.log(numpy.expm1(w / n))
    return w


def show_w(n_limit=60, w1_min=0.1716, w1_max=0.1720, w1_slices=1001):
    w = numpy.full((n_limit, w1_slices), 0.)
    w1 = numpy.linspace(w1_min, w1_max, w1_slices)
    w[0, :] = w1

    for n in range(1, n_limit):
        w[n, :] = n * numpy.log1p(numpy.exp(-w[n - 1, :]))

    w1, n = numpy.meshgrid(w1, numpy.arange(1, n_limit + 1))
    axes = pyplot.axes(projection='3d')
    axes.plot_surface(w1[::2, :], n[1::2, :], w[1::2, :])
    axes.set_xlabel('w1')
    axes.set_ylabel('n')
    axes.set_zlabel('wn')

    pyplot.show()


def get_w1_threshold(w1_min=-1, w1_max=1, n=1000):
    wn_min = get_wn(w1_min, n)
    wn_max = get_wn(w1_max, n)

    w1_mid = (w1_min + w1_max) / 2
    while w1_min < w1_mid < w1_max:
        wn_mid = get_wn(w1_mid, n)
        if abs(wn_mid - wn_min) < abs(wn_mid - wn_max):
            w1_min, wn_min = w1_mid, wn_mid
        else:
            w1_max, wn_max = w1_mid, wn_max
        w1_mid = (w1_min + w1_max) / 2
    return w1_min, w1_max


def main():
    # show_w(w1_min=-1, w1_max=1)
    # for n in range(10, 110, 10):
    #     w1_min, w1_max = get_w1_threshold(n=n)
    #     print(w1_min, w1_max)

    w1_min, w1_max = get_w1_threshold(n=100)
    print(f"{w1_min} < w1 < {w1_max} ({numpy.exp(w1_min)} < u1 < {numpy.exp(w1_max)})")
    show_w(w1_min=w1_min - 0.0001, w1_max=w1_max + 0.0001)


if __name__ == "__main__":
    main()
