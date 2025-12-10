"""
Production P1: Split edge E into two.

Left side: Two nodes connected by hyperedge of type E
Right side: Three nodes (original n1, new middle node, original n2)
            connected by two hyperedges of type E
            
Example:
    n1 ---E--- n2
    
    is transformed into:
    
    n1 ---E--- n3 ---E--- n2
    
where n3 is the new node in the middle between n1 and n2.
"""

from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production


@Production.register
class P1(Production):
    """
    Production P1 - split edge of type E.
    
    Adds a new node between two existing nodes
    connected by a hyperedge of type E.
    """
    
    def get_left_side(self) -> Graph:
        """
        Creates the left side of the production.
        
        Returns:
            Graph with two nodes connected by hyperedge E
        """
        g = Graph()
        
        # Create two nodes (coordinates are placeholders)
        n1 = Node(0, 0, "n1")
        n2 = Node(0, 0, "n2")
        
        g.add_node(n1)
        g.add_node(n2)
        
        # Connect them with hyperedge of type E
        g.add_edge(HyperEdge((n1, n2), "E"))
        
        return g
    
    def get_right_side(self, left: Graph, lvl: int) -> Graph:
        """
        Creates the right side of the production based on the match.
        
        Args:
            left: Matched subgraph (with current coordinates)
            lvl: Recursion level
            
        Returns:
            Graph with new middle node and two E hyperedges
        """
        # Get matched nodes
        nodes = left.ordered_nodes
        n1 = None
        n2 = None
        hn1 = None  # node representing hyperedge
        
        for node in nodes:
            if node.hyperref is None:
                if n1 is None:
                    n1 = node
                else:
                    n2 = node
            else:
                hn1 = node
        
        g = Graph()
        
        # Calculate coordinates of new node (midpoint between n1 and n2)
        mid_x = (n1.x + n2.x) / 2
        mid_y = (n1.y + n2.y) / 2
        
        # Create new node
        # Set hanging to negation of boundary of original hyperedge
        is_hanging = not hn1.hyperref.boundary if hn1 and hn1.hyperref else False
        n3 = Node(mid_x, mid_y, f"{lvl}_n3", hanging=is_hanging)
        
        g.add_node(n3)
        
        # Preserve boundary property from original hyperedge
        boundary = hn1.hyperref.boundary if hn1 and hn1.hyperref else False
        
        # Create two new hyperedges
        # check_nodes=False because n1 and n2 are in the original graph, not this new one
        g.add_edge(HyperEdge((n1, n3), "E", boundary=boundary), check_nodes=False)
        g.add_edge(HyperEdge((n2, n3), "E", boundary=boundary), check_nodes=False)
        
        return g
