from abc import ABC, abstractmethod
from graph import Graph


class Production(ABC):
    """
    Abstract base class for graph grammar productions.
    
    Each production defines a left side (pattern to match)
    and a right side (transformation result).
    """
    
    _registry: list = []
    
    @classmethod
    def register(cls, production_cls):
        """Decorator for registering productions."""
        cls._registry.append(production_cls)
        return production_cls
    
    @classmethod
    def get_all_productions(cls):
        """Returns all registered productions."""
        return [p() for p in cls._registry]
    
    @abstractmethod
    def get_left_side(self) -> Graph:
        """
        Returns the left side of the production (pattern).
        
        Returns:
            Graph representing the pattern to match
        """
        pass
    
    @abstractmethod
    def get_right_side(self, left: Graph) -> Graph:
        """
        Returns the right side of the production (transformation result).

        Args:
            left: Matched subgraph from the left side (with current values)

        Returns:
            Graph representing the transformation result
        """
        pass

    def filter_match(self, matched_graph: Graph) -> bool:
        """
        Additional filter for matched subgraphs.

        Override this method to add custom filtering logic
        beyond structural isomorphism.

        Args:
            matched_graph: The matched subgraph

        Returns:
            True if the match should be accepted, False to reject
        """
        return True
