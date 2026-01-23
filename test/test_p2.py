import unittest
import os
from graph import Graph
from node import Node
from edge import HyperEdge
from p2 import P2 
from visualization import draw 

class TestP2(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        
        # Węzły
        self.v1 = Node(0, 0, "v1")
        self.v2 = Node(2, 0, "v2")
        self.h1 = Node(1, 0, "h1") # Wiszący węzeł w środku
        
        self.nodes = [self.v1, self.v2, self.h1]
        for n in self.nodes:
            self.graph.add_node(n)
            
        # Hiperkrawędź E (v1-v2), R=1, B=0
        # Uwaga: Przekazujemy listę węzłów [v1, v2]
        self.edge = HyperEdge([self.v1, self.v2], hypertag="E", r=1, b=0)
        self.graph.add_edge(self.edge)

        if not os.path.exists("outputs"):
            os.makedirs("outputs")

    def test_production_P2(self):
        print("\n--- Rozpoczynam Test P2 ---")
        
        draw(self.graph, "outputs/p2_before.png")
        
        counts = self.graph.count_nodes()
        self.assertEqual(counts.hyper, 1, "Powinna być 1 hiperkrawędź przed")
        self.assertEqual(counts.normal, 3, "Powinny być 3 węzły przed")

        # --- APLIKACJA PRODUKCJI ---
        p2 = P2()
        # Wywołujemy bezpośrednio, bo P2 ma logikę geometryczną
        result = p2.apply(self.graph)
        
        print(f"Produkcja P2 zastosowana: {result}")
        self.assertTrue(result, "Produkcja powinna zwrócić True (została zastosowana)")
        
        draw(self.graph, "outputs/p2_after.png")

        # --- WERYFIKACJA ---
        counts_after = self.graph.count_nodes()
        
        # Oczekujemy 2 hiperkrawędzi (stara usunięta, 2 nowe dodane)
        self.assertEqual(counts_after.hyper, 2, "Powinny być 2 hiperkrawędzie po podziale")
        self.assertEqual(counts_after.normal, 3, "Liczba węzłów bez zmian")
        
        # Sprawdzamy szczegóły nowych krawędzi
        new_edges = self.graph.hyperedges # Korzystamy z property hyperedges
        
        for edge in new_edges:
            self.assertEqual(edge.hypertag, "E", "Tag powinien być E")
            self.assertEqual(edge.r, 0, "R powinno być 0")
            self.assertEqual(edge.b, 0, "B powinno być 0")
            
            # Sprawdzamy czy h1 jest w węzłach tej krawędzi
            node_labels = [n.label for n in edge.nodes]
            self.assertIn("h1", node_labels, f"Krawędź {edge.label} powinna być połączona z h1")

        print(f"Test P2 zakończony sukcesem. Wyniki w folderze 'outputs/'.")

if __name__ == '__main__':
    unittest.main()