class AVLNode:
    def __init__(self, value):
        self.left_child = None
        self.right_child = None
        self.value = value
        self.height = 1


class AVLTree:

    # funkce vrati vysku uzlu, pokud je uzel None vraci se 0
    def get_height(self, node):
        if node is None:
            return 0
        else:
            return node.height

    # funkce vypocita novou vysku uzlu
    def calculate_new_height(self, right_node, left_node):
        return 1 + max(self.get_height(right_node), self.get_height(left_node))

    def calculate_koef_of_node(self, node):
        """
        Funkce vypocita koeficient vysek podle, ktereho budeme uvazovat, jestli je potreba rotovat
        :param node: node, pro ktery budeme pocitat koeficient
        :return: vypocitame vysku leveho minus praveho
        """
        # pokud je uzel node None, tak nebudeme nic pocitat
        if node is None:
            return 0
        else:
            return self.get_height(node.left_child) - self.get_height(node.right_child)

    def rotate_right(self, node):
        """
        Funkce slouzi k provedeni prave rotace
        :param node: uzel, u ktereho chceme rotovat
        :return: vraci leveho potomka uzlu
        """
        # ulozime si leveho potomka uzlu
        lchild = node.left_child
        # ulozime si praveho potomka z leveho potomka (radek vyse)
        lchild_rchild = lchild.right_child
        # provedeme samotnou rotaci
        # pravy potomek leveho potomka bude uzel z parametru
        lchild.right_child = node
        # levy potomek node bude puvodni pravy potomek jeho leveho potomka
        node.left_child = lchild_rchild

        # prepocitame vysky, pozor zalezi na poradi !!!
        node.height = self.calculate_new_height(node.right_child, node.left_child)
        lchild.height = self.calculate_new_height(lchild.right_child, lchild.left_child)

        return lchild

    def rotate_left(self, node):
        """
        Funkce slouzi k provedeni leve rotace ==> obdoba prave
        :param node: uzel, u ktereho chceme rotovat
        :return: vraci praveho potomka uzlu
        """
        # ulozime si praveho potomka uzlu
        rchild = node.right_child
        # ulozime si leveho potomka z praveho potomka (radek vyse)
        rchild_lchild = rchild.left_child
        # provedeme samotnou rotaci
        # levy potomek praveho potomka bude uzel z parametru
        rchild.left_child = node
        # pravy potomek node bude puvodni levy potomek jeho praveho potomka
        node.right_child = rchild_lchild

        # prepocitame vysky, pozor zalezi na poradi !!!
        node.height = self.calculate_new_height(node.right_child, node.left_child)
        rchild.height = self.calculate_new_height(rchild.right_child, rchild.left_child)

        return rchild

    def add_node(self, node, value):
        """
        Funkce slouzi k pridani noveho uzlu. Postup pridavani je stejny, jako v pripade klasickho binarniho
        vyhledavaciho stromu. Vetsi a stejne hodnoty jsou v pravem podstromu mensi jsou v levem.
        
        Zmena prichazi az potom, kdy je potreba po kazdem pridani prepocitat vysky 
        a provest kombinace rotaci (pokud je to potreba)
        :param node: node (zaciname korenem) 
        :param value: hodnota, ktera ma byt pridana do stromu
        :return:
        """
        # prochazime pomoci rekurze
        # jakmile dojdeme na None ==> vytvorime novy uzel a pridame data
        if node is None:
            return AVLNode(value)
        elif value >= node.value:
            node.right_child = self.add_node(node.right_child, value)
        else:
            node.left_child = self.add_node(node.left_child, value)

        # prepocitame vysky (rekurze, takze se to propocita pro vsechny)
        node.height = self.calculate_new_height(node.right_child, node.left_child)
        # vypocitame si koeficient, podle ktereho budeme urcovat, jestli je potreba rotace a pripadne jaka
        koeficient = self.calculate_koef_of_node(node)

        # pokud je koeficient vetsi nez jedna ==> levy podstrom ma vetsi vysku - rotovat doprava
        if koeficient > 1:
            # ---- rotace vpravo ---- #
            # pokud je hodnota uzlu mensi nez hodnota leveho potomka staci rotovat jednou
            if value < node.left_child.value:
                return self.rotate_right(node)
            # ---- rotace vlevo vpravo ---- #
            # pokud je hodnota uzlu vetsi nez je hodnota leveho potomka musime ho nechat zrotovat doleva
            if value > node.left_child.value:
                node.left_child = self.rotate_left(node.left_child)
                return self.rotate_right(node)
        # pokud je koeficient mensi nez jedna ==> pravy podstrom ma vetsi vysku - rotovat doleva
        if koeficient < -1:
            # ---- rotace vlevo ---- #
            # pokud je hodnota uzlu vetsi nez hodnota praveho potomka staci rotovat jednou
            if value > node.right_child.value:
                return self.rotate_left(node)
            # ---- rotace vpravo vlevo ---- #
            # pokud je hodnota uzlu mensi nez je hodnota praveho potomka musime ho nechat zrotovat doprava
            if value < node.right_child.value:
                node.right_child = self.rotate_right(node.right_child)
                return self.rotate_left(node)

        return node

    def get_value_of_node_to_str(self, node):
        """
        Funkce pouze ziska hodnotu z uzlu, pokud je None, tak vrati '_' ==> ve formatu, jak je zadani z cviceni
        :param node: uzel pro vypis
        :return: hodnotu
        """
        if node is None:
            return '_'
        else:
            return str(node.value)

    def level_order(self, root):
        """
        Funkce zpracuje strom po jeho hladinach (urovni)
        :param root: koren stromu
        :return: vraci seznam zpracovanych uzlu a obsahuje i None (jsou potrebne pro vypis)
        """
        queue = [root]

        level_order = []

        while len(queue) != 0:
            root = queue.pop(0)

            if not root:
                level_order.append(None)
                continue
            else:
                level_order.append(root)
                queue.append(root.left_child)
                queue.append(root.right_child)
        return level_order
