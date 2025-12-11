from dataclasses import dataclass
from typing import Tuple
from node import Node


@dataclass
class HyperEdge:
    """
    Represents a hyperedge in the graph.

    A hyperedge connects any number of vertices (not just 2 like a regular edge).

    Attributes:
        nodes: Tuple of vertices connected by this hyperedge
        hypertag: Type of hyperedge (e.g., "E" - edge, "Q" - quadrilateral)
        r: R attribute used for production matching (0 or 1)
    """
    nodes: Tuple[Node, ...]
    hypertag: str
    r: int = 0

    def __post_init__(self):
        if len(self.nodes) < 2:
            raise ValueError("Hyperedge must connect at least 2 vertices")

    @property
    def label(self) -> str:
        """Generates a unique label for the hyperedge based on type and vertices."""
        node_labels = "_".join(n.label for n in self.nodes)
        return f"{self.hypertag}_{node_labels}"

    def __hash__(self):
        return hash((self.hypertag, self.nodes))

    def __eq__(self, other):
        if isinstance(other, HyperEdge):
            return self.hypertag == other.hypertag and set(self.nodes) == set(other.nodes)
        return False

    def __repr__(self):
        node_labels = ", ".join(n.label for n in self.nodes)
        return f"HyperEdge({self.hypertag}, [{node_labels}], r={self.r})"
