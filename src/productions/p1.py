"""
Production P1

Left side: Four nodes connected by E hyperedges forming a square,
           with a Q hyperedge in the middle connecting all 4 nodes.
           The Q hyperedge has r=r0.

Right side: Same structure but all hyperedges E have r=1.

Example:
         r=r3
    n1 ---E--- n2
    |          |
r=r2E    Q     E r=r1
    |   r=r0   |
    n4 ---E--- n3
         r=r4
    is transformed into:
         r=1
    n1 ---E--- n2
    |          |
r=1 E    Q     E r=1
    |   r=r0   |
    n4 ---E--- n3
         r=1
"""

from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P1(Production):
    """
    Production P1 - set boundary edges r=1.
    """

    def get_left_side(self) -> Graph:
        """
        Creates the left side of the production.

        Returns:
            Graph with 4 nodes in a square, connected by E edges,
            with Q hyperedge in the middle.
        """
        g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(1, 0, "n2")
        n3 = Node(1, 1, "n3")
        n4 = Node(0, 1, "n4")

        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_node(n4)

        g.add_edge(HyperEdge((n1, n2), "E"))
        g.add_edge(HyperEdge((n2, n3), "E"))
        g.add_edge(HyperEdge((n3, n4), "E"))
        g.add_edge(HyperEdge((n4, n1), "E"))

        g.add_edge(HyperEdge((n1, n2, n3, n4), "Q"))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        """
        Creates the right side of the production.

        Args:
            left: Matched subgraph (with current coordinates)

        Returns:
            Graph with same structure but E hyperedges changed to r=1
        """
        g = Graph()

        for edge in left.hyperedges:
            if edge.hypertag == "E":
<<<<<<< HEAD
                g.add_edge(HyperEdge(edge.nodes, "E", r=1), check_nodes=False)
=======
                g.add_edge(HyperEdge(edge.nodes, "E", r=1, b=edge.b), check_nodes=False)
>>>>>>> 3595051 (Add p1 production and tests)
            elif edge.hypertag == "Q":
                g.add_edge(HyperEdge(edge.nodes, "Q", r=edge.r), check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        """Only match if there is at least one E edge with r!=1."""
        for edge in matched_graph.hyperedges:
            if edge.hypertag == "E" and edge.r != 1:
                return True
        return False