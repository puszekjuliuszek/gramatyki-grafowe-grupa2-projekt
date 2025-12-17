from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P7(Production):
    def get_left_side(self) -> Graph:
        g = Graph()
        
        n1 = Node(0, 0, "n1")
        n2 = Node(1, 0, "n2")
        n3 = Node(1, 1, "n3")
        n4 = Node(0, 1, "n4")
        n5 = Node(1 + (2 ** 0.5)/2 , 1/2, "n5")

        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_node(n4)
        g.add_node(n5)

        g.add_edge(HyperEdge((n1, n2), "E"))
        g.add_edge(HyperEdge((n2, n3), "E"))
        g.add_edge(HyperEdge((n3, n4), "E"))
        g.add_edge(HyperEdge((n4, n5), "E"))
        g.add_edge(HyperEdge((n5, n1), "E"))

        p_edge = HyperEdge((n1, n2, n3, n4, n5), "P", r=1)
        g.add_edge(p_edge)

        return g

    def get_right_side(self, left: Graph) -> Graph:
        g = Graph()

        nodes = []
        for node in left.ordered_nodes:
            if node.hyperref is None:
                nodes.append(node)

        for edge in left.hyperedges:
            if edge.hypertag == "P":
                new_p = HyperEdge(edge.nodes, "P", r=1)
                g.add_edge(new_p, check_nodes=False)
            elif edge.hypertag == "E":
                new_e = HyperEdge(edge.nodes, "E", r=1)
                g.add_edge(new_e, check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        p_edge_found = False
        e_edges = []

        for edge in matched_graph.hyperedges:
            if edge.hypertag == "P":
                if getattr(edge, "r", 0) == 1:
                    p_edge_found = True
                else:
                    return False
            elif edge.hypertag == "E":
                e_edges.append(edge)

        if not p_edge_found:
            return False
        
        if all(getattr(e, "r", 0) == 1 for e in e_edges):
            return False
            
        return True