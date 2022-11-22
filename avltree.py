import sys
import re
from tree import AVLTree


def task(tree, node):
    # ziskame seznam uzlu po hladinach
    level_order = tree.level_order(node)

    # odstrani vsechny posledni None ==> kvuli vypisu
    index = len(level_order) - 1
    while level_order[index] is None and index >= 0:
        level_order.pop(index)
        index -= 1
    # zde budeme stavet vypis
    result = ""
    # pouzivam pro sestaveni oddelitek mezi hladinami
    count = 1
    nodes_on_level = 1
    # sestavovani vypisu
    for item in level_order:
        count += 1
        # pokud je None ==> '_' reseno uz va main
        value = tree.get_value_of_node_to_str(item)
        # pouze pro odliseni vypisu
        if len(level_order) == 1:
            result += value
        else:
            result += value
            if nodes_on_level * 2 == count:
                result += '|'
                nodes_on_level *= 2
            else:
                result += ' '
    # pokud je posledni znak |, tak ho nevypiseme
    if result[-1] == '|':
        print(result[:-1])
    else:
        print(result)


tree = AVLTree()

node = None

for line in sys.stdin:
    groups = re.match(r"^\s*(\d+)\s*$", line)
    if groups:
        value = groups.group(1)

        node = tree.add_node(node, int(value))

    task(tree, node)
