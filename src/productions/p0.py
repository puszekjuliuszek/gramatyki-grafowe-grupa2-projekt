"""
Production P0

Left side: Four nodes connected by E hyperedges forming a square,
           with a Q hyperedge in the middle connecting all 4 nodes.
           The Q hyperedge has r=0.

Right side: Same structure but Q hyperedge has r=1.

Example:
    n1 ---E--- n2
    |          |
    E    Q     E
    |   r=0    |
    n4 ---E--- n3

    is transformed into:

    n1 ---E--- n2
    |          |
    E    Q     E
    |   r=1    |
    n4 ---E--- n3
"""

from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P0(Production):
    """
    Production P0 - mark quadrilateral for processing.

    Changes r attribute of Q hyperedge from 0 to 1.
    """

    def get_left_side(self) -> Graph:
        """
        Creates the left side of the production.

        Returns:
            Graph with 4 nodes in a square, connected by E edges,
            with Q hyperedge (r=0) in the middle.
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
            Graph with same structure but Q hyperedge changed to r=1
        """
        g = Graph()

        nodes = []
        for node in left.ordered_nodes:
            if node.hyperref is None:
                nodes.append(node)

        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r), check_nodes=False)

        g.add_edge(HyperEdge(tuple(nodes), "Q", r=1), check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        """Only match Q hyperedges with r=0."""
        for edge in matched_graph.hyperedges:
            if edge.hypertag == "Q" and edge.r != 0:
                return False
        return True
