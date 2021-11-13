
# https://www.ilemaths.net/sujet-atteindre-12-variante-873815.html

import matplotlib.pyplot as plt


def verif(l, nb):
    n = len(l)
    if n == 1:
        if l[0] == nb:
            return 1
        else:
            return 0
    else:
        return verif(l[:n - 1], nb - l[n - 1]) or verif(l[:n - 1], nb + l[n - 1])


def suite(nb):
    l = [randint(1, 6)]
    while verif(l, nb) != 1: l.append(randint(1, 6))
    return l


def test(compt, nb):
    n = []
    d = []
    for i in range(compt):
        l = suite(nb)
        n.append(len(l))
        d.append(l[len(l) - 1])
    figure = plt.figure(figsize=(10, 10))
    plt.gcf().subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0.2)
    axes = figure.add_subplot(2, 1, 1)
    plt.hist(n, bins=range(15))
    plt.title("Histogramme du nombre d'essais nécessaires avec pour moyenne {:.2f}".format(numerical_approx(mean(n))))
    axes = figure.add_subplot(2, 1, 2)
    plt.hist(d, bins=range(8))
    plt.title("Histogramme de la valeur du dernier essai")
    plt.show()
    return n, d


test(10000, 12)
