from dataclasses import dataclass
from typing import List, Optional, Iterator, Set
import networkx as nx
from node import Node
from edge import HyperEdge


@dataclass
class NodeCount:
    """Stores counts of different node types in the graph."""
    normal: int = 0
    hyper: int = 0


class Graph:
    """
    Class representing a graph with hyperedges.
    
    Since networkx doesn't support hyperedges natively,
    we convert each hyperedge to a special node connected
    to all vertices that the hyperedge connects.
    """
    
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes: dict[str, Node] = {}
        self._hyperedges: dict[str, HyperEdge] = {}
    
    def add_node(self, node: Node) -> None:
        """Adds a vertex to the graph."""
        self._nodes[node.label] = node
        self._graph.add_node(node.label, node=node, is_hyper=False)
    
    def add_edge(self, edge: HyperEdge, check_nodes: bool = True) -> None:
        """
        Adds a hyperedge to the graph.
        
        The hyperedge is represented as a special node
        connected to all vertices it connects.
        
        Args:
            edge: Hyperedge to add
            check_nodes: Whether to check node existence (False for productions)
        """
        hyper_label = edge.label
        
        center_x = sum(n.x for n in edge.nodes) / len(edge.nodes)
        center_y = sum(n.y for n in edge.nodes) / len(edge.nodes)
        
        hyper_node = Node(center_x, center_y, hyper_label, hyperref=edge)
        
        self._hyperedges[hyper_label] = edge
        self._graph.add_node(hyper_label, node=hyper_node, is_hyper=True, hyperedge=edge)
        
        for node in edge.nodes:
            if check_nodes and node.label not in self._nodes:
                raise ValueError(f"Node {node.label} does not exist in the graph")
            if node.label not in self._nodes:
                self._nodes[node.label] = node
                self._graph.add_node(node.label, node=node, is_hyper=False)
            self._graph.add_edge(hyper_label, node.label)
    
    def get_node(self, label: str) -> Optional[Node]:
        """Returns the node with the given label."""
        return self._nodes.get(label)
    
    def get_hyperedge(self, label: str) -> Optional[HyperEdge]:
        """Returns the hyperedge with the given label."""
        return self._hyperedges.get(label)
    
    @property
    def nodes(self) -> List[Node]:
        """Returns list of all regular vertices."""
        return list(self._nodes.values())
    
    @property
    def hyperedges(self) -> List[HyperEdge]:
        """Returns list of all hyperedges."""
        return list(self._hyperedges.values())
    
    @property
    def ordered_nodes(self) -> List[Node]:
        """
        Returns list of all nodes (regular and hyper) in order.
        Used for production matching.
        """
        result = []
        for label, data in self._graph.nodes(data=True):
            result.append(data['node'])
        return result
    
    def count_nodes(self) -> NodeCount:
        """Counts nodes in the graph by type."""
        return NodeCount(normal=len(self._nodes), hyper=len(self._hyperedges))
    
    def find_subgraph_isomorphisms(self, pattern: 'Graph') -> List[dict]:
        """
        Finds all subgraph isomorphisms (pattern matches).

        Returns:
            List of dictionaries mapping pattern labels to graph labels
        """
        def node_match(n1, n2):
            if n1.get('is_hyper') != n2.get('is_hyper'):
                return False
            if n1.get('is_hyper'):
                e1 = n1.get('hyperedge')
                e2 = n2.get('hyperedge')
                if e1 and e2:
                    return e1.hypertag == e2.hypertag and e1.r == e2.r
            return True

        matcher = nx.algorithms.isomorphism.GraphMatcher(
            self._graph,
            pattern._graph,
            node_match=node_match
        )
        return list(matcher.subgraph_isomorphisms_iter())
    
    def remove_node(self, label: str) -> None:
        """Removes a node from the graph."""
        if label in self._nodes:
            del self._nodes[label]
        if label in self._hyperedges:
            del self._hyperedges[label]
        if self._graph.has_node(label):
            self._graph.remove_node(label)
    
    def apply(self, production: 'Production') -> int:
        """
        Applies a production to the graph.
        
        Returns:
            Number of times the production was applied
        """
        left = production.get_left_side()
        applied_count = 0
        
        while True:
            matches = self.find_subgraph_isomorphisms(left)
            if not matches:
                break
            
            match = matches[0]
            
            valid = all(self._graph.has_node(graph_label) for graph_label in match.keys())
            if not valid:
                break
            
            matched_graph = Graph()
            for graph_label, pattern_label in match.items():
                node_data = self._graph.nodes[graph_label]
                matched_graph._graph.add_node(pattern_label, **node_data)
                if not node_data.get('is_hyper', False):
                    matched_graph._nodes[pattern_label] = node_data['node']
                else:
                    matched_graph._hyperedges[pattern_label] = node_data.get('hyperedge')

            right = production.get_right_side(matched_graph, lvl=applied_count)

            inv_match = {v: k for k, v in match.items()}
            for label, data in left._graph.nodes(data=True):
                if data.get('is_hyper', False):
                    graph_label = inv_match[label]
                    self.remove_node(graph_label)
            
            for node in right.nodes:
                if node.label not in self._nodes:
                    self.add_node(node)
            
            for edge in right.hyperedges:
                self.add_edge(edge, check_nodes=False)
            
            applied_count += 1
        
        return applied_count
    
    def __repr__(self):
        return f"Graph(nodes={len(self._nodes)}, hyperedges={len(self._hyperedges)})"
