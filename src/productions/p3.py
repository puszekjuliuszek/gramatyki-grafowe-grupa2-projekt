from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P3(Production):

    def get_left_side(self) -> Graph:
        g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 1, "n2")

        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(HyperEdge((n1, n2), "E", r=1, b=0))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        edge = left.hyperedges[0]
        n1, n2 = edge.nodes

        new_node = Node(
            (n1.x + n2.x) / 2,
            (n1.y + n2.y) / 2,
            ""
        )

        left._nodes[new_node.label] = new_node

        left.add_edge(
            HyperEdge((n1, new_node), "E", r=0, b=edge.b),
            check_nodes=False
        )
        left.add_edge(
            HyperEdge((n2, new_node), "E", r=0, b=edge.b),
            check_nodes=False
        )

        edge.r = 0
        return left

    def filter_match(self, matched_graph: Graph) -> bool:
        if len(matched_graph.hyperedges) != 1:
            return False
            
        edge = matched_graph.hyperedges[0]
        
        if edge.hypertag != "E":
            return False
            
        # Check attributes r=1 and b=0
        if getattr(edge, "r", 0) != 1 or getattr(edge, "b", 1) != 0:
            return False
            
        return True