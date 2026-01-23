from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P12(Production):
    
    def get_left_side(self) -> Graph:
        g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(1, 0, "n2")
        n3 = Node(1.5, 0.5, "n3")
        n4 = Node(1, 1, "n4")
        n5 = Node(0.5, 1.25, "n5")
        n6 = Node(0, 1, "n6")
        n7 = Node(-0.5, 0.5, "n7")
        nodes = [n1, n2, n3, n4, n5, n6, n7]
        for n in nodes:
            g.add_node(n)
        
        # E edges around the boundary (cycle)
        for i in range(len(nodes)):
            g.add_edge(HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), "E"))
        
        # T hyperedge in the middle with r=0 connecting all nodes
        g.add_edge(HyperEdge(tuple(nodes), "T", r=0))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        """
        Same structure, but change T.r from 0 to 1.
        """
        g = Graph()

        # collect normal nodes (exclude hyper-nodes)
        normal_nodes = [node for node in left.ordered_nodes if node.hyperref is None]

        # keep boundary E edges as-is
        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)

        # rebuild T using all normal nodes
        g.add_edge(HyperEdge(tuple(normal_nodes), "T", r=1), check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        """Only match T hyperedges with r=0."""
        for edge in matched_graph.hyperedges:
            if edge.hypertag == "T" and edge.r != 0:
                return False
        return True