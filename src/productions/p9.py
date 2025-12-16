"""
Production P9

Left side: A hexagonal element consisting of 7 nodes:
           - 1 central node
           - 6 outer nodes
           - 6 boundary 'E' hyperedges connecting the outer nodes
           - 1 central 'Q' hyperedge connecting all 7 nodes (center + outer)
           The Q hyperedge has r=0.

Right side: Same structure but Q hyperedge has r=1.
"""

from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P9(Production):
    """
    Production P9 - mark hexagonal element (with center node) for processing.

    Changes r attribute of QS hyperedge from 0 to 1.
    """

    def get_left_side(self) -> Graph:
        """
        Creates the left side of the production.

        Returns:
            Graph with 7 nodes (1 center, 6 outer), connected by boundary E edges,
            with Q hyperedge (r=0) connecting all nodes.
        """
        g = Graph()

        # Create nodes (approximate hexagonal layout for visualization)
        # Center node
        n0 = Node(0, 0, "n0")
        
        # Outer nodes (going counter-clockwise)
        n1 = Node(1, 0, "n1")
        n2 = Node(0.5, 0.866, "n2")
        n3 = Node(-0.5, 0.866, "n3")
        n4 = Node(-1, 0, "n4")
        n5 = Node(-0.5, -0.866, "n5")
        n6 = Node(0.5, -0.866, "n6")

        nodes = [n0, n1, n2, n3, n4, n5, n6]
        for n in nodes:
            g.add_node(n)

        # Add boundary edges (E) between outer nodes
        # Connect n1-n2, n2-n3, ..., n6-n1
        g.add_edge(HyperEdge((n1, n2), "E"))
        g.add_edge(HyperEdge((n2, n3), "E"))
        g.add_edge(HyperEdge((n3, n4), "E"))
        g.add_edge(HyperEdge((n4, n5), "E"))
        g.add_edge(HyperEdge((n5, n6), "E"))
        g.add_edge(HyperEdge((n6, n1), "E"))

        # Add central hyperedge (Q) connecting all 7 nodes
        # Matches the visual representation where S is in the center 
        # of the spoked wheel structure.
        g.add_edge(HyperEdge(tuple(nodes), "Q", r=0))

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

        # Copy all nodes from the match
        nodes = []
        for node in left.ordered_nodes:
            if node.hyperref is None:
                nodes.append(node)
                g.add_node(node)

        # Copy edges, modifying S to have r=1
        for edge in left.hyperedges:
            if edge.hypertag == "E":
                # Preserve boundary edges exactly as they are
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r), check_nodes=False)
            elif edge.hypertag == "Q":
                # Recreate S edge with r=1
                g.add_edge(HyperEdge(edge.nodes, "Q", r=1), check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        """Only match Q hyperedges with r=0."""
        for edge in matched_graph.hyperedges:
            if edge.hypertag == "Q" and edge.r != 0:
                return False
        return True