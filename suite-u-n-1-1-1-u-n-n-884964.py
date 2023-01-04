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
# v_{n} = -log(exp(v_{n+1})-1)/(n-1)

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


def get_v(n_min=2, n_max=60, v_min=0.6108, v_max=0.6110, v_slices=1001):
    v = numpy.full((n_max - n_min + 1, v_slices), 0.)
    v_start = numpy.linspace(v_min, v_max, v_slices)
    n_values = numpy.arange(n_min, n_max + 1)

    v[0, :] = v_start
    for n in range(n_min, n_max):
        v[n + 1 - n_min, :] = numpy.log1p(numpy.exp(-v[n - n_min, :] * (n - 1)))

    return v_start, n_values, v


def get_vn2(n, v_min=numpy.log1p(0), v_max=numpy.log1p(1), v_slices=11):
    vn = numpy.linspace(v_min, v_max, v_slices)
    vn1 = numpy.log1p(numpy.exp(-vn * (n - 1)))
    vn2 = numpy.log1p(numpy.exp(-vn1 * n))

    return vn, vn2


def plot_surface(x_values, y_values, z_values, axes, x_name, y_name, z_name):
    x_values, y_values = numpy.meshgrid(x_values, y_values)

    # axes.plot_surface(x_values, y_values, z_values, cmap=cm.coolwarm)
    # axes.plot_surface(x_values[::2, :], y_values[::2, :], z_values[::2, :], cmap=cm.coolwarm)
    axes.plot_surface(x_values[1::2, :], y_values[1::2, :], z_values[1::2, :], cmap=cm.coolwarm)
    axes.set_xlabel(f"{x_name}")
    axes.set_ylabel(f"{y_name}=2k+1")
    axes.set_title(f"{z_name}({x_name}, {y_name})")


def plot_curves(v2_min, v2_max, x_values, y_values, z_values, axes, x_name, y_name, z_name):
    colors = cm.coolwarm(x_values)
    for i, c in enumerate(colors):
        axes.plot(y_values, z_values[:, i], color=c)

    axes.set_xlabel(f"{y_name}")
    axes.set_ylabel(f"{z_name}")
    axes.set_title(f"{z_name}({x_name}, {y_name})")

    v2, n_values, v = get_v(n_max=y_values.max(), v_min=v2_min, v_max=v2_max, v_slices=1)
    axes.plot(n_values, v[:, 0], 'r')

    v3, n_values, v = get_v(n_min=3, n_max=y_values.max(), v_min=numpy.log1p(0), v_max=numpy.log1p(1), v_slices=2)
    axes.plot(n_values, v.max(axis=1), 'k')
    axes.plot(n_values, v.min(axis=1), 'k')


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


def plot_quivers_2(v2_min, v2_max, axes, n_min=2, n_max=50, v_slices=11):
    n = numpy.arange(n_min, n_max + 1, 1)
    v = numpy.linspace(numpy.log1p(0), numpy.log1p(1), v_slices)

    n, v = numpy.meshgrid(n, v)
    dn = numpy.full(n.shape, 2.)
    vn1 = numpy.log1p(numpy.exp(-v * (n - 1)))
    vn2 = numpy.log1p(numpy.exp(-vn1 * n))
    dv = vn2 - v

    axes.quiver(n, v, dn, dv, scale=2, angles='xy', scale_units='xy', cmap=cm.coolwarm)
    axes.set_xlabel(f"n")
    axes.set_ylabel(f"vn")
    axes.set_title(f"∇vn+2(vn, n)")

    v2, n_values, v = get_v(n_max=n_max, v_min=v2_min, v_max=v2_max, v_slices=1)
    axes.plot(n_values, v[:, 0], 'r')


def plot_vn2(axes, n_min=2, n_max=10, v_min=numpy.log1p(0), v_max=numpy.log1p(1), v_slices=1001):
    n = numpy.arange(n_min, n_max + 1)
    v = numpy.linspace(v_min, v_max, v_slices)

    n_, v_ = numpy.meshgrid(n, v)
    vn1 = numpy.log1p(numpy.exp(-v_ * (n_ - 1)))
    vn2 = numpy.log1p(numpy.exp(-vn1 * n_))

    colors = cm.coolwarm(n/n.max())
    for i, c in enumerate(colors):
        axes.plot(v, vn2[:, i], color=c)

    axes.set_xlabel('vn')
    axes.set_ylabel('vn+2')
    axes.set_title(f"vn+2(vn, n) n={n_min}..{n_max}")
    axes.plot(v, v, color='k')


def main():
    figure = pyplot.figure()
    figure_rows, figure_columns = 2, 3

    axes = figure.add_subplot(figure_rows, figure_columns, 1, projection='3d')
    w1_min, w1_max = get_threshold(partial(get_wn, n=1000))
    print(f"{w1_min} < w1 < {w1_max} ({numpy.exp(w1_min)} < u1 < {numpy.exp(w1_max)})")
    w1_delta = 0.50
    w1, n, w = get_w(n_max=50, w1_min=w1_min - w1_delta, w1_max=w1_max + w1_delta, w1_slices=1001)
    plot_surface(w1, n, w, axes, 'w1', 'n', 'w')

    axes = figure.add_subplot(figure_rows, figure_columns, 2, projection='3d')
    v2_min, v2_max = get_threshold(partial(get_vn, n=1000))
    print(f"{v2_min} < v2 < {v2_max} ({1 / numpy.expm1(v2_max)} < u1 < {1 / numpy.expm1(v2_min)})")
    v2_delta = 0.25
    v1, n, v = get_v(n_max=50, v_min=v2_min - v2_delta, v_max=v2_max + v2_delta, v_slices=1001)
    plot_surface(v1, n, v, axes, 'v2', 'n', 'v')

    v2_delta = 0.25
    v1, n, v = get_v(n_max=50, v_min=v2_min - v2_delta, v_max=v2_max + v2_delta, v_slices=21)
    axes = figure.add_subplot(figure_rows, figure_columns, 3)
    plot_quivers(v, axes, 'v2', 'n', 'v')
    axes = figure.add_subplot(figure_rows, figure_columns, 4)
    plot_curves(v2_min, v2_max, v1, n, v, axes, 'v2', 'n', 'v')

    axes = figure.add_subplot(figure_rows, figure_columns, 5)
    plot_quivers_2(v2_min, v2_max, axes, n_max=50, v_slices=21)

    axes = figure.add_subplot(figure_rows, figure_columns, 6)
    plot_vn2(axes, n_min=2, n_max=8)

    pyplot.show()


if __name__ == "__main__":
    main()
