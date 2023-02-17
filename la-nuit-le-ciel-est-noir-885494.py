# See subject at https://www.ilemaths.net/sujet-la-nuit-le-ciel-est-noir-885494.html

from cmath import phase
from itertools import count
from math import sin, cos, ceil, pi, asin

from matplotlib import pyplot
from matplotlib.patches import Polygon, Circle


def project(point, angle):
    sin_a, cos_a = sin(angle), cos(angle)
    d = point.real * sin_a - point.imag * cos_a
    return point + d * (-sin_a + 1j * cos_a)


def draw_sun(axes, min_angle: float, max_angle: float, center: complex, radius: float):
    t_min, t_max = project(center, min_angle), project(center, max_angle)
    axes.add_patch(Polygon([(0, 0), (t_min.real, t_min.imag), (t_max.real, t_max.imag)], facecolor='y'))
    axes.add_patch(Circle((center.real, center.imag), radius, facecolor='r'))


def find_next_sun(min_angle, max_angle, radius, left_sun):
    sin_a, cos_a = sin(min_angle), cos(min_angle)
    sin_b, cos_b = sin(max_angle), cos(max_angle)

    min_x, min_y = 1 + round(left_sun.real), round(left_sun.imag)
    for y in count(min_y):
        x = max(min_x, ceil((y * cos_b - radius) / sin_b))
        d = x * sin_a - y * cos_a
        if d < radius - 1e-9:
            return x + y * 1j


def find_all_suns(radius):
    intervals = [(0, pi / 4, 0 + 0j)]

    while intervals:
        min_angle, max_angle, left_sun = intervals.pop()
        sun = find_next_sun(min_angle, max_angle, radius, left_sun)
        angle = phase(sun)
        delta_angle = asin(radius / abs(sun))
        min_sun_angle = angle - delta_angle
        max_sun_angle = angle + delta_angle

        yield sun, max(min_angle, min_sun_angle), min(max_sun_angle, max_angle)

        if max_sun_angle < max_angle:
            intervals.append((max_sun_angle, max_angle, left_sun))
        if min_angle < min_sun_angle:
            intervals.append((min_angle, min_sun_angle, sun))


def get_sky_horizon(radius):
    return max(abs(sun) for sun, min_angle, max_angle in find_all_suns(radius))


def plot_horizons(radii, axis):
    horizons = [get_sky_horizon(radius) for radius in radii]

    axis.set_xscale('log')
    axis.set_yscale('log')
    axis.set_xlabel('1/radius')
    axis.set_ylabel('horizon')
    axis.plot([1 / radius for radius in radii], horizons, '+r')
    axis.plot([0, 1 / min(radii)], [0, 1 / min(radii)], 'k')


def draw_sky(radius, axis):
    axis.set_title(f"{radius=}")
    axis.set_xlim(0, 1 / radius)
    axis.set_ylim(0, sin(pi / 4) / radius)

    for sun, min_angle, max_angle in find_all_suns(radius):
        draw_sun(axis, min_angle, max_angle, sun, radius)


def main():
    figure, axes = pyplot.subplots(ncols=2)
    plot_horizons([0.95 ** i for i in range(100)], axis=axes[1])
    draw_sky(radius=0.1, axis=axes[0])
    pyplot.show()


if __name__ == "__main__":
    main()
