import unittest
import os
from graph import Graph
from node import Node
from edge import HyperEdge
from p2 import P2
from visualization import draw

class TestP2Negatives(unittest.TestCase):
    
    def setUp(self):
        self.graph = Graph()
        self.p2 = P2()
        if not os.path.exists("outputs"):
            os.makedirs("outputs")

    def test_no_hanging_node(self):
        """
        Krawędź chce się podzielić (R=1), ale NIE MA wiszącego węzła.
        Oczekiwane: False (P2 nie robi nic, bo nie ma konfliktu topologicznego).
        """
        print("\nTest 1: Brak wiszącego węzła")
        
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 0, "n2") 
        self.graph.add_node(n1)
        self.graph.add_node(n2)
        
        edge = HyperEdge([n1, n2], hypertag="E", r=1, b=0)
        self.graph.add_edge(edge)
        
        
        draw(self.graph, "outputs/p2_neg_no_node_before.png")
        result = self.p2.apply(self.graph)
        draw(self.graph, "outputs/p2_neg_no_node_after.png")
        
        print(f"Wynik: {result}")
        self.assertFalse(result, "P2 nie powinna działać bez wiszącego węzła")
        
        self.assertEqual(len(self.graph.hyperedges), 1)
        self.assertEqual(self.graph.hyperedges[0].r, 1)

    def test_wrong_r_flag(self):
        """
        SCENARIUSZ 2: Jest wiszący węzeł, ale krawędź ma R=0.
        Oczekiwane: False (P2 czeka, aż P6 najpierw oznaczy krawędź).
        """
        print("\nTest 2: R=0")
        
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 0, "n2")
        h1 = Node(2, 0, "h1")
        
        for n in [n1, n2, h1]:
            self.graph.add_node(n)
            
        edge = HyperEdge([n1, n2], hypertag="E", r=0, b=0)
        self.graph.add_edge(edge)
        
        draw(self.graph, "outputs/p2_neg_r0_before.png")
        result = self.p2.apply(self.graph)
        draw(self.graph, "outputs/p2_neg_r0_after.png")
        
        print(f"Wynik: {result}")
        self.assertFalse(result, "P2 nie powinna ruszać krawędzi z R=0")
        
        self.assertEqual(len(self.graph.hyperedges), 1)

    def test_wrong_label(self):
        """
        SCENARIUSZ 3: Warunki spełnione, ale to element P, a nie E.
        Oczekiwane: False (P2 dotyczy tylko krawędzi).
        """
        print("\nTest 3: Zła etykieta - P zamiast E")
        
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 0, "n2")
        h1 = Node(2, 0, "h1")
        
        for n in [n1, n2, h1]:
            self.graph.add_node(n)
            
        edge = HyperEdge([n1, n2], hypertag="P", r=1, b=0)
        self.graph.add_edge(edge)
        
        draw(self.graph, "outputs/p2_neg_label_before.png")
        result = self.p2.apply(self.graph)
        draw(self.graph, "outputs/p2_neg_label_after.png")
        
        print(f"Wynik: {result}")
        self.assertFalse(result, "P2 nie może dzielić elementów P, tylko krawędzie E")

if __name__ == '__main__':
    unittest.main()