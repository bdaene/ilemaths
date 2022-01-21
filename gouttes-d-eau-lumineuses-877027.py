# https://www.ilemaths.net/sujet-gouttes-d-eau-lumineuses-877027.html

import numpy
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation


class Scene:

    def __init__(self, nb_light_strips=64, nb_led_per_strip=16, tree_size=16):
        self.strip_positions = numpy.random.randn(3, nb_light_strips) * tree_size
        self.led_positions = numpy.empty((3, nb_light_strips * nb_led_per_strip), dtype=self.strip_positions.dtype)
        for i in range(nb_led_per_strip):
            self.led_positions[:2, i*nb_light_strips:(i+1)*nb_light_strips] = self.strip_positions[:2, :]
            self.led_positions[2, i * nb_light_strips:(i + 1) * nb_light_strips] = self.strip_positions[2, :] - i
        self.strip_states = numpy.full((nb_led_per_strip, nb_light_strips), False)

        self.figure = pyplot.figure(figsize=(16, 9))
        axes = self.figure.add_axes([0, 0, 1, 1], projection='3d', autoscale_on=0.5)
        axes.set_axis_off()
        view_size = tree_size * 1.5
        axes.set_xlim(-view_size, view_size)
        axes.set_ylim(-view_size, view_size)
        axes.set_zlim(-view_size - nb_led_per_strip, view_size)
        self.scatter = axes.scatter(self.led_positions[0, :], self.led_positions[1, :], self.led_positions[2, :],
                                    vmin=0, vmax=1, linewidth=0, s=32, alpha=0.75)
        self.scatter.set_cmap('Blues_r')

    def update(self, frame_number):
        self.strip_states[1:, :] = self.strip_states[:-1, :]
        self.strip_states[0, :] = False

        numbers = numpy.random.randint(256, size=self.strip_states.shape[1])
        for i, number in enumerate(numbers):
            if number < self.strip_states.shape[0]:
                self.strip_states[number, i] = True

        self.scatter.set_array(self.strip_states.flatten())


def main(save=False):
    scene = Scene()
    animation = FuncAnimation(scene.figure, scene.update, interval=125)
    if save:
        animation.save('gouttes.gif', fps=8, dpi=32)
    else:
        pyplot.show()


if __name__ == "__main__":
    main()
