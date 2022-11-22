import sys
import re
from main import Graph


def task(graph1, graph2):
    # z druheho grafu odstranime shodne hrany
    for e1 in graph1.get_edges():
        for e2 in graph2.get_edges():
            if (e1.node_from.get_name() == e2.node_from.get_name().upper()
                    and e1.node_to.get_name() == e2.node_to.get_name().upper()):
                g2.get_edges().remove(e2)

    # zbyle hrany, ktere neobsahuje prvni graf budou do nej vlozeny
    for e in graph2.get_edges():
        n_from_name = e.node_from.get_name()
        n_to_name = e.node_to.get_name()
        # nejdrive pridame uzly
        graph1.add_node(n_from_name)
        graph1.add_node(n_to_name)
        # nasledne pridame hranu
        graph1.add_edge(n_from_name, n_to_name, e.edge_name, e.edge_value)
    # vypiseme vysledek
    for e in graph1.get_edges():
        print(e.node_from.get_name() + ' -> ' + e.node_to.get_name())


g1 = Graph([], [], False)
g2 = Graph([], [], False)

i = 0

for line in sys.stdin:
    groups = re.match(r"^(.*,\s.*)$", line)

    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            if n.isupper():
                g1.add_node(n)
            if n.islower():
                g2.add_node(n)

    else:
        edge = re.match(r"^(.*\s->\s.*)$", line)
        nodes = edge.group(1).split(" -> ")

        if nodes[0].isupper() and nodes[1].isupper():
            g1.add_edge(nodes[0], nodes[1], "e" + str(i), None)
            i = i + 1
            pattern = '.' + str(i)
        if nodes[0].islower() and nodes[1].islower():
            g2.add_edge(nodes[0], nodes[1], "e" + str(i), None)
            i = i + 1
            pattern = '.' + str(i)

task(g1, g2)
