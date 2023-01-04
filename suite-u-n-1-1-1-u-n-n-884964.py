# See https://www.ilemaths.net/sujet-suite-u-n-1-1-1-u-n-n-884964.html
from functools import partial

import numpy
from matplotlib import pyplot, cm


# u_{n+1} = (1+1/u_{n})^n
# w_{n} = log(u_{n})
# w_{n+1} = log(u_{n+1}) = n*log(1 + 1/u_{n}) = n*log1p(1/u_{n}) = n*log1p(exp(-w_{n}))
# w_{n} = -log(exp(w_{n+1}/n)-1)
# v_{n} = w_{n}/(n-1) = log(u_{n})/(n-1)
# v_{n+1} = w_{n+1}/n = n*log1p(exp(-w_{n}))/n = log1p(exp(-w_{n})) = log1p(exp(-v_{n}*(n-1)))

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


def get_vn(v2, n):
    v = v2
    for n in range(2, n):
        v = numpy.log1p(numpy.exp(-v * (n - 1)))
    return v


def get_threshold(func, x_min=-1, x_max=1, y=None):
    y_min = func(x_min)
    y_max = func(x_max)
    if y is None:
        y = (y_min + y_max) / 2

    x_mid = (x_min + x_max) / 2
    while x_min < x_mid < x_max:
        y_mid = func(x_mid)
        if (y_min - y) * (y_mid - y) > 0:
            x_min = x_mid
            y_min = y_mid
        if (y_max - y) * (y_mid - y) > 0:
            x_max = x_mid
            y_max = y_mid
        x_mid = (x_min + x_max) / 2
    return x_min, x_max


def get_w(n_max=60, w1_min=0.1716, w1_max=0.1720, w1_slices=1001):
    w = numpy.full((n_max, w1_slices), 0.)
    w1 = numpy.linspace(w1_min, w1_max, w1_slices)
    n_values = numpy.arange(1, n_max + 1)

    w[0, :] = w1
    for n in range(1, n_max):
        w[n, :] = n * numpy.log1p(numpy.exp(-w[n - 1, :]))

    return w1, n_values, w


def get_v(n_max=60, v2_min=0.6108, v2_max=0.6110, v2_slices=1001):
    v = numpy.full((n_max - 1, v2_slices), 0.)
    v2 = numpy.linspace(v2_min, v2_max, v2_slices)
    n_values = numpy.arange(2, n_max + 1)

    v[0, :] = v2
    for n in range(2, n_max):
        v[n - 1, :] = numpy.log1p(numpy.exp(-v[n - 2, :] * (n - 1)))

    return v2, n_values, v


def plot_surface(x_values, y_values, z_values, axes, x_name, y_name, z_name):
    x_values, y_values = numpy.meshgrid(x_values, y_values)

    # axes.plot_surface(x_values, y_values, z_values, cmap=cm.coolwarm)
    # axes.plot_surface(x_values[::2, :], y_values[::2, :], z_values[::2, :], cmap=cm.coolwarm)
    axes.plot_surface(x_values[1::2, :], y_values[1::2, :], z_values[1::2, :], cmap=cm.coolwarm)
    axes.set_xlabel(x_name)
    axes.set_ylabel(y_name)
    # axes.set_zlabel(f"{w_name}")
    axes.set_title(f"{z_name}({x_name}, {y_name})")


def plot_quivers(v, axes, x_name, y_name, z_name):
    if v.shape[0] % 2:
        v = v[:-(v.shape[0] % 2), :]
    x = v[::2, :]
    y = v[1::2, :]
    dx = x[1:, :] - x[:-1, :]
    dy = y[1:, :] - y[:-1, :]
    c = numpy.tile(x[0, :], (x.shape[0], 1))

    axes.quiver(x[:-1], y[:-1], dx, dy, c[:-1], scale=1, angles='xy', scale_units='xy', cmap=cm.coolwarm)

    axes.plot(x[:, v.shape[1] // 2], y[:, v.shape[1] // 2], 'r')
    axes.set_xlabel(f"{z_name}({x_name}, {y_name}=2k)")
    axes.set_ylabel(f"{z_name}({x_name}, {y_name}=2k+1)")
    axes.set_title(f"{z_name}({x_name}, {y_name})")


def main():
    figure = pyplot.figure()
    figure_rows, figure_columns = 2, 3

    w1_min, w1_max = get_threshold(partial(get_wn, n=1000))
    print(f"{w1_min} < w1 < {w1_max} ({numpy.exp(w1_min)} < u1 < {numpy.exp(w1_max)})")
    w1_delta = 0.002
    w1, n, w = get_w(n_max=50, w1_min=w1_min - w1_delta, w1_max=w1_max + w1_delta, w1_slices=1001)
    axes = figure.add_subplot(figure_rows, figure_columns, 1, projection='3d')
    plot_surface(w1, n, w, axes, 'w1', 'n', 'w')

    v2_min, v2_max = get_threshold(partial(get_vn, n=1000))
    print(f"{v2_min} < v2 < {v2_max} ({1 / (numpy.expm1(v2_max))} < u1 < {1 / (numpy.expm1(v2_min))})")
    v2_delta = 0.001
    v1, n, v = get_v(n_max=50, v2_min=v2_min - v2_delta, v2_max=v2_max + v2_delta, v2_slices=1001)
    axes = figure.add_subplot(figure_rows, figure_columns, 2, projection='3d')
    plot_surface(v1, n, v, axes, 'v1', 'n', 'v')

    v2_delta = 0.25
    v1, n, v = get_v(n_max=100, v2_min=v2_min - v2_delta, v2_max=v2_max + v2_delta, v2_slices=21)
    axes = figure.add_subplot(figure_rows, figure_columns, 3)
    plot_quivers(v, axes, 'v2', 'n', 'v')

    pyplot.show()


if __name__ == "__main__":
    main()
