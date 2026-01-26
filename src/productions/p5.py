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
        """Creates the right side: one center vertex, edges only to edge midpoints."""
        g = Graph()

        # Get 4 corners from Q hyperedge
        corners_set = set()
        for edge in left.hyperedges:
            if edge.hypertag == "Q" and len(edge.nodes) == 4:
                corners_set = {n for n in edge.nodes}
                break
        if len(corners_set) != 4:
            n1, n2, n3, n4 = left.get_node("n1"), left.get_node("n2"), left.get_node("n3"), left.get_node("n4")
            n5, n6, n7, n8 = left.get_node("n5"), left.get_node("n6"), left.get_node("n7"), left.get_node("n8")
            return self._build_right_side_fallback(g, left, [n1, n2, n3, n4], [n5, n6, n7, n8])

        all_nodes = [node for node in left.ordered_nodes if node.hyperref is None]
        if len(all_nodes) != 8:
            n1, n2, n3, n4 = left.get_node("n1"), left.get_node("n2"), left.get_node("n3"), left.get_node("n4")
            n5, n6, n7, n8 = left.get_node("n5"), left.get_node("n6"), left.get_node("n7"), left.get_node("n8")
            return self._build_right_side_fallback(g, left, [n1, n2, n3, n4], [n5, n6, n7, n8])

        node_to_neighbors = {n: [] for n in all_nodes}
        for edge in left.hyperedges:
            if edge.hypertag == "E" and len(edge.nodes) == 2:
                a, b = edge.nodes
                node_to_neighbors[a].append(b)
                node_to_neighbors[b].append(a)

        # Build 8-node cycle by following E-edges only (graph boundary order).
        # Start at any corner; from corner pick the midpoint that is closest to edge geometric center.
        start = next(iter(corners_set))
        cycle = [start]
        prev = None
        current = start
        for _ in range(7):
            neighbors = node_to_neighbors[current]
            if prev is None:
                # At first corner: 2 neighbors are midpoints; pick the one closest to its edge's geometric center
                mid_candidates = [n for n in neighbors if n not in corners_set]
                if len(mid_candidates) == 2:
                    def dist_to_edge_center(m):
                        other = next(c for c in node_to_neighbors[m] if c != start)
                        ex = (start.x + other.x) / 2
                        ey = (start.y + other.y) / 2
                        return (m.x - ex)**2 + (m.y - ey)**2
                    nxt = min(mid_candidates, key=dist_to_edge_center)
                else:
                    nxt = neighbors[0] if neighbors else None
            else:
                nxt = neighbors[1] if neighbors[0] == prev else neighbors[0]
            if nxt is None:
                n1, n2, n3, n4 = left.get_node("n1"), left.get_node("n2"), left.get_node("n3"), left.get_node("n4")
                n5, n6, n7, n8 = left.get_node("n5"), left.get_node("n6"), left.get_node("n7"), left.get_node("n8")
                return self._build_right_side_fallback(g, left, [n1, n2, n3, n4], [n5, n6, n7, n8])
            prev, current = current, nxt
            cycle.append(current)

        # Strict alternation: cycle[1,3,5,7] must be non-corners
        if any(cycle[i] in corners_set for i in (1, 3, 5, 7)):
            n1, n2, n3, n4 = left.get_node("n1"), left.get_node("n2"), left.get_node("n3"), left.get_node("n4")
            n5, n6, n7, n8 = left.get_node("n5"), left.get_node("n6"), left.get_node("n7"), left.get_node("n8")
            return self._build_right_side_fallback(g, left, [n1, n2, n3, n4], [n5, n6, n7, n8])

        corners = [cycle[0], cycle[2], cycle[4], cycle[6]]

        # For each edge (c_i, c_{i+1}), use the node that is actually on that edge (closest to edge center).
        # If an edge has 2 nodes (split), pick the one closest to geometric midpoint of the two corners.
        def edge_center(c_a, c_b):
            common = set(node_to_neighbors.get(c_a, [])) & set(node_to_neighbors.get(c_b, []))
            common = [n for n in common if n not in corners_set]
            if not common:
                return None
            mid_x = (c_a.x + c_b.x) / 2
            mid_y = (c_a.y + c_b.y) / 2
            return min(common, key=lambda n: (n.x - mid_x)**2 + (n.y - mid_y)**2)

        midpoints = []
        for i in range(4):
            c_i = corners[i]
            c_next = corners[(i + 1) % 4]
            m = edge_center(c_i, c_next)
            if m is None:
                midpoints = [cycle[1], cycle[3], cycle[5], cycle[7]]
                break
            midpoints.append(m)
        if len(midpoints) != 4:
            midpoints = [cycle[1], cycle[3], cycle[5], cycle[7]]

        corner_labels = "_".join(sorted(n.label for n in corners))
        v_x = sum(n.x for n in corners) / 4
        v_y = sum(n.y for n in corners) / 4
        v = Node(v_x, v_y, f"V_{corner_labels}")

        for node in cycle:
            g.add_node(node)
        g.add_node(v)

        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)

        # Single center; edges only to the 4 edge midpoints (centers of shape's edges)
        for mp in midpoints:
            g.add_edge(HyperEdge((mp, v), "E", r=0, b=0), check_nodes=False)

        for i in range(4):
            c_i = corners[i]
            m_i = midpoints[i]
            m_prev = midpoints[(i - 1) % 4]
            g.add_edge(HyperEdge((c_i, m_i, v, m_prev), "Q", r=0, b=0), check_nodes=False)

        return g

    def _build_right_side_fallback(self, g: Graph, left: Graph, corners, midpoints) -> Graph:
        """Fallback using pattern order when geometry-based midpoint detection fails."""
        n1, n2, n3, n4 = corners[0], corners[1], corners[2], corners[3]
        n5, n6, n7, n8 = midpoints[0], midpoints[1], midpoints[2], midpoints[3]
        corner_labels = "_".join(sorted(n.label for n in corners))
        v_x = sum(n.x for n in corners) / 4
        v_y = sum(n.y for n in corners) / 4
        v = Node(v_x, v_y, f"V_{corner_labels}")
        for node in corners + midpoints:
            g.add_node(node)
        g.add_node(v)
        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)
        for mp in midpoints:
            g.add_edge(HyperEdge((mp, v), "E", r=0, b=0), check_nodes=False)
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
