
# https://www.ilemaths.net/sujet-atteindre-12-variante-873815.html

# Ces import manquaient
from random import randint

import matplotlib.pyplot as plt


def verif(l, nb):
    # On peut descendre jusqu'au ca sde base len(l) == 0 qui est encore plus simple
    # On peut retourner un booléen ce qui est plus propre que 0 ou 1
    # On peut accèder à une liste par la fin avec des indices négatifs l[n-1] == l[-1]
    if not l:    # Une liste vide est "fausse" dans les tests booléens
        return nb == 0
    return verif(l[:-1], nb-l[-1]) or verif(l[:-1], nb+l[-1])


def suite(nb):
    # Simplification car maintenant verif accepte une liste vide et retourne un booléen
    l = []
    while not verif(l, nb):
        l.append(randint(1, 6))
    return l


def suite_2(nb):
    # Version optimisée de 'suite(nb)'
    # Au lieu de reparcourir tout l'arbre à chaque ajout à la liste, on met à jour seulement les feuilles
    # Il y a beaucoup de feuilles les mêmes (+5-3-5 == -5-3+5 par exemple), on ne garde qu'un exemplaire de chaque feuille (avec un set)
    # On peut encore réduire de moitié le nombre de feuille car si on peut atteindre n alors on peut atteindre -n en inversant les signes
    # Mes tests montre que ce suite_2 tourne 7.4 fois plus vite que suite pour nb==12, 593 fois plus vite pour nb==40
    nb = abs(nb)
    l = []
    numbers = {0}
    while nb not in numbers:
        number = randint(1, 6)
        l.append(number)
        numbers = {abs(n - number) for n in numbers} | {n + number for n in numbers}

    return l


def test(compt, nb):
    n = []
    d = []
    for i in range(compt):
        # l = suite(nb)
        l = suite_2(nb)
        n.append(len(l))
        d.append(l[-1])     # l[-1] est le dernier élément de l
    figure = plt.figure(figsize=(10, 10))
    plt.gcf().subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0.2)
    figure.add_subplot(2, 1, 1)  # On ne fait rien avec 'axes', pas besoin de cette variable
    plt.hist(n, bins=[k+0.5 for k in range(max(n)+1)])  # Centre les barres sur les nombres entiers et ne coupe pas le graphe
    # numerical_approx et mean semblent venir de SageMath qui est compliqué à installer comme une dépendance.
    # Le format .2f arrondi déjà à deux décimales et mean peut être calculé avec des fonctions builtin de python
    # Utiliser les f-strings est plus naturel que str.format
    plt.title(f"Histogramme du nombre d'essais nécessaires avec pour moyenne {sum(n)/len(n):.2f}")
    figure.add_subplot(2, 1, 2)
    plt.hist(d, bins=[k+0.5 for k in range(7)])     # Centre les barres sur les nombres entiers
    plt.title("Histogramme de la valeur du dernier essai")
    plt.show()
    return n, d


if __name__ == "__main__":  # Permet de réutiliser les fonctions de ce module dans un autre module sans lancer le test
    test(100000, 12)
