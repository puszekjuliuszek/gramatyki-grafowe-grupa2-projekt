"""
Production P8

Breaks the pentagonal element (hypertag == P) marked for refinement (r == 1),
if all its edges are broken
"""

from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P8(Production):
    """
    Production P8 - Break boundary edges

    Breaks the pentagonal element (hypertag == P) marked for refinement (r == 1),
    replacing it with 5 Q and 5 E hyperedges.
    """

    def get_left_side(self) -> Graph:
        """
        Creates the left side of the production.

        Returns:
            Left side graph
        """
        g = Graph()

        nodes = [
            Node(0, 0, "n1"),
            Node(1, 0, "n2"),
            Node(1, 1, "n3"),
            Node(0, 1, "n4"),
            Node(1.5, 0.5, "n5"),
            Node(0.5, 0, "n6"),
            Node(0, 0.5, "n7"),
            Node(0.5, 1, "n8"),
            Node(1.25, 0.75, "n9"),
            Node(1.25, 0.25, "n10")
        ] 

        for node in nodes:
            g.add_node(node)

        g.add_edge(HyperEdge((nodes[0], nodes[5]), "E"))
        g.add_edge(HyperEdge((nodes[5], nodes[1]), "E"))
        g.add_edge(HyperEdge((nodes[1], nodes[9]), "E"))
        g.add_edge(HyperEdge((nodes[9], nodes[4]), "E"))
        g.add_edge(HyperEdge((nodes[4], nodes[8]), "E"))
        g.add_edge(HyperEdge((nodes[8], nodes[2]), "E"))
        g.add_edge(HyperEdge((nodes[2], nodes[7]), "E"))
        g.add_edge(HyperEdge((nodes[7], nodes[3]), "E"))
        g.add_edge(HyperEdge((nodes[3], nodes[6]), "E"))
        g.add_edge(HyperEdge((nodes[6], nodes[0]), "E"))
        g.add_edge(HyperEdge((nodes[0], nodes[1], nodes[2], nodes[3], nodes[4]), "P"))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        """
        Creates the right side of the production.

        Args:
            left: Matched subgraph (with current coordinates)

        Returns:
            Right side graph with new Q hyperedges replacing P hyperedge
        """
        g = Graph()

        nodes = left.nodes
        line_nodes = nodes[1::2]

        new_x = sum([node.x for node in line_nodes]) / 5
        new_y = sum([node.y for node in line_nodes]) / 5
        new_node = Node(new_x, new_y, "n11")

        for node in nodes + [new_node]:
            g.add_node(node)

        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(edge)

        for node in line_nodes:
            g.add_edge(HyperEdge((new_node, node), "E", r=0, b=0), check_nodes=False)

        n = len(nodes)
        for i in range(1, len(nodes), 2):
            g.add_edge(HyperEdge((nodes[i], nodes[(i+1)%n], nodes[(i+2)%n], new_node), "Q", r=0, b=0), check_nodes=False)
      
        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        """r == 1 for P hiperedge"""
        for edge in matched_graph.hyperedges:
            if edge.hypertag == "P" and edge.r != 1:
                return False
        return True
