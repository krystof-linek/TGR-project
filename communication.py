import sys
import re
from main import Graph


def task(graph):
    # zjistime, jestli existuji nasobne hrany
    multiply_edges = graph.is_multigraph()
    # pokud existuji, tak je odstranime
    graph.remove_edges_from_graph(multiply_edges)
    # pokud oba uzly nemaji stejny vystupni a vstupni stupen uzlu, tak to znamena, ze vazba jde pouze jednim smerem
    for e in graph.get_edges():
        if (e.node_from.get_out_degree() != e.node_from.get_in_degree()) \
                and (e.node_to.get_out_degree() != e.node_to.get_in_degree()):
            # prehozenim uzlu vypiseme hranu, ktera chybi
            print(e.node_to.get_name() + ' -> ' + e.node_from.get_name())


g = Graph()

g.set_oriented(True)

i = 0
edge = "e" + str(i)
for line in sys.stdin:
    groups = re.match(r"^Employ:\s(.*)$", line)
    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)
    else:
        groups = re.match(r"^(.*)\s->\s(.*)$", line)
        g.add_edge(groups.group(1), groups.group(2), edge, None)
        i = i + 1
        edge = "e" + str(i)

task(g)
