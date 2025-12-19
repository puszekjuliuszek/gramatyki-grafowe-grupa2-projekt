from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


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

        nodes = []
        for node in left.ordered_nodes:
            if node.hyperref is None:
                nodes.append(node)

        center_nodes = [nodes[0], nodes[2], nodes[4], nodes[6], nodes[8], nodes[10]]
        sum_x = sum(n.x for n in center_nodes)
        sum_y = sum(n.y for n in center_nodes)
        center = Node(sum_x/6, sum_y/6, "center")
        g.add_node(center)


        for edge in left.hyperedges:
            if edge.hypertag == "E":
                g.add_edge(HyperEdge(edge.nodes, "E", r=edge.r, b=edge.b), check_nodes=False)

        n = len(nodes)
        for i in range(1, n, 2):
            g.add_edge(HyperEdge((nodes[i], center), "E", b=0), check_nodes=False)
        
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
