from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Node:
    """
    Represents a vertex in the graph.
    
    Attributes:
        x: X coordinate of the vertex
        y: Y coordinate of the vertex
        label: Vertex label (unique identifier)
        hanging: Whether the vertex is a hanging node
        hyperref: Reference to hyperedge (if this node represents a hyperedge)
    """
    x: float
    y: float
    label: str
    hanging: bool = False
    hyperref: Optional[Any] = None
    
    def __hash__(self):
        return hash(self.label)
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.label == other.label
        return False
    
    def __repr__(self):
        return f"Node({self.label}, x={self.x}, y={self.y}, hanging={self.hanging})"
