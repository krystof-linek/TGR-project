import sys
import re
from main import Graph


def task(graph):
    print(graph.is_complete_graph())


g = Graph()

for line in sys.stdin:
    groups = re.match(r"^Employ:\s(.*)$", line)
    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)

    else:
        groups = re.match(r"^(.*):\s(.*)$", line)

        if groups:
            edge = groups.group(1)
            nodes = groups.group(2).split(', ')

            # pro kazdeho musime pridat s kym uz pracoval
            # posledniho zpracovat nemusime, jelikoz uz je zpracovan z predchozich kroku
            # v teto casti se zpracovava radek, ktery odpovida jednomu projektu

            nodes_completed = []

            for n1 in nodes:
                # kazdy uzel ma hranu s kazdym uzlem
                for n2 in nodes:
                    # kontrola, jestli se sobe uzly nerovnaji, nebo jestli uz uzel neni zpracovan
                    if n1 != n2 and n2 not in nodes_completed:
                        g.add_edge(n1, n2, edge, None)
                # tento uzel je uz zpracovan
                nodes_completed.append(n1)

task(g)
