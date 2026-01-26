import math
from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


def _build_cycle_from_geometry(corners_set, all_nodes, node_to_neighbors):
    """
    Build cyclic order [c0, m0, c1, m1, ...] from corners (sorted by angle) and
    midpoints between consecutive corners. Does not rely on ordered_nodes order.
    Returns (cycle, edge_midpoints) or (None, None) if building fails.
    """
    corners_list = list(corners_set)
    cx = sum(n.x for n in corners_list) / len(corners_list)
    cy = sum(n.y for n in corners_list) / len(corners_list)
    corners_list.sort(key=lambda n: math.atan2(n.y - cy, n.x - cx))
    k = len(corners_list)
    midpoints_ordered = []
    for i in range(k):
        c1, c2 = corners_list[i], corners_list[(i + 1) % k]
        common = set(node_to_neighbors.get(c1, [])) & set(node_to_neighbors.get(c2, []))
        mid = common - corners_set
        if len(mid) != 1:
            return None, None
        midpoints_ordered.append(mid.pop())
    cycle = []
    for i in range(k):
        cycle.append(corners_list[i])
        cycle.append(midpoints_ordered[i])
    edge_midpoints = midpoints_ordered
    return cycle, edge_midpoints


@Production.register
class P11(Production):
    def get_left_side(self) -> Graph:
        g = Graph()

        n1  = Node(0, 1, "n1")
        n8  = Node(0.5, 1.5, "n8")
        n6  = Node(1, 2, "n6")
        n9  = Node(1.5, 1.5, "n9")
        n4  = Node(2, 1, "n4")
        n10 = Node(2, 0.5, "n10")
        n3  = Node(2, 0, "n3")
        n11 = Node(1.5, -0.5, "n11")
        n5  = Node(1, -1, "n5")
        n12 = Node(0.5, -0.5, "n12")
        n2  = Node(0, 0, "n2")
        n7  = Node(0, 0.5, "n7")

        nodes = [n1, n8, n6, n9, n4, n10, n3, n11, n5, n12, n2, n7]

        for n in nodes:
            g.add_node(n)

        n = len(nodes)
        for i in range(n):
            currN = nodes[i]
            nextN = nodes[(i+1)%n]
            g.add_edge(HyperEdge((currN, nextN), "E"))

        g.add_edge(HyperEdge((n1, n6, n4, n3, n5, n2), "S", r=1))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        g = Graph()

        # Get corners from S hyperedge
        corners_set = set()
        for edge in left.hyperedges:
            if edge.hypertag == "S":
                corners_set = {n for n in edge.nodes}
                break

        all_nodes = [node for node in left.ordered_nodes if node.hyperref is None]
        node_to_neighbors = {n: [] for n in all_nodes}
        for edge in left.hyperedges:
            if edge.hypertag == "E" and len(edge.nodes) == 2:
                a, b = edge.nodes
                node_to_neighbors[a].append(b)
                node_to_neighbors[b].append(a)

        # Build cycle from geometry (sort corners by angle, find midpoint between consecutive corners)
        cycle, edge_midpoints = _build_cycle_from_geometry(corners_set, all_nodes, node_to_neighbors)

        if cycle is None or len(cycle) != 12:
            # Cannot build valid hex right side; copy left E-edges only
            for edge in left.hyperedges:
                if edge.hypertag == "E":
                    g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)
            return g

        nodes = cycle
        center_nodes = [nodes[0], nodes[2], nodes[4], nodes[6], nodes[8], nodes[10]]
        sum_x = sum(n.x for n in center_nodes) / 6
        sum_y = sum(n.y for n in center_nodes) / 6
        center = Node(sum_x, sum_y, "center")
        g.add_node(center)

        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)

        # Center connected only to the 6 edge midpoints, never to corners
        for mid in edge_midpoints:
            g.add_edge(HyperEdge((mid, center), "E", b=0), check_nodes=False)
        n = len(nodes)
        for i in range(1, n, 2):
            g.add_edge(HyperEdge((nodes[i], nodes[(i+1)%n], nodes[(i+2)%n], center), "Q", r=0), check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        for edge in matched_graph.hyperedges:
            if edge.hypertag == "E" and edge.r != 0:
                return False
            if edge.hypertag == "S" and edge.r != 1:
                return False

        return True
