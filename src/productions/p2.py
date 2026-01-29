from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P2(Production):
    """
    Production P2 – Break internal edge using an existing hanging node.

    Breaks an E edge with r=1, b=0 if a node exists exactly at its midpoint.
    The edge is replaced by two E edges with r=0.
    """

    def get_left_side(self) -> Graph:
        """
        Left side:
        - v1 ---E(r=1,b=0)--- v2
        - hanging node h at the midpoint (not connected by edges)
        """
        g = Graph()

        v1 = Node(0, 0, "v1")
        v2 = Node(2, 0, "v2")
        h  = Node(1, 0, "h")  # midpoint

        g.add_node(v1)
        g.add_node(v2)
        g.add_node(h)

        g.add_edge(HyperEdge((v1, v2), "E", r=1, b=0))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        """
        Right side:
        - v1 ---E(r=0)--- h ---E(r=0)--- v2
        """
        g = Graph()

        # Extract nodes
        v1 = left.get_node("v1")
        v2 = left.get_node("v2")
        h  = left.get_node("h")

        # Original edge (to preserve b)
        edge = next(e for e in left.hyperedges if e.hypertag == "E")
        b_val = edge.b

        # Add nodes
        for n in (v1, v2, h):
            g.add_node(n)

        # Add new edges
        g.add_edge(HyperEdge((v1, h), "E", r=0, b=b_val), check_nodes=False)
        g.add_edge(HyperEdge((h, v2), "E", r=0, b=b_val), check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        """
        Conditions:
        - exactly one E edge
        - E has r=1 and b=0
        - one extra node exists at the geometric midpoint
        """
        e_edges = [e for e in matched_graph.hyperedges if e.hypertag == "E"]
        if len(e_edges) != 1:
            return False

        edge = e_edges[0]
        if edge.r != 1 or edge.b != 0:
            return False

        v1, v2 = edge.nodes
        mid_x = (v1.x + v2.x) / 2
        mid_y = (v1.y + v2.y) / 2
        eps = 1e-5

        for node in matched_graph.nodes:
            if node in (v1, v2):
                continue
            if abs(node.x - mid_x) < eps and abs(node.y - mid_y) < eps:
                return True

        return False
