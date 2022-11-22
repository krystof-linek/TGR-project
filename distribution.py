import sys
import re
from main import Graph


def task(graph):
    graph = Graph(graph.get_nodes())

    max_out_degree = graph.get_node_with_max_out_degree()
    max_in_degree = graph.get_node_with_max_in_degree()

    print('Export: ' + max_out_degree.get_name() + ' (' + str(max_out_degree.get_out_degree()) + ')')
    print('Import: ' + max_in_degree.get_name() + ' (' + str(max_in_degree.get_in_degree()) + ')')


g = Graph()

g.set_oriented(True)

for line in sys.stdin:
    groups = re.match(r"^Store:\s(.*)$", line)

    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)
    else:
        groups = re.match(r"^(.*):\s(.*)$", line)

        if groups:
            edge = groups.group(1)
            nodes = groups.group(2).split(' -> ')
            g.add_edge(nodes[0], nodes[1], edge, None)

task(g)
