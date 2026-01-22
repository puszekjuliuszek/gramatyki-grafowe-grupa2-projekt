"""
Production P4

Breaks boundary edges (E with b=1) marked for refinement (r=1)
"""

from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production
from time import time


@Production.register
class P4(Production):
    """
    Production P4 - Break boundary edges

    Breaks boundary edges (E with b=1) marked for refinement (r=1)
    """

    def get_left_side(self) -> Graph:
        """
        Creates the left side of the production.

        Returns:
            Left side graph
        """
        g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 1, "n2")

        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(HyperEdge((n1, n2), "E", r=1))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        """
        Creates the right side of the production.

        Args:
            left: Matched subgraph (with current coordinates)

        Returns:
            Right side graph with new vertex breaking edge in half
        """
        g = Graph()

        nodes = left.nodes

        new_x = (nodes[0].x + nodes[1].x) / 2
        new_y = (nodes[0].y + nodes[1].y) / 2
        new_node = Node(new_x, new_y, f"n{time()}")
        nodes.append(new_node)

        for node in nodes:
            g.add_node(node)

        b_value = left.hyperedges[0].b
        g.add_edge(HyperEdge((nodes[0], nodes[2]), "E", r=0, b=b_value), check_nodes=False)
        g.add_edge(HyperEdge((nodes[2], nodes[1]), "E", r=0, b=b_value), check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        """r == 1 AND b == 1"""
        for edge in matched_graph.hyperedges:
            if edge.r != 1 or edge.b != 1:
                return False
        return True
