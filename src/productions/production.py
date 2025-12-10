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
    def get_right_side(self, left: Graph, lvl: int) -> Graph:
        """
        Returns the right side of the production (transformation result).
        
        Args:
            left: Matched subgraph from the left side (with current values)
            lvl: Recursion level / application number
            
        Returns:
            Graph representing the transformation result
        """
        pass
