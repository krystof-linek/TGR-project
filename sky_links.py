import sys
import re
from main import Graph


def task(graph):
    multiply_edges = graph.is_multigraph()

    if len(multiply_edges) > 0:
        for me in multiply_edges:
            print(me.node_from.get_name() + ' -> ' + me.node_to.get_name())


g = Graph()

g.set_oriented(True)

for line in sys.stdin:
    groups = re.match(r"^City:\s(.*)$", line)
    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)
    else:
        groups = re.match(r"^(.*):\s(.*)$", line)

        if groups:
            edge = groups.group(1)
            nodes_names = groups.group(2).split(' -> ')

            i = 0
            pattern = "." + str(i)
            while i < len(nodes_names) - 1:
                g.add_edge(nodes_names[i], nodes_names[i+1], edge + pattern, None)
                i = i + 1
                pattern = '.' + str(i)

task(g)
