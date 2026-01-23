import unittest
import os
from graph import Graph
from node import Node
from edge import HyperEdge
from p2 import P2 
from visualization import draw 

class TestP2Attributes(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        
        self.v1 = Node(0, 0, "v1")
        self.v2 = Node(2, 0, "v2")
        self.h1 = Node(1, 0, "h1")
        
        self.nodes = [self.v1, self.v2, self.h1]
        for n in self.nodes:
            self.graph.add_node(n)
            
        if not os.path.exists("p2_outputs"):
            os.makedirs("p2_outputs")

    def test_P2_with_B0(self):
        """
        Test dla krawędzi wewnętrznej (B=0).
        Oczekiwany wynik: Produkcja wykonana (True).
        """
        print("\n--- Rozpoczynam Test P2 (B=0) ---")
        
        # Dodajemy krawędź z atrybutem B=0
        edge_b0 = HyperEdge([self.v1, self.v2], hypertag="E", r=1, b=0)
        self.graph.add_edge(edge_b0)

        draw(self.graph, "p2_outputs/p2_b0_before.png")
        
        counts = self.graph.count_nodes()
        self.assertEqual(counts.hyper, 1, "Powinna być 1 hiperkrawędź przed")

        p2 = P2()
        result = p2.apply(self.graph)
        
        print(f"Produkcja P2 dla B=0 zastosowana: {result}")
        self.assertTrue(result, "Produkcja powinna zwrócić True dla B=0")
        
        draw(self.graph, "p2_outputs/p2_b0_after.png")

        counts_after = self.graph.count_nodes()
        
        self.assertEqual(counts_after.hyper, 2, "Powinny być 2 hiperkrawędzie po podziale")
        
        for edge in self.graph.hyperedges:
            self.assertEqual(edge.b, 0, "Nowe krawędzie muszą dziedziczyć B=0")
            self.assertEqual(edge.r, 0, "R powinno zostać zresetowane do 0")
            
            node_labels = [n.label for n in edge.nodes]
            self.assertIn("h1", node_labels, f"Krawędź {edge.label} powinna być połączona z h1")

    def test_P2_with_B1(self):
        """
        Test dla krawędzi brzegowej (B=1).
        Oczekiwany wynik: Produkcja NIE wykonana (False).
        """
        print("\n--- Rozpoczynam Test P2 (B=1) ---")
        
        # Dodajemy krawędź z atrybutem B=1
        edge_b1 = HyperEdge([self.v1, self.v2], hypertag="E", r=1, b=1)
        self.graph.add_edge(edge_b1)

        draw(self.graph, "p2_outputs/p2_b1_before.png")
        
        counts = self.graph.count_nodes()
        self.assertEqual(counts.hyper, 1, "Powinna być 1 hiperkrawędź przed")

        p2 = P2()
        result = p2.apply(self.graph)
        
        print(f"Produkcja P2 dla B=1 zastosowana: {result}")
        self.assertFalse(result, "Produkcja powinna zwrócić False dla B=1 (powinna być ignorowana)")
        
        draw(self.graph, "p2_outputs/p2_b1_after.png") # Obrazek powinien być identyczny jak 'before'

        counts_after = self.graph.count_nodes()
        
        self.assertEqual(counts_after.hyper, 1, "Liczba krawędzi nie powinna się zmienić")
        self.assertEqual(self.graph.hyperedges[0].b, 1, "Atrybut B powinien nadal wynosić 1")

        print(f"Testy P2 zakończone. Wyniki w folderze 'outputs/'.")

if __name__ == '__main__':
    unittest.main()