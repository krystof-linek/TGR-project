import sys
import re
from main import Graph


def task(graph):
    # ziska seznam mostu
    briges = graph.get_bridges_of_graph()
    # ziska seznam artikulaci
    articulations = graph.get_articulations_of_graph()
    # prazdne seznamy => neni artikulace a ani most
    if len(articulations) == 0 and len(briges) == 0:
        print("Zadna")
    else:
        # vypis mostu
        for edge in graph.get_edges():
            for b in briges:
                if edge.edge_name == b.edge_name:
                    print(edge.node_from.get_name() + ' -> ' + edge.node_to.get_name())
        # vypis artikulaci
        for node in articulations:
            print(node.get_name())


def test_graph():

    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    g.add_node("F")
    g.add_node("G")

    g.add_edge("A", "C", "h1", None)
    g.add_edge("A", "B", "h2", None)
    g.add_edge("B", "C", "h3", None)
    g.add_edge("C", "D", "h4", None)
    g.add_edge("D", "G", "h7", None)
    g.add_edge("D", "F", "h5", None)
    g.add_edge("D", "E", "h6", None)
    g.add_edge("G", "F", "h8", None)
    g.add_edge("G", "E", "h9", None)

    return g


def test_graph_bridge():

    g = Graph([], [], False)

    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    g.add_node("F")
    g.add_node("G")
    g.add_node("H")

    g.add_edge("A", "B", "h9", None)
    g.add_edge("A", "D", "h1", None)
    g.add_edge("D", "C", "h7", None)
    g.add_edge("D", "E", "h2", None)
    g.add_edge("E", "H", "h6", None)
    g.add_edge("E", "F", "h3", None)
    g.add_edge("E", "G", "h5", None)
    g.add_edge("F", "G", "h4", None)
    g.add_edge("C", "B", "h8", None)

    return g


g = Graph([], [], False)

for line in sys.stdin:
    groups = re.match(r"^City:\s(.*)$", line)
    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)
    else:
        groups = re.match(r"^(.*):\s*(.*)\s*$", line)

        if groups:
            edge_name = groups.group(1)
            nodes = groups.group(2).split(' -> ')

            i = 0
            pattern = "." + str(i + 1)
            while i < len(nodes) - 1:
                g.add_edge(nodes[i], nodes[i + 1], edge_name + pattern, None)
                i = i + 1
                pattern = '.' + str(i + 1)


task(g)
