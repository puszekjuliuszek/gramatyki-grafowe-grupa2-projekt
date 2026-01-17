from graph import Graph
from edge import HyperEdge

class P6:
    def apply(self, graph: Graph):
        """
        Wykonuje produkcję P6 (Marking) na podanym grafie.
        Zmienia atrybut R hiperkrawędzi o etykiecie 'P' z 0 na 1.
        """
        candidates = self._find_applicable_edges(graph)
        
        if not candidates:
            return False

        for edge in candidates:
            print(f"Applying P6: Marking edge {edge.label} (P) for refinement (R=1)")
            edge.r = 1
            
        return True

    # def _find_applicable_edges(self, graph: Graph):
    #     candidates = []
    #     for edge in graph.hyperedges:
    #         if edge.hypertag != 'P' or edge.r != 0:
    #             continue

    #         if len(edge.nodes) != 5:
    #             continue
            
    #         candidates.append(edge)
        
    #     return candidates

    def _find_applicable_edges(self, graph: Graph):
        candidates = []
        for edge in graph.hyperedges:
            if edge.hypertag != 'P' or edge.r != 0:
                continue

            if len(edge.nodes) != 5:
                continue

            pentagon_nodes = set(edge.nodes)
            boundary_edges_count = 0
            
            for potential_boundary in graph.hyperedges:
                if potential_boundary.hypertag == 'E' and len(potential_boundary.nodes) == 2:
                    n1, n2 = potential_boundary.nodes
                    if n1 in pentagon_nodes and n2 in pentagon_nodes:
                        boundary_edges_count += 1
            
            if boundary_edges_count == 5:
                candidates.append(edge)
        
        return candidates