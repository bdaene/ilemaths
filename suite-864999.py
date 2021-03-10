
# See subject at https://www.ilemaths.net/sujet-suite-864999.html

"""
La suite de Conway
"""

from itertools import groupby, islice


def gen_conway(germe):
    """Génère la suite de Conway à partir du germe"""
    while True:
        yield germe
        germe = ''.join(f"{len(tuple(g))}{c}" for c, g in groupby(germe))


def main():
    """Entrée principale du programme"""
    germe = input("Donner le premier terme de la suite de Conway : ")
    n = int(input("Combien de termes voulez-vous calculer ? "))

    for i, terme in enumerate(islice(gen_conway(germe), n+1)):
        print(f"terme numéro {i}: \t{terme}")


if __name__ == "__main__":
    main()
