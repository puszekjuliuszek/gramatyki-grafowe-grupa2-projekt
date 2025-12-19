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
    - 5 new Q hyperedges (4 corner + 1 central) all with R=0
    - 4 new E hyperedges connecting midpoints to center
"""

from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production
import math


@Production.register
class P5(Production):
    """Production P5 - breaks quadrilateral into 5 smaller quadrilaterals."""

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
        
        # Find Q hyperedge to get corners
        q_edge = None
        for edge in left.hyperedges:
            if edge.hypertag == "Q" and edge.r == 1:
                q_edge = edge
                break
        
        if q_edge is None:
            raise ValueError("Q hyperedge with R=1 not found")
        
        corners = list(q_edge.nodes)
        if len(corners) != 4:
            raise ValueError("Expected 4 corner nodes")
        
        # Find all E hyperedges to identify midpoints
        e_edges = [e for e in left.hyperedges if e.hypertag == "E"]
        
        # Build a mapping: (corner1, corner2) -> midpoint
        edge_to_midpoint = {}
        for e in e_edges:
            nodes_list = list(e.nodes)
            if len(nodes_list) == 2:
                n1, n2 = nodes_list
                # Check if one is a corner and one is a midpoint
                if n1 in corners and n2 not in corners:
                    edge_to_midpoint[(n1, n2)] = n2
                    edge_to_midpoint[(n2, n1)] = n2
                elif n2 in corners and n1 not in corners:
                    edge_to_midpoint[(n1, n2)] = n1
                    edge_to_midpoint[(n2, n1)] = n1
        
        # Sort corners by angle from centroid to get proper order
        cx = sum(n.x for n in corners) / 4
        cy = sum(n.y for n in corners) / 4
        
        def angle_from_center(n):
            dx = n.x - cx
            dy = n.y - cy
            return math.atan2(dy, dx)
        
        corners_ordered = sorted(corners, key=angle_from_center)
        n1, n2, n3, n4 = corners_ordered
        
        # Find midpoints on each edge using the mapping
        n5 = edge_to_midpoint.get((n1, n2)) or edge_to_midpoint.get((n2, n1))
        n6 = edge_to_midpoint.get((n2, n3)) or edge_to_midpoint.get((n3, n2))
        n7 = edge_to_midpoint.get((n3, n4)) or edge_to_midpoint.get((n4, n3))
        n8 = edge_to_midpoint.get((n4, n1)) or edge_to_midpoint.get((n1, n4))
        
        if not all([n5, n6, n7, n8]):
            # Fallback: find midpoints by checking which nodes are not corners
            all_nodes = set(left.nodes)
            corner_set = set(corners)
            midpoints = list(all_nodes - corner_set)
            if len(midpoints) >= 4:
                # Use geometric approach to match midpoints to edges
                midpoints.sort(key=angle_from_center)
                n5, n6, n7, n8 = midpoints[0], midpoints[1], midpoints[2], midpoints[3]
            else:
                raise ValueError(f"Not enough midpoint nodes found. Expected 4, found {len(midpoints)}")
        
        # Calculate central vertex
        corner_labels = "_".join(sorted(n.label for n in corners))
        v_x = sum(n.x for n in corners) / 4
        v_y = sum(n.y for n in corners) / 4
        v = Node(v_x, v_y, f"V_{corner_labels}")
        
        # Add all nodes
        for node in left.nodes:
            if node.hyperref is None:
                g.add_node(node)
        g.add_node(v)
        
        # Keep existing E hyperedges
        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)
        
        # New E hyperedges to center
        for mp in [n5, n6, n7, n8]:
            g.add_edge(HyperEdge((mp, v), "E", r=0, b=0), check_nodes=False)
        
        # 5 new Q hyperedges
        g.add_edge(HyperEdge((n1, n5, v, n8), "Q", r=0, b=0), check_nodes=False)
        g.add_edge(HyperEdge((n5, n2, n6, v), "Q", r=0, b=0), check_nodes=False)
        g.add_edge(HyperEdge((v, n6, n3, n7), "Q", r=0, b=0), check_nodes=False)
        g.add_edge(HyperEdge((n8, v, n7, n4), "Q", r=0, b=0), check_nodes=False)
        g.add_edge(HyperEdge((n5, n6, n7, n8), "Q", r=0, b=0), check_nodes=False)
        
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
