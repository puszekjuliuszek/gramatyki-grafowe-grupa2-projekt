import unittest
import os
from graph import Graph
from node import Node
from edge import HyperEdge
from p6 import P6
from visualization import draw

class TestP6Pentagon(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        

        self.v1 = Node(0, 0, "v1")    # Lewy dół
        self.v2 = Node(4, 0, "v2")    # Prawy dół
        self.v3 = Node(5, 3, "v3")    # Prawa góra
        self.v4 = Node(2, 5, "v4")    # Szczyt
        self.v5 = Node(-1, 3, "v5")   # Lewa góra
        
        self.nodes = [self.v1, self.v2, self.v3, self.v4, self.v5]
        for n in self.nodes:
            self.graph.add_node(n)

        self.graph.add_edge(HyperEdge([self.v1, self.v2], hypertag="E", r=0, b=1))
        self.graph.add_edge(HyperEdge([self.v2, self.v3], hypertag="E", r=0, b=1))
        self.graph.add_edge(HyperEdge([self.v3, self.v4], hypertag="E", r=0, b=1))
        self.graph.add_edge(HyperEdge([self.v4, self.v5], hypertag="E", r=0, b=1))
        self.graph.add_edge(HyperEdge([self.v5, self.v1], hypertag="E", r=0, b=1))
        
        self.center_edge = HyperEdge(self.nodes, hypertag="P", r=0, b=0)
        self.graph.add_edge(self.center_edge)

        if not os.path.exists("outputs"):
            os.makedirs("outputs")

    def test_production_P6_pentagon(self):
        
        draw(self.graph, "outputs/p6_pentagon_before.png")
        
        self.assertEqual(self.center_edge.r, 0, "Początkowo R powinno wynosić 0")
        
        counts = self.graph.count_nodes()
        self.assertEqual(counts.normal, 5)
        self.assertEqual(counts.hyper, 6)

        p6 = P6()
        result = p6.apply(self.graph)
        
        print(f"Produkcja P6 zastosowana: {result}")
        self.assertTrue(result, "Produkcja powinna zostać zastosowana dla elementu P")
        
        draw(self.graph, "outputs/p6_pentagon_after.png")
        
        p_edges = [e for e in self.graph.hyperedges if e.hypertag == 'P']
        self.assertEqual(len(p_edges), 1)
        modified_p = p_edges[0]
        
        self.assertEqual(modified_p.r, 1, "Atrybut R elementu P powinien zmienić się na 1")
        
        counts_after = self.graph.count_nodes()
        self.assertEqual(counts_after.normal, 5, "Liczba węzłów nie powinna się zmienić")
        self.assertEqual(counts_after.hyper, 6, "Liczba hiperkrawędzi nie powinna się zmienić")
        
        e_edges = [e for e in self.graph.hyperedges if e.hypertag == 'E']
        for e in e_edges:
            self.assertEqual(e.r, 0, "Krawędzie brzegowe E nie powinny zmienić flagi R")

        print("Test P6 zakończony sukcesem.")

if __name__ == '__main__':
    unittest.main()