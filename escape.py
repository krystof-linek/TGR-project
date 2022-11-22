import sys
import re
import random
from main import Graph


# bludiste = Tarryho algoritmus
def task(graph):
    result = []

    nodes = graph.get_nodes()

    # startovaci uzel
    start_node = nodes[0]
    # konceny uzel
    end_node = nodes[len(nodes)-1]

    # pocitadlo pro jistotu, aby nedoslo k zacykleni
    count = 0
    # inicializace pocatecniho uzlu
    next_node = start_node
    # pokud nekde resitelnost bude vyhodnocena jako False ==> ukonci se vypocet
    is_solvable = True
    # dokud nedojdeme ke koncovemu uzlu nebo pokud pocitadlo dosahne 100 cyklu
    while is_solvable and count < 200 and next_node != end_node:
        # z jakeho uzlu pujdeme
        from_node = next_node
        # najdeme si sousedy
        neighbours = graph.get_neighbours(from_node)
        # sousedi, co nemaji zadnou znacku
        neighbours_without_mark = []

        # projde vsechny sousedy a vytvori seznam vsech, co nemaji znacku (IN ani OUT)
        for n in neighbours:
            if not n.mark_out and not n.mark_in:
                neighbours_without_mark.append(n)

        # pokud delka seznamu neni 0 tak existuji sousedi, co nemaji znacky
        if len(neighbours_without_mark) != 0:
            # nahodne vybere jednoho z neoznackovanych
            index = random.randint(0, len(neighbours_without_mark) - 1)
            next_node = neighbours_without_mark[index].node_to
            # ulozime si nazev hrany
            edge = neighbours_without_mark[index].edge_name
            # pridame vystupni znacku
            graph.get_edge_by_nodes_and_edge_name(from_node, next_node, edge).set_mark_out()
            # zjistime, jestli uz jedna z hran souseda neni oznacena jako IN
            neighbours = graph.get_neighbours(next_node)
            has_in_mark = False
            for n in neighbours:
                if n.mark_in:
                    has_in_mark = True
            # pokud neni oznacena, tak jsme vstoupili do nove mistnosti a oznacime si (dvere) jako IN
            # v pripade startovaciho uzlu nemuzu dat zadne IN
            if not has_in_mark and next_node != start_node:
                graph.get_edge_by_nodes_and_edge_name(next_node, from_node, edge).set_mark_in()
        else:
            # pokud vsichni maji znacku a jsme ve startovacim uzlu, tak uloha nema reseni => vsechny znacky jsou OUT
            if next_node == start_node:
                is_solvable = False
            else:
                # pokud vsichni maji jiz znacku, tak se vrat zpet pres IN
                for n in neighbours:
                    if n.mark_in:
                        next_node = n.node_to

        result.append(from_node.get_name() + ' -> ' + next_node.get_name())
        count += 1

    if is_solvable:
        for r in result:
            print(r)
    else:
        print("Neni cesta ven!")


g = Graph([], [], False)

i = 1
for line in sys.stdin:
    groups = re.match(r"^Sections:\s(.*)$", line)
    if groups:
        nodes = groups.group(1).split(", ")

        for n in nodes:
            g.add_node(n)
    else:
        groups = re.match(r"^(.*)\s-\s(.*)$", line)

        if groups:
            node_from = groups.group(1)
            node_to = groups.group(2)

            g.add_edge(node_from, node_to, "h" + str(i), 1)
            g.add_edge(node_to, node_from, "h" + str(i), 1)
            i += 1

task(g)
