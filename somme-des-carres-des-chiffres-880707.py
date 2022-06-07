
# See https://www.ilemaths.net/sujet-somme-des-carres-des-chiffres-880707.html

import networkx
from matplotlib import pyplot


def get_sum_digits(n, base=10, power=1):
    s = 0
    while n:
        n, d = divmod(n, base)
        s += d**power
    return s


def get_nodes(limit=100):
    nodes = set()
    new_nodes = set(range(1, limit))
    while new_nodes:
        node = new_nodes.pop()
        nodes.add(node)
        node_sum = get_sum_digits(node, power=2)
        if node_sum not in nodes:
            new_nodes.add(node_sum)
    return nodes


def main():
    nodes = get_nodes(20)

    graph = networkx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from([(node, get_sum_digits(node, power=2)) for node in nodes])

    networkx.draw_planar(graph, with_labels=True)
    pyplot.show()


if __name__ == "__main__":
    main()
