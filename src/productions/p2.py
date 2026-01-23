from graph import Graph
from node import Node
from edge import HyperEdge
import math

class P2:
    def apply(self, graph: Graph):
        """
        Wykonuje produkcję P2 na podanym grafie.
        Zwraca True, jeśli produkcja została zastosowana, False w przeciwnym razie.
        """
        candidates = self._find_applicable_nodes(graph)
        
        if not candidates:
            return False

        # Aplikujemy zmiany dla wszystkich znalezionych kandydatów
        for edge, v1, v2, h_node in candidates:
            print(f"Applying P2: Breaking edge {edge.label} at hanging node {h_node.label}")
            
            # Zapamiętujemy stary atrybut B i R (chociaż R ustawiamy na 0)
            old_b = edge.b
            
            # 1. Usuwamy starą hiperkrawędź
            # W Twoim graph.py usuwanie hiperkrawędzi odbywa się przez remove_node podając label
            graph.remove_node(edge.label)
            
            # 2. Tworzymy dwie nowe hiperkrawędzie
            # Pierwsza: v1 <-> h_node
            # Zakładam, że konstruktor HyperEdge przyjmuje (nodes, hypertag, r, b)
            new_edge1 = HyperEdge([v1, h_node], hypertag="E", r=0, b=old_b)
            
            # Druga: h_node <-> v2
            new_edge2 = HyperEdge([h_node, v2], hypertag="E", r=0, b=old_b)
            
            # Dodajemy do grafu (check_nodes=False, bo węzły już są w grafie)
            graph.add_edge(new_edge1, check_nodes=False)
            graph.add_edge(new_edge2, check_nodes=False)
            
        return True

    def _find_applicable_nodes(self, graph: Graph):
        candidates = []
        # Używamy graph.hyperedges (property zdefiniowane w graph.py), a nie graph.edges
        for edge in graph.hyperedges:
            # Warunek 1: Typ E, R=1, B=0
            # Sprawdzamy atrybuty obiektu HyperEdge
            if edge.hypertag == 'E' and edge.r == 1 and edge.b == 0:
                if len(edge.nodes) != 2:
                    continue
                
                v1, v2 = edge.nodes[0], edge.nodes[1]
                
                # Warunek 2: Sprawdzamy geometrię - czy istnieje wiszący węzeł w środku?
                hanging_node = self._find_hanging_node_between(graph, v1, v2)
                
                if hanging_node:
                    candidates.append((edge, v1, v2, hanging_node))
        return candidates

    def _find_hanging_node_between(self, graph: Graph, v1: Node, v2: Node):
        """
        Szuka węzła, który leży geometrycznie w połowie odległości między v1 a v2.
        """
        mid_x = (v1.x + v2.x) / 2.0
        mid_y = (v1.y + v2.y) / 2.0
        epsilon = 1e-5 

        # Iterujemy po graph.nodes (property zwracające listę Node)
        for node in graph.nodes:
            # Pomijamy same końce krawędzi
            if node == v1 or node == v2:
                continue
            
            # Sprawdzamy czy to nie jest węzeł reprezentujący hiperkrawędź (jeśli takie są w liście nodes)
            # W Twoim graph.py property 'nodes' zwraca tylko self._nodes.values(), 
            # czyli zwykłe wierzchołki, więc jest OK.
            
            if abs(node.x - mid_x) < epsilon and abs(node.y - mid_y) < epsilon:
                return node
                
        return None