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

        g.add_edge(HyperEdge((n1, n2), "E"))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        g = Graph()
        edge = left.hyperedges[0]
        n1, n2 = edge.nodes

        g.add_node(n1)
        g.add_node(n2)
        edge.r=0
        g.add_edge(edge)

        new_x = (n1.x + n2.x) / 2
        new_y = (n1.y + n2.y) / 2
        
        new_node = Node(new_x, new_y, "n3")

        g.add_node(new_node)
        e1 = HyperEdge((n1, new_node), "E", r=0, b=edge.b)
        e2 = HyperEdge((new_node, n2), "E", r=0, b=edge.b)

        g.add_edge(e1, check_nodes=False)
        g.add_edge(e2, check_nodes=False)

        return g

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