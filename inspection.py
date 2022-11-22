import sys
import re
from main import Graph


def task(graph):

    move = graph.get_euler_move()

    if move is not None:
        result = "|"
        for e in move:
            result += '-' + e.edge_name + '-|'
        print(result)


def task_graph():
    # funguje
    g.add_edge("Ua", "Ub", "01", None)
    g.add_edge("Ub", "Uc", "02", None)
    g.add_edge("Uc", "Ud", "03", None)
    g.add_edge("Ud", "Uf", "04", None)
    g.add_edge("Uf", "Uc", "05", None)
    g.add_edge("Uc", "Ua", "06", None)
    g.add_edge("Ua", "Uf", "07", None)

    return g


def house_graph():
    # funguje
    g.add_edge("E", "D", "7", None)
    g.add_edge("B", "A", "2", None)
    g.add_edge("A", "C", "1", None)
    g.add_edge("B", "C", "3", None)
    g.add_edge("B", "E", "8", None)
    g.add_edge("B", "D", "4", None)
    g.add_edge("C", "D", "6", None)
    g.add_edge("C", "E", "5", None)

    return g


def video_graph():
    # funguje pokud pri vypisu cesty je index-- ne index++
    g.add_edge("F", "A", "6", None)
    g.add_edge("A", "B", "1", None)
    g.add_edge("B", "C", "2", None)
    g.add_edge("C", "D", "3", None)
    g.add_edge("D", "E", "4", None)
    g.add_edge("E", "F", "5", None)
    g.add_edge("E", "A", "13", None)
    g.add_edge("D", "B", "10", None)
    g.add_edge("D", "I", "11", None)
    g.add_edge("E", "J", "12", None)
    g.add_edge("J", "I", "16", None)
    g.add_edge("I", "H", "15", None)
    g.add_edge("G", "H", "8", None)
    g.add_edge("H", "B", "9", None)
    g.add_edge("A", "G", "7", None)
    g.add_edge("J", "G", "14", None)
    g.add_edge("J", "K", "17", None)
    g.add_edge("I", "K", "18", None)
    g.add_edge("G", "K", "20", None)
    g.add_edge("H", "K", "19", None)

    return g


def test_graph():
    # funguje
    g.add_edge("A", "B", "1", None)
    g.add_edge("B", "C", "2", None)
    g.add_edge("C", "D", "3", None)
    g.add_edge("D", "E", "4", None)
    g.add_edge("E", "F", "5", None)
    g.add_edge("F", "A", "6", None)
    g.add_edge("A", "D", "7", None)
    g.add_edge("E", "B", "8", None)
    g.add_edge("D", "B", "9", None)
    g.add_edge("E", "A", "10", None)

    return g


g = Graph([], [], False)

#task_graph()
#house_graph()
#video_graph()
#test_graph()

bad_input = False
for line in sys.stdin:
    groups = re.match(r"^\s*(.+)\s+\|-(\d+)-\|\s+(.+)\s*$", line)
    if groups:
        node_from = groups.group(1)
        node_to = groups.group(3)
        edge_name = groups.group(2)
        # orientovane v obou smerech
        g.add_edge(node_from, node_to, edge_name, None)
    else:
        bad_input = True

if bad_input:
    print("chybny format vstupu")
else:
    task(g)
