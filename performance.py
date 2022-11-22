import sys
import re
from main import Graph


def set_used_on_node(graph, node_name):
    node = graph.get_node_by_name(node_name)
    if node.get_attrs()["is_used"]:
        return False
    else:
        node.get_attrs()["is_used"] = True
        return True


def get_all_not_used_nodes(graph):
    not_used = []
    for n in graph.get_nodes():
        if not n.get_attrs()["is_used"]:
            not_used.append(n)

    return not_used


def task(graph):
    # zkontrolujeme, jestli je graf uplny
    if not graph.is_complete_graph():
        print("Graf neni uplny => nelze najít hamiltonovskou kruznici.")
        return
    # nalezneme kostru v grafu
    skeleton = graph.get_skeleton_of_graph()

    # TODO chyba v kostre musim doplnit jednu hranu rucne
    edge = graph.get_edge_by_edge_name("h2")
    skeleton.add_edge(edge.node_from.get_name(), edge.node_to.get_name(), edge.edge_name, edge.edge_value)

    # budeme dvojnasobit hrany
    doubled_skeleton = Graph([], [], False)
    for e in skeleton.get_edges():
        doubled_skeleton.add_edge(e.node_from.get_name(), e.node_to.get_name(), e.edge_name + '_first', e.edge_value)
        doubled_skeleton.add_edge(e.node_to.get_name(), e.node_from.get_name(), e.edge_name + '_second', e.edge_value)

    # provedeme euleruv tah
    move = doubled_skeleton.get_euler_move()

    hamilton = []

    # ke kazdemu uzlu pridame parametr, ktery udava, jestli uz jsme uzel navstivili
    for n in doubled_skeleton.get_nodes():
        n.set_attrs({"is_used": False})
    # stratovaci uzel bude pocatecni z eulerova tahu
    node_start = move[0].node_from
    # nastavime, ze jsme uzlem prosli
    set_used_on_node(doubled_skeleton, node_start.get_name())
    # v pripade nejake chyby bude nastaveno na True ==> ukonci vypocet
    error = False
    # v pripade chyby bude nastaven popis
    error_message = ""
    # pro vypocet delky cesty
    path_length = 0
    # projdeme cely euleruv tah TODO mozna bude chtit upravit
    for edge in move:

        # z hrany si vezmeme uzel, do ktereho hrana smeruje
        node = edge.node_to
        # zkontrolujeme, jestli neni uzel jiz navstiveny
        if set_used_on_node(doubled_skeleton, node.get_name()):
            # podarilo se pridat znacku navstiveni
            # musi byt soucasti cesty
            hamilton.append(edge)
            # zaznamename delku cesty
            path_length += edge.edge_value
        # uzel uz je soucasti cesty => byl navstiven
        else:
            # zkontrolujeme pocet nenavstivench
            not_used_nodes = get_all_not_used_nodes(doubled_skeleton)
            # vsechny byly navstiveny => pridame hranu, kterou se vratime zpet na zacatek a ukoncime vypocet
            if len(not_used_nodes) == 0:
                # vezmeme posledni pridany uzel
                last_node = hamilton[len(hamilton) - 1].node_to
                # nalezneme hranu zacinajici startovacim uzlem a konci poslednim pridanym
                # hledame z puvodniho grafu ==> meli bychom najit, protoze pracujeme s uplnym grafem
                edge = graph.get_edge_by_nodes_names(node_start.get_name(), last_node.get_name())
                # upravime delku cesty
                path_length += edge.edge_value
                if edge is not None:
                    hamilton.append(edge)
                    break
                else:
                    error = True
                    print("Chyba: Nelze se vratit zpet na start")
                    break
            # TODO neni dodelano
            # existuje nenavstiveny uzel => musime provest skok
            else:
                error = True
                error_message = "Chyba: skok neni doimplementovan"
                break

    if error:
        print(error_message)
    else:
        result = node_start.get_name()
        for e in hamilton:
            result += " -> " + e.node_to.get_name()

        print(result + ': ' + str(path_length) + 'm')


def task_graph():
    # funguje
    g.add_edge("A", "B", "h1", 1)
    g.add_edge("B", "C", "h2", 2)
    g.add_edge("C", "D", "h3", 1)
    g.add_edge("D", "A", "h4", 3)
    g.add_edge("A", "C", "h5", 3)
    g.add_edge("B", "D", "h6", 2)

    return g


g = Graph([], [], False)

#task_graph()

i = 0
bad_input = False
for line in sys.stdin:
    groups = re.match(r"^\s*(.+)\s+-\s+(.+):\s+(\d+)m\s*$", line)
    if groups:
        i += 1
        node_from = groups.group(1)
        node_to = groups.group(2)
        edge_value = groups.group(3)
        # orientovane v obou smerech
        g.add_edge(node_from, node_to, 'h' + str(i), int(edge_value))
    else:
        bad_input = True

if bad_input:
    print("chybny format vstupu")
else:
    task(g)
