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
        pattern_midpoints = [left.get_node(f"n{i}") for i in range(5, 9)]
        
        corners = [n1, n2, n3, n4]
        corner_set = set(corners)
        corner_labels = "_".join(sorted(n.label for n in corners))
        v_x = sum(n.x for n in corners) / 4
        v_y = sum(n.y for n in corners) / 4
        v = Node(v_x, v_y, f"V_{corner_labels}")
        
        # Identify which midpoint is on which edge by checking E edges
        # Build map: (corner1, corner2) -> midpoint on that edge
        # A midpoint on edge c1-c2 must:
        # 1. Connect to both c1 and c2 via E edges
        # 2. Not be a corner itself
        # 3. Be geometrically between c1 and c2 (or very close)
        midpoint_map = {}
        corner_order = [n1, n2, n3, n4]
        
        for i in range(4):
            c1 = corner_order[i]
            c2 = corner_order[(i + 1) % 4]
            # Find midpoint on edge c1-c2
            best_mp = None
            best_score = float('inf')
            
            for mp in pattern_midpoints:
                if mp in corner_set:
                    continue
                
                # Check if mp connects to both c1 and c2 via E edges, and ONLY to c1 and c2
                connects_to_c1 = False
                connects_to_c2 = False
                edge_count = 0  # Count total E edges connected to mp
                connected_corners = set()  # Track ALL corners mp connects to
                
                for edge in left.hyperedges:
                    if edge.hypertag == "E" and len(edge.nodes) == 2:
                        if mp in edge.nodes:
                            edge_count += 1
                            # Check which corner(s) this edge connects to
                            for corner in corners:
                                if corner in edge.nodes:
                                    connected_corners.add(corner)
                                    if corner == c1:
                                        connects_to_c1 = True
                                    if corner == c2:
                                        connects_to_c2 = True
                
                # Midpoint should connect to exactly 2 corners (c1 and c2) and no others
                # This ensures we're using the actual midpoint created by P3/P4, not an outer corner
                # or a node that connects to multiple corners
                if connects_to_c1 and connects_to_c2 and len(connected_corners) == 2 and connected_corners == {c1, c2}:
                    # Verify geometric position: midpoint should be between corners
                    # Calculate expected midpoint position
                    expected_x = (c1.x + c2.x) / 2
                    expected_y = (c1.y + c2.y) / 2
                    # Distance from expected position
                    dist = math.sqrt((mp.x - expected_x)**2 + (mp.y - expected_y)**2)
                    # Prefer midpoints that are closer to the expected position
                    # and have exactly 2 E edges (one to each corner) - this is the ideal case
                    # Penalize nodes with more edges (they might be corners or other nodes)
                    ideal_edge_count = 2
                    edge_penalty = abs(edge_count - ideal_edge_count) * 0.5
                    score = dist + edge_penalty
                    if score < best_score:
                        best_score = score
                        best_mp = mp
            
            if best_mp:
                midpoint_map[(c1, c2)] = best_mp
                midpoint_map[(c2, c1)] = best_mp
        
        # If we couldn't identify all midpoints, fall back to pattern labels
        if len(midpoint_map) < 4:
            midpoint_map = {
                (n1, n2): pattern_midpoints[0], (n2, n1): pattern_midpoints[0],
                (n2, n3): pattern_midpoints[1], (n3, n2): pattern_midpoints[1],
                (n3, n4): pattern_midpoints[2], (n4, n3): pattern_midpoints[2],
                (n4, n1): pattern_midpoints[3], (n1, n4): pattern_midpoints[3]
            }
        
        # Add all nodes
        for node in corners + pattern_midpoints:
            g.add_node(node)
        g.add_node(v)
        
        # Keep existing E hyperedges
        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)
        
        # New E hyperedges to center - use identified midpoints
        for i in range(4):
            c1 = corner_order[i]
            c2 = corner_order[(i + 1) % 4]
            mp = midpoint_map.get((c1, c2))
            if mp and mp not in corner_set:
                g.add_edge(HyperEdge((mp, v), "E", r=0, b=0), check_nodes=False)
        
        # Create 4 new Q hyperedges using identified midpoints
        for i in range(4):
            c1 = corner_order[i]
            c2 = corner_order[(i + 1) % 4]
            c_prev = corner_order[(i - 1) % 4]
            mp1 = midpoint_map.get((c1, c2))  # Midpoint on edge c1-c2
            mp2 = midpoint_map.get((c_prev, c1))  # Midpoint on edge c_prev-c1
            if mp1 and mp2 and mp1 not in corner_set and mp2 not in corner_set:
                g.add_edge(HyperEdge((c1, mp1, v, mp2), "Q", r=0, b=0), check_nodes=False)
        
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
