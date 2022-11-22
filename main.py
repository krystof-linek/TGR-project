from collections import namedtuple
import copy
import math


class Node:
    def __init__(self, name, in_degree=0, out_degree=0):
        self.name = name
        self.in_degree = in_degree
        # pokud je neorientovany ukladame pouze sem
        self.out_degree = out_degree
        # pro bludiste
        self.naslednici = []
        self.attrs = None

    def set_attrs(self, attr):
        self.attrs = attr

    def get_attrs(self):
        return self.attrs

    def addNaslednik(self, node):
        self.naslednici.append(node)

    def getNasledniky(self):
        return self.naslednici

    def __repr__(self):
        return '{ ' + str(self.get_name()) + ' ,out_degree: ' + str(self.get_out_degree()) + ' , in_degree: ' \
               + str(self.get_in_degree()) + ', attrs: ' + str(self.attrs) + ' }'

    def get_name(self):
        return self.name

    def get_degree(self, is_oriented):
        if is_oriented:
            return self.out_degree + self.in_degree
        else:
            return self.out_degree

    def get_out_degree(self):
        return self.out_degree

    def get_in_degree(self):
        return self.in_degree

    def inc_degree(self, is_oriented):
        if is_oriented:
            self.out_degree += 1
            self.in_degree += 1
        else:
            self.out_degree += 1

    def inc_out_degree(self):
        self.out_degree += 1

    def inc_in_degree(self):
        self.in_degree += 1

    def dec_degree(self, is_oriented):
        if is_oriented:
            self.out_degree -= 1
            self.in_degree -= 1
        else:
            self.out_degree -= 1

    def dec_out_degree(self):
        self.out_degree -= 1

    def dec_in_degree(self):
        self.in_degree -= 1


#Edge = namedtuple('Edge', ['node_from', 'node_to', 'edge_name', 'edge_value'])

class Edge:
    def __init__(self, node_from, node_to, edge_name, edge_value):
        self.node_from = node_from
        self.node_to = node_to
        self.edge_name = edge_name
        self.edge_value = edge_value
        # bludiste
        self.mark_in = False
        self.mark_out = False
        self.attrs = {}

    def set_attrs(self, attr):
        self.attrs = attr

    def get_attrs(self):
        return self.attrs

    def set_mark_in(self):
        self.mark_in = True

    def set_mark_out(self):
        self.mark_out = True

    def __repr__(self):
        return 'node_from: ' + self.node_from.get_name() + ', node_to: ' + self.node_to.get_name() + \
               ', edge_name: ' + self.edge_name + ', edge_value: ' + str(self.edge_value) + ', marks (in: ' + \
               str(self.mark_in) + ' out: ' + str(self.mark_out) + ')' + ', attrs: ' + str(self.attrs)


class Graph:

    def __init__(self, nodes=[], edges=[], is_oriented=False):
        self.__nodes = nodes
        self.__edges = edges
        self.__is_oriented = is_oriented

    def __repr__(self):
        return 'Graf{ ' + str(self.__edges) + '}'

    def get_nodes(self):
        return self.__nodes

    def get_node_by_name(self, name):
        for n in self.get_nodes():
            if n.get_name() == name:
                return n

    def get_empty_nodes(self):
        """
        Funkce hleda prazdne uzly v grafu.
        :return: vraci pole s prazdnymi uzly, pokud zadne nejsou ==> pole je prazdne
        """
        g = Graph(self.__nodes, self.__edges, self.__is_oriented)

        empty_nodes = []
        for n in g.get_nodes():
            if n.get_degree(g.is_oriented()) == 0:
                empty_nodes.append(n)

        return empty_nodes

    def get_edges(self):
        return self.__edges

    def is_oriented(self):
        return self.__is_oriented

    def set_oriented(self, value):
        self.__is_oriented = value

    def get_node_by_name(self, node_name):
        """
        Funkce slouzi k vyhledani uzlu na zaklade jeho jmena.
        :param node_name: jmeno uzlu
        :return: pokud uzel existuje, tak ho vrati, jinak vraci None
        """

        node = None

        for n in self.get_nodes():
            if n.get_name() == node_name:
                node = n

        return node

    def add_node(self, node_name):
        """
        Funkce prida novy uzel do kopie puvodniho grafu, vraci tedy novy graf => nedochazi k uprave puvodniho
        :param node_name: uzel, ktery ma byt pridan
        :return: novy graf s pridanym uzlem
        """

        g = Graph(self.get_nodes(), self.get_edges(), self.is_oriented())

        g = g.get_nodes().append(Node(node_name))

        return g

    def remove_node(self, node):
        #TODO musi byt odstraneny i prislusne hrany
        """
        Funkce odstrani uzel z grafu ==> z jeho seznamu
        :param node: uzel, ktery ma byt odstranen
        :return: vraci kopii puvodniho grafu bez odstraneneho uzlu
        """
        g = Graph(self.get_nodes(), self.get_edges(), self.is_oriented())

        g.get_nodes().remove(node)

        return g

    def remove_solo_nodes(self):
        for n in self.get_nodes():
            if n.get_degree(self.is_oriented()) == 0:
                self.get_nodes().remove(n)

    def get_node_with_max_out_degree(self):
        """
        Funkce vyhleda uzel s nejvetsim vystupnim stupnem.
        :return: vraci odpovidajici uzel, pripadne None
        """
        max_degree = 0
        node = None

        for n in self.get_nodes():
            degree = n.get_out_degree()
            if degree > max_degree:
                max_degree = degree
                node = n
        return node

    def get_node_with_max_in_degree(self):
        """
        Funkce vyhleda uzel s nejvetsim vstupnim stupnem.
        :return: vraci odpovidajici uzel, pripadne None
        """
        max_degree = 0
        node = None

        for n in self.get_nodes():
            degree = n.get_in_degree()
            if degree > max_degree:
                max_degree = degree
                node = n
        return node

    def add_edge(self, node_from_name, node_to_name, edge_name, edge_value):
        """
        Funkce prida novou hranu do grafu, opet se vytvari kopie grafu a neupravuje se original.
        :param node_from_name: nazev uzlu, z ktereho hrana vychazi
        :param node_to_name: nazev uzlu, do ktereho hrana vchazi
        :param edge_name: nazev hrany
        :param edge_value: ohodnoceni hrany
        :return: vraci novy graf s pridanou hranou
        """
        g = Graph(self.get_nodes(), self.get_edges(), self.is_oriented())

        node_from = g.get_node_by_name(node_from_name)
        node_to = g.get_node_by_name(node_to_name)
        # pokud uzel neexistuje, tak ho vytvori
        if node_from is None:
            node_from = Node(node_from_name)
            g.get_nodes().append(node_from)
        # pokud uzel neexistuje, tak ho vytvori
        if node_to is None:
            node_to = Node(node_to_name)
            g.get_nodes().append(node_to)
        # upravi stupen u obou uzlu
        if g.is_oriented():
            node_from.inc_out_degree()
            node_to.inc_in_degree()
        else:
            #pokud je smycka, tak v neorientovanem grafu se zvysi stupen o 2
            if node_from == node_to and not g.is_oriented():
                node_from.inc_degree(g.is_oriented())
                node_from.inc_degree(g.is_oriented())
            else:
                #neni orientovany a neni smycka zvysujeme pouze o 1
                node_from.inc_degree(g.is_oriented())
                node_to.inc_degree(g.is_oriented())
        # pridani samotne hrany
        g = g.get_edges().append(Edge(node_from, node_to, edge_name, edge_value))

        return g

    def remove_edges_from_graph(self, edges=[]):
        """
        Funkce odstrani z grafu hrany, ktere jsou v seznamu edges
        :param edges: seznam hran, ktere maji byt odstraneny z grafu
        :return: vraci novy graf, z ktereho jsou odebrany prislusne hrany
        """
        g = Graph(self.__nodes, self.__edges, self.is_oriented())

        #odstranime vsechny hrany, ktere jsou v listu edges
        #zaroven musime zmenit i stupne u jednotlivych uzlu
        for e in edges:
            if e in g.get_edges():
                if g.is_oriented():
                    e.node_from.dec_out_degree()
                    e.node_to.dec_in_degree()
                else:
                    # neni orientovany a je smycka ==> musime odstranit 2 stupne
                    if e.node_from == e.node_to:
                        e.node_from.dec_degree(g.is_oriented())
                        e.node_from.dec_degree(g.is_oriented())
                    # neni orientovany
                    else:
                        e.node_from.dec_degree(g.is_oriented())
                        e.node_to.dec_degree(g.is_oriented())
                g.get_edges().remove(e)

        return g

    def get_max_degree(self):
        """
        Nalezne maximalni stupen v grafu.
        :return: vraci maximalni stupen v grafu
        """
        max_degree = 0

        for n in self.get_nodes():
            degree = n.get_degree(self.is_oriented())
            if degree > max_degree:
                max_degree = degree
        return max_degree

    def get_max_out_degree(self):
        """
        Nalezne maximalni vystupni stupen v grafu.
        :return: vraci maximalni vystupni stupen v grafu.
        """
        max_degree = 0

        for n in self.get_nodes():
            degree = n.get_out_degree()
            if degree > max_degree:
                max_degree = degree
        return max_degree

    def get_max_in_degree(self):
        """
        Nalezne maximalni vstupni stupen v grafu.
        :return: vraci maximalni vstupni stupen v grafu.
        """
        max_degree = 0

        for n in self.get_nodes():
            degree = n.get_in_degree()
            if degree > max_degree:
                max_degree = degree
        return max_degree

    def get_loops(self):
        """
        Funkce vyhledava smycky v grafu.
        :return: vraci seznam nazvu uzlu, ktere tvori smycky. Pokud je seznam prazdny ==> graf nema smycky.
        """

        g = Graph(self.__nodes, self.__edges, self.__is_oriented)

        #seznam smycek
        nodes_with_loop = []

        for e in g.get_edges():
            #pokud se node_from = node_to ==> jedna se o smycku
            if e.node_from == e.node_to:
                nodes_with_loop.append(e.node_from)

        return nodes_with_loop

    def is_multigraph(self):
        """
        Funkce zjistuje, jestli je graf multigraf (jestli obsahuje nasobne hrany)
        :return: vraci seznam nasobnych hran, pokud je seznam prazdny ==> nejedna se o multigraf
        """

        g = Graph(self.__nodes, self.__edges, self.__is_oriented)

        #bude obsahovat prvni nalezene hrany
        first_edges = []
        #bude obsahovat hrany, ktere jsou duplicitni (nasobne)
        multiply_edges = []

        for e in g.get_edges():
            node_from = e.node_from
            node_to = e.node_to
            edge_name = e.edge_name
            for e2 in g.get_edges():
                #pokud hrana jeste nebyla zpracovana
                if e2 not in first_edges and e2 not in multiply_edges:
                    #pokud maji stejne uzly, ale jiny nazev hrany ==> jedna se o nasobnou hranu
                    if e2.node_from == node_from and e2.node_to == node_to and e2.edge_name != edge_name:
                        first_edges.append(e)
                        multiply_edges.append(e2)

        return multiply_edges

    def is_complete_graph(self):
        """
        Funkce zjistuje, jestli se jedna o uplny graf nebo ne.
        :return: vraci true nebo false podle toho, zda se jedna o uplny graf nebo ne
        """

        graph = Graph(self.__nodes, self.__edges, self.is_oriented())

        # zjistime, jestli graf neobsahuje nasobne hrany
        multi_edges = graph.is_multigraph()

        # pokud se nerovna 0, tak obsahuje nasobne hrany, ktere musime odstranit
        if len(multi_edges) != 0:
            graph = graph.remove_edges_from_graph(multi_edges)
        # pocet hran musi byt roven teto rovnici, aby graf mohl byt uplny
        equation = (len(graph.get_nodes()) * (len(graph.get_nodes()) - 1)) / 2
        # porovname pocet hran v grafu s hodnotou rovnice
        return equation == len(graph.get_edges())

    """ ---- doplneni uloha 2 ---- """

    def get_skeleton_of_graph(self):
        """
        Funkce vyhleda kostru v ohodnocenem grafu.
        - pouziva Kruskaluv algoritmus
        :return: vraci kostru grafu
        """

        for n in self.get_nodes():
            if n.get_degree(self.is_oriented()) == 0:
                print("Pozor graf obsahuje izolovany uzel! (" + n.get_name() + ')')

        # vytvorime si kopii grafu
        #graph = Graph(self.get_nodes().copy(), self.get_edges().copy(), self.is_oriented())
        graph = copy.deepcopy(self)
        # seradime vzestupne hrany v grafu dle jejich ohodnoceni
        graph.get_edges().sort(key=lambda x: x.edge_value, reverse=False)
        # kostra musi obsahovat vsechny uzly, takze je muzeme hned nakopirovat
        skeleton = Graph(self.__nodes, [], self.is_oriented())
        # vytvorime si mnozinu, ktera bude symbolizovat navstivene uzly
        visited = set([])

        i = 0
        while len(graph.get_edges()) != 0 and i <= 300:
            # odebereme hranu z grafu ke zpracovani
            e = graph.get_edges().pop(0)
            # pokud by v navstivenych jiz byly oba uzly ==> vytvorime smycku (v kostre nemohou byt smycky)
            if not (e.node_from in visited and e.node_to in visited):
                skeleton.add_edge(e.node_from.get_name(), e.node_to.get_name(), e.edge_name, e.edge_value)
                visited.add(e.node_from)
                visited.add(e.node_to)
            i += 1

        if i == 200:
            print("Pravdepodobne doslo k zacykleni!")

        return skeleton

    def get_edge_by_nodes_and_edge_name(self, node_from, node_to, edge_name):
        """
        Funkce vyhleda objekt Edge (hrana) na zaklade vystupniho, vstupniho uzlu a jejiho nazvu
        :param node_from: vystupni uzel
        :param node_to: vstupni uzel
        :param edge_name: nazev hrany
        :return: vraci objekt Edge
        """
        for e in self.get_edges():
            if node_from == e.node_from and node_to == e.node_to and edge_name == e.edge_name:
                return e

    def get_edge_by_nodes_names(self, node_from_name, node_to_name):
        """
        Funkce vyhleda objekt Edge (hrana) na zaklade vystupniho, vstupniho uzlu
        :param node_from_name: jmeno uzlu, z ktereho hrana vychazi
        :param node_to_name: jmeno uzlu, do kterheo hrana vchazi
        :return: vraci hranu nebo None ==> pokud takova hrana nexistuje
        """
        for edge in self.get_edges():
            if edge.node_from.get_name() == node_from_name and edge.node_to.get_name() == node_to_name:
                return edge
            if edge.node_from.get_name() == node_to_name and edge.node_to.get_name() == node_from_name:
                return edge
        return None

    def get_edge_by_edge_name(self, edge_name):
        """
        Funkce vybere hranu z grafu na zaklade jejiho nazvu.
        :param edge_name: nazev hranu
        :return: vraci hranu (jako objekt)
        """
        for e in self.get_edges():
            if e.edge_name == edge_name:
                return e

    def get_neighbours(self, node):

        # TODO mozna by to chtelo prejmenovat, protoze to uplne nazvu naslednici nesedi

        """
        Funkce vraci vsechny uzly, ktere vychazi z uzlu node
        :param node: uzel, z ktereho vychazi hrany
        :return: seznam hran vychazejici z uzlu node
        """

        neighbours = []

        for e in self.get_edges():
            if e.node_from == node:
                neighbours.append(e)

        return neighbours

    def get_bridges_of_graph(self):

        """
        Funkce slouzi k vyhledani mostu v grafu
        :return: vraci seznam hran, ktere tvori mosty (jejich odstranenim by se graf rozpadl na vice komponent)
        """
        # vytvorime si kopii grafu
        graph = copy.deepcopy(self)

        # nastavime si znacky TODO myslim, ze muzeme odstranit znacku detect, nakonec jsem ji nevyuzil
        for n in graph.get_nodes():
            n.set_attrs({"mark": None, "remove": False, "detect": False, "edges": []})
        # nastavime si znacky k hranam a priradime si hrany k uzlum
        for e in graph.get_edges():
            e.node_from.get_attrs()["edges"].append(e)
            e.node_to.get_attrs()["edges"].append(e)
            e.get_attrs()["in_skeleton"] = False
        # budeme pracovat se zasobnikem
        stack = []
        # list, ktery naznacuje navstivene uzly
        # TODO asi muzeme smazat, vyresil jsem nakonec pres znacky primo v objektu
        opens = []
        # hrany, ktere budou tvorit kostru
        skeleton_edges = []
        # inicializace ==> prvni uzel je startovaci a jde na zasobnik
        if len(graph.get_nodes()) != 0:
            start_node = graph.get_nodes()[0]
            stack.append(start_node)
            start_node.get_attrs()["mark"] = 'open'
        # pocitadlo, aby nedoslo v pripade chybi k zacykleni
        count_error = 0
        # cyklus pobezi dokud bude neco na zasobniku nebo bude prekroceno kontrolni pocitadlo
        while len(stack) != 0 and count_error <= 300:
            count_error += 1
            # bereme vrchol ze zasobniku
            peak_node = stack[len(stack) - 1]
            # ziskame znacku
            mark = peak_node.get_attrs()["mark"]
            # pokud je None nastavime znacku open
            if mark is None:
                peak_node.get_attrs()["mark"] = 'open'
                opens.append(peak_node)
            # pokud je znacka open
            if mark == 'open':
                # projdeme vsechny hrany vychazejici z uzlu
                for e in peak_node.get_attrs()["edges"]:
                    # pokud se najde neoznackovany uzel nastavi se na True
                    has_no_mark = False
                    # pracujeme s hranami, ktere jeste nejsou v kostre
                    if not e.get_attrs()["in_skeleton"]:
                        # vybereme naslednika
                        if e.node_from == peak_node:
                            neighbour = e.node_to
                        else:
                            neighbour = e.node_from
                        # pokud nema naslednik zatim znacku
                        if neighbour.get_attrs()["mark"] is None:
                            # hranu zahrneme do kostry
                            e.get_attrs()["in_skeleton"] = True
                            skeleton_edges.append(e)
                            # pridame naslednika na zasobnik
                            stack.append(neighbour)
                        # pokud ma naslednik znacku open ==> nasli jsme smycku
                        elif neighbour.get_attrs()["mark"] == 'open':

                            loop_node = neighbour

                            counter = len(stack) - 1
                            # uzly tvorici smycky
                            loop_nodes = [loop_node]
                            # odebereme ze zasobniku uzel => budeme odebirat dokud nenarazime zase na naslendika
                            # tim ziskame vsechny uzly tvorici smycku
                            node_back = stack.pop(counter)
                            # seznam hran, ktere musi byt zachovany
                            save_edges = set([])
                            # seznam hran, ktere budou smazany
                            remove_edges = set([])
                            # opakujeme dokud nenarazime na zasobniku na naslednika tvorici smycku
                            while loop_node != node_back:
                                node_back.get_attrs()["remove"] = True
                                counter -= 1
                                loop_nodes.append(node_back)
                                node_back = stack.pop(counter)
                            # vytvorime nazev noveho uzlu (nazvy vsech uzlu tvvorici smycku)
                            new_node_name = ""
                            # projdeme vsechny uzly tvorici smycky
                            for node in loop_nodes:
                                node_back.get_attrs()["remove"] = True
                                # tvorba nazvu noveho uzlu
                                new_node_name += node.get_name()
                                # projdeme hrany uzlu
                                for edge in node.get_attrs()["edges"]:
                                    # pokud neobsahuje znacku remove ==> musime hranu zachovat
                                    if not edge.node_from.get_attrs()["remove"] or not edge.node_to.get_attrs()["remove"]:
                                        save_edges.add(edge)
                                    else:
                                        remove_edges.add(edge)
                            # pridame do grafu novy uzel
                            graph.add_node(new_node_name)
                            # nechame si vratit objekt nove vytvoreneho uzlu
                            new_node = graph.get_node_by_name(new_node_name)
                            # nastavime mu znacky
                            new_node.set_attrs({"mark": 'open', "remove": False, "edges": []})
                            # projdeme hrany, ktere mame zachovat
                            for edge in save_edges:
                                if edge.node_to and edge.node_from:
                                    # pro vystupni uzel hrany
                                    if edge.node_from.get_attrs()["remove"]:
                                        # nastavime hrane nove vytvoreny uzel
                                        edge.node_from = new_node
                                        # pridame hranu k uzlu
                                        new_node.get_attrs()["edges"].append(edge)
                                        # upravime stupen uzlu
                                        new_node.inc_degree(graph.is_oriented())
                                    # pro vstupni uzel hrany
                                    if edge.node_to.get_attrs()["remove"]:
                                        # nastavime hrane nove vytvoreny uzel
                                        edge.node_to = new_node
                                        # priradime hranu k uzlu
                                        new_node.get_attrs()["edges"].append(edge)
                                        # upravime stupen uzlu
                                        new_node.inc_degree(graph.is_oriented())
                            # odstranime jiz nepotrebne hrany
                            graph = graph.remove_edges_from_graph(remove_edges)
                            # odstranime jiz nepotrebne uzly
                            for n in loop_nodes:
                                graph = graph.remove_node(n)
                            # pridame novy uzel na zasobnik
                            stack.append(new_node)

                        has_no_mark = True
                        break

                if not has_no_mark:
                    # pokud je zpracovan davam znacku closed
                    neighbour.get_attrs()["marks"] = 'closed'
                    stack.pop(len(stack) - 1)
        # vytvorime mnozinu s mosty
        bridges = set([])
        # pridame mosty do mnoziny, ktery vratime
        for n in graph.get_nodes():
            # print("Uzel " + n.get_name())
            for e in n.get_attrs()["edges"]:
                bridges.add(e)
        # vratime mnozinu mostu
        return bridges

    def get_articulations_of_graph(self):
        """
        Funkce slouzi k hledani artikulaci v grafu
        :return: vraci seznam artikulaci (uzlu)
        """

        # vytvorime kopii grafu
        graph = copy.deepcopy(self)
        # nastavime znacky (parametry)
        for n in graph.get_nodes():
            n.set_attrs({"mark": None, "edges": [], "defnum": None, "low": math.inf})
        # pridame hrany k uzlum
        for e in graph.get_edges():
            e.node_from.get_attrs()["edges"].append(e)
            e.node_to.get_attrs()["edges"].append(e)
            e.get_attrs()["in_skeleton"] = False

        LIFO = []

        RESULT = []

        skeleton = []

        i = 0
        # pridame na zasobnik prvni uzel
        if len(graph.get_nodes()) != 0:
            LIFO.append(graph.get_nodes()[0])
            LIFO[0].get_attrs()["mark"] = 'OPEN'
            LIFO[0].get_attrs()["defnum"] = i
        # chybove pocitadlo
        count_error = 0
        # opakuj dokud neni zasobnik prazdny nebo kontrolni pocitadlo neni 500
        while len(LIFO) != 0 and count_error <= 500:
            count_error += 1
            # vybereme uzel ze zasobniku
            node = LIFO.__getitem__(len(LIFO) - 1)
            # pokud ma znacku 'CLOSED' pokracuj
            if node.get_attrs()["mark"] == 'CLOSED':
                continue
            # pokud ma znacku 'OPEN'
            elif node.get_attrs()["mark"] == 'OPEN':
                # pokud bude mit oznackovaneho souseda zmeni se na True
                has_not_marked_neighbour = False
                # projdeme vsechny hrany uzlu
                for e in node.get_attrs()['edges']:
                    # vybereme naslednika
                    if e.node_from == node:
                        neighbour = e.node_to
                    elif e.node_to == node:
                        neighbour = e.node_from
                    else:
                        continue
                    # pokud naslednik nema znacku
                    if neighbour.get_attrs()["mark"] is None:
                        # print(node.get_name() + ' --> ' + neighbour.get_name())
                        # pridame hranu do kostry
                        e.get_attrs()['in_skeleton'] = True
                        skeleton.append({"node_from": node, "edge": e.edge_name, "node_to": neighbour})

                        i += 1
                        # nastavime znacku na 'OPEN'
                        neighbour.get_attrs()["mark"] = 'OPEN'
                        # nastavime hodnotu defnum
                        neighbour.get_attrs()["defnum"] = i
                        # pridame na zasobnik
                        LIFO.append(neighbour)
                        # nastavime, ze mel uzel, ktery jeste nebyl navstiven
                        has_not_marked_neighbour = True
                        node = neighbour
                # pokud jiz nemel zadny neoznackovany uzel
                if not has_not_marked_neighbour:
                    # uzavri uzel
                    node.get_attrs()["mark"] = 'CLOSED'
                    # odstran ze zasobniku
                    LIFO.remove(node)
                    # print(node.get_name())
                    RESULT.append(node)
        # projdeme vysledek
        for n in RESULT:
            # inicializace minima
            min_next_defnum = math.inf
            edges = n.get_attrs()["edges"]
            # projdeme hrany, ktere nejsou v kostre
            for e in edges:
                if not e.get_attrs()["in_skeleton"]:
                    # vybereme naslednika
                    if e.node_from == n:
                        neighbour = e.node_to
                    else:
                        neighbour = e.node_from
                    # pokud je defnum naslednika mensi ==> ukladame jako nove minimum
                    if neighbour.get_attrs()["defnum"] < min_next_defnum:
                        min_next_defnum = neighbour.get_attrs()["defnum"]
            # inicializace low naslednika
            min_low_of_next = math.inf
            # projdeme kostru a hledame minimum low naslendika
            for s in skeleton:
                if s["node_from"] == n:
                    low = s["node_to"].get_attrs()["low"]
                    if low < min_low_of_next:
                        min_low_of_next = low

            attrs = n.get_attrs()
            # vypocitame low (minimum ze tri hodnot)
            n.get_attrs()["low"] = min(attrs["defnum"], min_low_of_next, min_next_defnum)
        # seznam artikulaci
        articulations = []
        # projdeme kostru, pokud je splnena podminka ==> artikulace
        for n in skeleton:
            if n["node_from"].get_attrs()["defnum"] <= n["node_to"].get_attrs()["low"] and n["node_from"].get_attrs()["defnum"] != 0:
                articulations.append(n["node_from"])
        # vracime seznam artikulaci
        return articulations

    def print_articulation_table(self):
        """
        Funkce, ktera vypise artikulacni tabulku
        :return:
        """
        for n in self.get_nodes():
            print(n.get_name() + ': defnum = ' + str(n.get_attrs()['defnum']) + ': low = ' + str(n.get_attrs()['low']))

    """ ---- doplneni uloha 3 ---- """

    def dijkstras_algoritmh(self):
        """
        Implementace dijkstrova algoritmu, ktery se pouziva na hledani nejkratsi cesty
        :return:
        """
        # vytvorime si kopii grafu
        graph = copy.deepcopy(self)
        # pripravime si potrebne atributy pro uzly
        for n in graph.get_nodes():
            n.set_attrs({"processed": False, "parent": '-' if (n.get_name() == 'ISP') else None,
                         "length_path": 0 if (n.get_name() == 'ISP') else math.inf, "edges_from": []})
        # pripravime si potrebne atributy pro hrany
        for e in graph.get_edges():
            e.node_from.get_attrs()['edges_from'].append(e)
        # zaciname uzlem ISP, ktery je na zactaku
        node_start = graph.get_nodes()[0]
        # seznam, ktery znaci uzly, ktere musime zpracovat
        to_process = [node_start]
        # kontrolni pocitadlo
        count_error = 0
        # cyklus budeme opakvoat dokud budeme mit uzel ke zpracovani nebo dokud nebude presahnuto kontrolni pocitadlo
        while len(to_process) != 0 and count_error <= 500:
            count_error += 1
            # vezme si uzel ke zpracovani
            node = to_process.pop(0)
            # pokud jeste neni zpracovan
            if not node.get_attrs()['processed']:
                # projdeme jeho hrany
                for e in node.get_attrs()["edges_from"]:
                    # pokud jeste nema nastavenou delku cesty => ma nekonecno
                    if e.node_to.get_attrs()["length_path"] == math.inf:
                        # nastavime delku cesty
                        e.node_to.get_attrs()["length_path"] = e.edge_value + node.get_attrs()["length_path"]
                        # nastavime rodice
                        e.node_to.get_attrs()["parent"] = node
                        # pridame uzel ke zpracovani
                        to_process.append(e.node_to)
                    # uzel uz ma delku pridelenou
                    else:
                        # vypocitame si potencionalni delku cesty
                        length_path = node.get_attrs()["length_path"] + e.edge_value
                        # porovname ji se stavajici
                        if length_path < e.node_to.get_attrs()["length_path"]:
                            # pokud je vyhodnejsi prenastavime
                            e.node_to.get_attrs()["length_path"] = length_path
                            e.node_to.get_attrs()["parent"] = node
                            e.node_to.get_attrs()["processed"] = False
                            to_process.append(e.node_to)
                node.get_attrs()["processed"] = True
            # vzdycky musime seradit od nejmensiho po nejvetsi
            to_process.sort(key=lambda x: x.get_attrs()["length_path"], reverse=False)

        return graph

    def get_euler_move(self):
        # vytvorime si kopii grafu
        graph = copy.deepcopy(self)
        # pocet uzlu s lichym stupnem
        odd_degrees = 0
        node_with_odd = None
        # pridani atributu a kontrola stupnu jednotlivych uzlu
        for n in graph.get_nodes():
            n.set_attrs({"edges": [], "start": False})

            if n.get_degree(graph.is_oriented()) % 2 != 0:
                odd_degrees += 1
                # pouzijeme prvni uzel s lichym stupnem
                if node_with_odd is None:
                    node_with_odd = n
        # euleruv tah lze najit pouze v pripade, ze maji vsechny uzly sudy stupen nebo prave 2 maji lichy
        if odd_degrees != 2 and odd_degrees != 0:
            print(odd_degrees)
            print("Euleruv tah nelze najit.")
            print("Pocet uzlu s lichym stupnem je: " + str(odd_degrees))
            return
        # pridame atributy pro hrany
        for e in graph.get_edges():
            e.set_attrs({"used": False})
            e.node_from.get_attrs()["edges"].append(e)
            e.node_to.get_attrs()["edges"].append(e)
        # seznam vsech cyklu, ktere pri pruchodu vytvorime
        cycles = []
        # jeden konkretni cyklus
        one_cycle = []
        # pokud je lichy stupen, tak startovaci bude jeden z nich
        if odd_degrees == 2:
            start_node = node_with_odd
        # vsechny uzly maji sudy stupen startovaci bude bude prvni
        else:
            start_node = graph.get_nodes()[0]
        # pro detekci smycky
        start_node.get_attrs()["start"] = True
        # pridame na zasobnik
        stack = [start_node]

        count_error = 0
        while len(stack) > 0 and count_error <= 500:
            count_error += 1

            node = stack[len(stack) - 1]

            is_cycle = False
            # musi byt neco v poli, ktere hran, ktere tvori cykly
            if len(one_cycle) != 0:
                for e in node.get_attrs()["edges"]:
                    # tohle zamezuje tomu, aby se nevratil pres hranu, ktrou zrovna prisel (ta je posledni pridana)
                    if e != one_cycle[len(one_cycle) - 1]:
                        # pokud se muzem dostat k startovacimu uzlu => vytvorime smycku
                        if e.node_from.get_attrs()["start"] or e.node_to.get_attrs()["start"]:
                            # hranu oznacime jako pouzitou
                            e.get_attrs()["used"] = True
                            # pridame ji do cyklu
                            one_cycle.append(e)
                            # detekovali jsme cyklus
                            is_cycle = True
                            break
            # cyklus jeste nebyl detekovan
            if not is_cycle:
                # udava, jestli uz byly pouzity vsechny hrany
                all_used = True
                # pokud uz jsou pouzity vsechny hrany a nemam kam dal jit => provedu skok pres posledni hranu
                last_edge = None
                # pokusim se jeste najit jednu neoznacenou hranu
                for e in node.get_attrs()["edges"]:
                    if not e.get_attrs()["used"]:
                        if e.node_from == node:
                            next_node = e.node_to
                        else:
                            next_node = e.node_from
                        stack.append(next_node)
                        one_cycle.append(e)
                        e.get_attrs()["used"] = True
                        all_used = False
                        break
                    last_edge = e
                # nejde udelat cyklus a vsechny uz jsou pouzity
                if all_used:
                    # udelam skok uz pres pouzitou hranu => jinak by se neukoncil
                    if last_edge.node_from == node:
                        next_node = last_edge.node_to
                    else:
                        next_node = last_edge.node_from
                    # pridam uzel na zasobnik
                    stack.append(next_node)
                    # tato hrana bude taky tvorit smycku
                    one_cycle.append(last_edge)
            # detekovali jsme smycku
            else:
                # pridame ji do seznamu smycek
                cycles.append({"cycle": one_cycle, "all_processed": False})
                # startovac uzel uz nebude startovaci
                stack[0].get_attrs()["start"] = False
                # vyprazdnime zasobnik a pole smycek
                one_cycle = []
                stack = []
                # musime najit jeste nenavstivenou hranu, pres kterou pujdeme hledat dalsi smycku
                for c in cycles:
                    # pokud se v teto smycce nenachazi nejaka neoznacena hrana, tak se preskoci
                    if c["all_processed"]:
                        continue
                    # muze obsahovat neoznacenou hranu musime ji najit
                    else:
                        # pokud se neoznacena nenajde tak zustane true => tento cyklus bude oznacen jako zpracovany a priste bude preskocen
                        all_processed = True
                        # pro kazdou hranu zkontrolujeme, jestli nejaky uzel nema neoznacenou hranu
                        for e in c["cycle"]:
                            # pokud najdeme neoznacenou hranu, tak si poznamename novy startovaci uzel
                            new_start_node = None
                            # pokud existuje neoznacena hrana, tak se nastvi startovaci uzel
                            for edge in e.node_to.get_attrs()["edges"]:
                                if not edge.get_attrs()["used"]:
                                    # existuje neoznacena hrana => cyklus nemuze byt oznacen jako zpracovany
                                    all_processed = False
                                    # startovaci uzel
                                    new_start_node = e.node_to
                                    break
                            # pokud existuje neoznacena hrana, tak se nastvi startovaci uzel
                            if new_start_node is None:
                                for edge in e.node_from.get_attrs()["edges"]:
                                    if not edge.get_attrs()["used"]:
                                        # existuje neoznacena hrana => cyklus nemuze byt oznacen jako zpracovany
                                        all_processed = False
                                        # startovaci uzel
                                        new_start_node = e.node_from
                                        break
                        # neoznacena hrana nebyla nalazena
                        if all_processed:
                            # cyklus bude oznacen jako zpracovany
                            c["all_processed"] = True
                        elif new_start_node is None:
                            break
                        else:
                            # jinak takova hrana existuje
                            new_start_node.get_attrs()["start"] = True
                            # pridame uzel na zasobnik a vse opakujeme
                            stack.append(new_start_node)

        # kontrolni vypis cyklu
        #for c in cycles:
            #print("cycle---")
            #for e in c["cycle"]:
                #print(e)

        # zhotoveni tahu

        move = []

        node = start_node

        error = False
        while len(cycles) != 0 and not error and count_error < 500:
            count_error += 1

            index = len(cycles) - 1
            find = False

            count_error2 = 0
            while not find and count_error2 < 500:
                count_error2 += 1

                c = cycles[index]

                for edge in c["cycle"]:
                    if not edge.get_attrs()["used"]:
                        c["cycle"].remove(edge)
                        continue
                    if edge.get_attrs()["used"]:
                        for e in node.get_attrs()["edges"]:
                            if e == edge:
                                find = True
                                move.append(e)
                                e.get_attrs()["used"] = False
                                if e.node_from == node:
                                    node = e.node_to
                                else:
                                    node = e.node_from
                                # i = 0
                                # print("----------------------- ")
                                # for m in move:
                                # i += 1
                                # print(str(i) + '. ' + m.edge_name)
                                c["cycle"].remove(e)
                                break
                if len(c["cycle"]) == 0:
                    cycles.remove(c)
                    find = True
                if not find:
                    # print("pocet cyklu: ")
                    # print(len(cycles))
                    # print(cycles)
                    # for c in cycles:
                    # for e in c["cycle"]:
                    # print(e)
                    if index > 0:
                        index -= 1

        if len(move) != 0:
            return move

