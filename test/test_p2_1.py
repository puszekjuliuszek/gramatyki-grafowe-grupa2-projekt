import unittest
import os
from graph import Graph
from node import Node
from edge import HyperEdge
from p2 import P2
from visualization import draw

class TestP2Triangle(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        
        self.n1 = Node(0, 0, "n1")    # Węzeł 1
        self.n2 = Node(0, 2, "n2")    # Węzeł 2
        self.n3 = Node(0, 1, "n3")    # Węzeł 3 (Hanging Node - środek)
        
        self.nodes = [self.n1, self.n2, self.n3]
        for n in self.nodes:
            self.graph.add_node(n)
            
        self.edge_to_break = HyperEdge([self.n1, self.n2], hypertag="E", r=1, b=0)
        self.graph.add_edge(self.edge_to_break)

        self.graph.add_edge(HyperEdge([self.n2, self.n3], hypertag="E", r=0, b=0))
        self.graph.add_edge(HyperEdge([self.n3, self.n1], hypertag="E", r=0, b=0))

        if not os.path.exists("outputs"):
            os.makedirs("outputs")

    def test_production_P2_triangle(self):

        draw(self.graph, "outputs/p2_triangle_before.png")

        counts = self.graph.count_nodes()
        self.assertEqual(counts.normal, 3)
        self.assertEqual(counts.hyper, 3)
        self.assertEqual(self.edge_to_break.r, 1, "Główna krawędź musi mieć R=1")

        p2 = P2()
        result = p2.apply(self.graph)
        
        print(f"Produkcja P2 zastosowana: {result}")
        self.assertTrue(result, "Produkcja P2 powinna wykryć hanging node i dokonać podziału")
        
        draw(self.graph, "outputs/p2_triangle_after.png")

        counts_after = self.graph.count_nodes()
        
        self.assertEqual(counts_after.normal, 3)
        
        self.assertEqual(counts_after.hyper, 4)
        
        direct_connection = False
        for edge in self.graph.hyperedges:
            nodes = edge.nodes
            if (self.n1 in nodes and self.n2 in nodes):
                direct_connection = True
                break
        
        self.assertFalse(direct_connection, "Bezpośrednia długa krawędź n1-n2 powinna zostać usunięta")

        print("Test P2 zakończony sukcesem.")

if __name__ == '__main__':
    unittest.main()