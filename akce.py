import sys
import re
from main import Graph


def task(graph):
    graph = Graph(graph.get_nodes(), graph.get_edges(), graph.is_oriented())

    max_degree = graph.get_max_degree()

    for node in graph.get_nodes():
        if node.get_degree(graph.is_oriented()) == max_degree:
            print(node.get_name() + " (" + str(int(node.get_degree(graph.is_oriented()))) + ")")


g = Graph()

for line in sys.stdin:
    groups = re.match(r"^Group:\s(.*)$", line)
    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)
    else:
        edge = re.match(r"^.*\s-\s.*$", line)
        nodes = edge.group(0).split(" - ")
        g.add_edge(nodes[0], nodes[1], None, None)

task(g)
