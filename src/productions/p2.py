from src.graph import Graph
from src.node import Node
from src.edge import HyperEdge
from src.productions.production import Production

@Production.register
class P2(Production):
    """
    Produkcja P2: Rozbicie krawędzi E (R=1, B=0) w miejscu, gdzie znajduje się już wiszący węzeł.
    """
    def get_left_side(self) -> Graph:
        g = Graph()
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        h = Node(1, 0, "h") # Wiszący węzeł (geometrycznie w środku)
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(h)
        # We wzorcu h nie musi być połączony krawędzią, żeby został znaleziony przez izomorfizm
        g.add_edge(HyperEdge((n1, n2), "E"))
        return g

    def get_right_side(self, left: Graph) -> Graph:
        g = Graph()
        n1 = left.get_node("n1")
        n2 = left.get_node("n2")
        h = left.get_node("h")
        
        # Pobieramy atrybut b ze starej krawędzi
        old_edge = [e for e in left.hyperedges if e.hypertag == "E"][0]
        old_b = old_edge.b
        
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(h)
        
        # Tworzymy dwie nowe krawędzie łączące końce z węzłem h
        g.add_edge(HyperEdge((n1, h), "E", r=0, b=old_b))
        g.add_edge(HyperEdge((h, n2), "E", r=0, b=old_b))
        
        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        n1 = matched_graph.get_node("n1")
        n2 = matched_graph.get_node("n2")
        h = matched_graph.get_node("h")
        
        # Sprawdzamy czy to jedyna krawędź E w dopasowaniu
        edge = [e for e in matched_graph.hyperedges if e.hypertag == "E"][0]
        
        # Warunki: Typ E, R=1, B=0
        if edge.r != 1 or edge.b != 0:
            return False
            
        # Warunek geometryczny: czy h leży dokładnie w połowie n1-n2
        mid_x = (n1.x + n2.x) / 2.0
        mid_y = (n1.y + n2.y) / 2.0
        epsilon = 1e-5
        if abs(h.x - mid_x) < epsilon and abs(h.y - mid_y) < epsilon:
            return True
            
        return False