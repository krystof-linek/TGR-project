import sys
import re
from main import Graph


def task(graph):
    nodes_with_loop = graph.get_loops()

    result = ""

    count = 0
    for node in nodes_with_loop:
        count += 1

        if count == len(nodes_with_loop):
            result = result + node.get_name()
        else:
            result = result + node.get_name() + ', '

    print(result)


g = Graph()

g.set_oriented(True)

for line in sys.stdin:
    groups = re.match(r"^Guideposts:\s(.*)$", line)
    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)
    else:
        groups = re.match(r"^(.*):\s(.*)$", line)

        if groups:
            edge = groups.group(1)
            nodes = groups.group(2).split(' -> ')

            i = 0
            pattern = "." + str(i)
            while i < len(nodes) - 1:
                g.add_edge(nodes[i], nodes[i+1], edge + pattern, None)
                i = i + 1
                pattern = '.' + str(i)

task(g)
