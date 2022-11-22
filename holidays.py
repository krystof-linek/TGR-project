import sys
import re
from main import Graph


def task(graph):
    empty_nodes = graph.get_empty_nodes()

    result = ''

    i = 0
    for n in empty_nodes:
        if i < len(empty_nodes) - 1:
            result = result + n.get_name() + ', '
        else:
            result = result + n.get_name()
        i = i + 1

    print(result)


g = Graph()

g.set_oriented(True)

for line in sys.stdin:
    groups = re.match(r"^Places:\s(.*)$", line)

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
                g.add_edge(nodes_names[i], nodes_names[i + 1], edge + pattern, None)
                i = i + 1
                pattern = '.' + str(i)


task(g)
