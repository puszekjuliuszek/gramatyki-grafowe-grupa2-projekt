"""
Production P5

Breaks a quadrilateral element marked for refinement (R=1) if all its edges are broken (R=0).

Left side:
    - 4 corner nodes forming a quadrilateral
    - 4 midpoint nodes on the edges
    - 8 E hyperedges connecting corners to midpoints (all with R=0)
    - 1 Q hyperedge connecting all 4 corner nodes (with R=1)

Right side:
    - Same nodes plus a new central vertex V at the centroid
    - 4 new Q hyperedges (all with R=0)
    - 4 new E hyperedges connecting midpoints to center (all with R=0, B=0)

Boundary attribute (B) handling:
    - Existing outer E edges PRESERVE their B attribute (B=0 stays B=0, B=1 stays B=1)
    - New internal E edges (midpoints to center) are always B=0 (they are internal)
    - New Q hyperedges are always B=0 (element interiors are never boundaries)
"""


from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production
import math


@Production.register
class P5(Production):
    """Production P5 - breaks quadrilateral into 4 smaller quadrilaterals."""

    def get_left_side(self) -> Graph:
        """Creates the left side pattern."""
        g = Graph()
        
        # Corner nodes
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")
        
        # Midpoint nodes
        n5 = Node(1, 0, "n5")
        n6 = Node(2, 1, "n6")
        n7 = Node(1, 2, "n7")
        n8 = Node(0, 1, "n8")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            g.add_node(node)
        
        # E hyperedges (all R=0)
        g.add_edge(HyperEdge((n1, n5), "E", r=0))
        g.add_edge(HyperEdge((n5, n2), "E", r=0))
        g.add_edge(HyperEdge((n2, n6), "E", r=0))
        g.add_edge(HyperEdge((n6, n3), "E", r=0))
        g.add_edge(HyperEdge((n3, n7), "E", r=0))
        g.add_edge(HyperEdge((n7, n4), "E", r=0))
        g.add_edge(HyperEdge((n4, n8), "E", r=0))
        g.add_edge(HyperEdge((n8, n1), "E", r=0))
        
        # Q hyperedge (R=1)
        g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        return g

    def get_right_side(self, left: Graph) -> Graph:
        """Creates the right side transformation."""
        g = Graph()
        
        # Retrieve nodes by their pattern labels
        n1 = left.get_node("n1")
        n2 = left.get_node("n2")
        n3 = left.get_node("n3")
        n4 = left.get_node("n4")
        n5 = left.get_node("n5")
        n6 = left.get_node("n6")
        n7 = left.get_node("n7")
        n8 = left.get_node("n8")
        
        # Calculate central vertex
        corners = [n1, n2, n3, n4]
        corner_labels = "_".join(sorted(n.label for n in corners))
        v_x = sum(n.x for n in corners) / 4
        v_y = sum(n.y for n in corners) / 4
        v = Node(v_x, v_y, f"V_{corner_labels}")
        
        # Add all nodes
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            g.add_node(node)
        g.add_node(v)
        
        # Keep existing E hyperedges
        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)
        
        # New E hyperedges to center
        # Mapping: n5->bottom, n6->right, n7->top, n8->left (relative to pattern)
        for mp in [n5, n6, n7, n8]:
            g.add_edge(HyperEdge((mp, v), "E", r=0, b=1), check_nodes=False)
        
        # 5 new Q hyperedges
        g.add_edge(HyperEdge((n1, n5, v, n8), "Q", r=0, b=0), check_nodes=False)
        g.add_edge(HyperEdge((n5, n2, n6, v), "Q", r=0, b=0), check_nodes=False)
        g.add_edge(HyperEdge((v, n6, n3, n7), "Q", r=0, b=0), check_nodes=False)
        g.add_edge(HyperEdge((n8, v, n7, n4), "Q", r=0, b=0), check_nodes=False)
        
        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        """Check if production can be applied."""
        q_edges = [e for e in matched_graph.hyperedges if e.hypertag == "Q"]
        if len(q_edges) != 1 or q_edges[0].r != 1:
            return False
        
        e_edges = [e for e in matched_graph.hyperedges if e.hypertag == "E"]
        if not all(e.r == 0 for e in e_edges):
            return False
        
        regular_nodes = [n for n in matched_graph.nodes if n.hyperref is None]
        return len(regular_nodes) == 8
