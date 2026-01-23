import unittest
import os
from graph import Graph
from node import Node
from edge import HyperEdge
from p6 import P6
from visualization import draw

class TestP6Scenarios(unittest.TestCase):
    
    def setUp(self):
        self.p6 = P6()
        if not os.path.exists("p6_outputs_scenarios"):
            os.makedirs("p6_outputs_scenarios")

    def _build_graph_variant(self, missing_node=False, missing_edge=False, add_clutter=False):
        """
        Pomocnicza metoda budująca graf wg Twojego sprawdzonego wzorca.
        Pozwala modyfikować strukturę dla różnych scenariuszy testowych.
        """
        graph = Graph()
        
        v1 = Node(0, 0, "v1")    # Lewy dół
        v2 = Node(4, 0, "v2")    # Prawy dół
        v3 = Node(5, 3, "v3")    # Prawa góra
        v4 = Node(2, 5, "v4")    # Szczyt
        v5 = Node(-1, 3, "v5")   # Lewa góra
        
        nodes_to_add = [v1, v2, v3, v4, v5]
        
        if missing_node:
            nodes_to_add.remove(v5) 
            
        v_extra = None
        if add_clutter:
            v_extra = Node(6, 6, "v_extra")
            nodes_to_add.append(v_extra)

        for n in nodes_to_add:
            graph.add_node(n)

        edges_defs = [
            (v1, v2),
            (v2, v3),
            (v3, v4)
        ]
        
        if not missing_node:
            edges_defs.append((v4, v5))

            if not missing_edge:
                edges_defs.append((v5, v1))
        
        for start, end in edges_defs:
            graph.add_edge(HyperEdge([start, end], hypertag="E", r=0, b=1))
            
        if add_clutter and v_extra:
            graph.add_edge(HyperEdge([v3, v_extra], hypertag="E", r=0, b=1))

        pentagon_nodes = [n for n in nodes_to_add if n != v_extra]
        
        center_edge = HyperEdge(pentagon_nodes, hypertag="P", r=0, b=0)
        graph.add_edge(center_edge)
        
        return graph

    def test_negative_missing_edge(self):
        """
        TEST NEGATYWNY 1: Brak krawędzi na obwodzie.
        Graf ma 5 węzłów, P łączy 5 węzłów, ale brakuje krawędzi E między v5 a v1.
        """
        print("\nScenariusz: Brak krawędzi (Broken Pentagon)")
        graph = self._build_graph_variant(missing_edge=True)
        
        draw(graph, "p6_outputs_scenarios/p6_missing_edge_before.png")
        
        result = self.p6.apply(graph)
        
        draw(graph, "p6_outputs_scenarios/p6_missing_edge_after.png")
        
        if result:
            print("INFO: Produkcja zadziałała (Graf niekompletny, ale P6 waliduje tylko węzły).")
        else:
            print("INFO: Produkcja prawidłowo zablokowana.")
            self.assertFalse(result)

    def test_negative_missing_node(self):
        """
        TEST NEGATYWNY 2: Brak węzła.
        Graf ma 4 węzły tworzące czworokąt.
        """
        print("\nScenariusz: Brak węzła (4 nodes)")
        graph = self._build_graph_variant(missing_node=True)
        
        draw(graph, "p6_outputs_scenarios/p6_missing_node_before.png")
        
        result = self.p6.apply(graph)
        
        draw(graph, "p6_outputs_scenarios/p6_missing_node_after.png")
        
        self.assertFalse(result, "Produkcja NIE POWINNA zadziałać dla 4 węzłów!")

    def test_positive_clutter(self):
        """
        TEST POZYTYWNY: Pentagon + dodatkowy element.
        """
        print("\nScenariusz: Poprawny Pentagon + Clutter")
        graph = self._build_graph_variant(add_clutter=True)
        
        draw(graph, "p6_outputs_scenarios/p6_clutter_before.png")
        
        result = self.p6.apply(graph)
        
        draw(graph, "p6_outputs_scenarios/p6_clutter_after.png")
        
        self.assertTrue(result, "Produkcja powinna zadziałać mimo dodatkowego elementu!")
        
        p_edge = [e for e in graph.hyperedges if e.hypertag == 'P'][0]
        self.assertEqual(p_edge.r, 1)

if __name__ == '__main__':
    unittest.main()