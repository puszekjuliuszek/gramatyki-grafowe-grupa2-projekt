"""
Production P9

Left side: A hexagonal element consisting of 6 outer nodes:
           - 6 boundary 'E' hyperedges connecting the outer nodes
           - 1 central 'S' hyperedge connecting all 6 nodes
           The S hyperedge has r=0.

Right side: Same structure but S hyperedge has r=1.
"""

from src.edge import HyperEdge
from src.graph import Graph
from src.node import Node
from src.productions.production import Production


@Production.register
class P9(Production):

    def get_left_side(self) -> Graph:
        g = Graph()
        n1 = Node(1, 0, "n1")
        n2 = Node(0.5, 0.866, "n2")
        n3 = Node(-0.5, 0.866, "n3")
        n4 = Node(-1, 0, "n4")
        n5 = Node(-0.5, -0.866, "n5")
        n6 = Node(0.5, -0.866, "n6")

        nodes = [n1, n2, n3, n4, n5, n6]
        for n in nodes:
            g.add_node(n)

        g.add_edge(HyperEdge((n1, n2), "E"))
        g.add_edge(HyperEdge((n2, n3), "E"))
        g.add_edge(HyperEdge((n3, n4), "E"))
        g.add_edge(HyperEdge((n4, n5), "E"))
        g.add_edge(HyperEdge((n5, n6), "E"))
        g.add_edge(HyperEdge((n6, n1), "E"))


        g.add_edge(HyperEdge(tuple(nodes), "S", r=0))

        return g

    def get_right_side(self, left: Graph) -> Graph:
        g = Graph()

        nodes = []
        for node in left.ordered_nodes:
            if node.hyperref is None:
                nodes.append(node)
                g.add_node(node)

        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r), check_nodes=False)


        g.add_edge(HyperEdge(tuple(nodes), "S", r=1), check_nodes=False)

        return g

    def filter_match(self, matched_graph: Graph) -> bool:
        for edge in matched_graph.hyperedges:
            if edge.hypertag == "S" and edge.r != 0:
                return False
        return True