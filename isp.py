import sys
import re
from main import Graph


def task(graph):
    # nejkratsi cesta = dijkstruv algoritmus
    graph = graph.dijkstras_algoritmh()
    # pouze vypis
    for n in graph.get_nodes():

        parent = n.get_attrs()["parent"]
        way = []
        count_error = 0
        while parent != '-' and count_error < 500:
            count_error += 1
            for node in graph.get_nodes():
                if parent == node:
                    way.append(parent.get_name())
                    parent = node.get_attrs()["parent"]
        way.reverse()
        # vypis cesty
        way_result = "["
        for name in way:
            way_result += name + ' -> '
        way_result += n.get_name() + "]"
        # kompletni vypis
        print(n.get_name() + ': ' + str(n.get_attrs()["length_path"]) + 'm, cesta: ' + way_result) \
            if n.get_attrs()["parent"] != '-' else print(n.get_name())


g = Graph([], [], True)

i = 1
bad_input = False
negative_edge_value = False
error_message = ""
for line in sys.stdin:
    groups = re.match(r"^\s*(.+)\s+-\s+(.+):\s+(-*\d+)m\s*$", line)
    if groups:
        node_from = groups.group(1)
        node_to = groups.group(2)
        edge_value = groups.group(3)
        if int(edge_value) < 0:
            negative_edge_value = True
            error_message = "Graf obsahuje záporně ohodnocené hrany ==> nelze použít Dijkstův algoritmus."
        # orientovane v obou smerech
        g.add_edge(node_from, node_to, "h" + str(i), int(edge_value))
        i += 1
        g.add_edge(node_to, node_from, "h" + str(i), int(edge_value))
        i += 1
    else:
        bad_input = True
        error_message = "chybny format vstupu"

if negative_edge_value:
    print(error_message)
elif bad_input:
    print(error_message)
else:
    task(g)
