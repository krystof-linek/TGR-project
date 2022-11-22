import sys
import re
from main import Graph


# kostra = Kruskaluv algoritmus
def task(graph):
    for e in graph.get_skeleton_of_graph().get_edges():
        print(e.node_from.get_name() + ' - ' + e.node_to.get_name())


g = Graph([], [], False)

i = 1
for line in sys.stdin:
    groups = re.match(r"^CPU:\s(.*)$", line)
    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)
    else:
        groups = re.match(r"^(.*)\s-\s(.*):\s(\d+)s$", line)

        if groups:
            node_from = groups.group(1)
            node_to = groups.group(2)
            edge_value = groups.group(3)

            g.add_edge(node_from, node_to, "h" + str(i), edge_value)
            i += 1

task(g)
