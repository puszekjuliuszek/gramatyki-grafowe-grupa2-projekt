import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p5 import P5
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


class TestP5BasicApplication:
    """
    Test Case: Basic correct application.
    
    Checks if P5 correctly applies to a single, isolated quadrilateral 
    where the Q hyperedge has R=1 and all E hyperedges have R=0.
    All outer edges are boundary edges (b=1) since this is an isolated element.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        # Corner nodes
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 0, "n2")
        n3 = Node(4, 4, "n3")
        n4 = Node(0, 4, "n4")
        
        # Midpoint nodes
        n5 = Node(2, 0, "n5")
        n6 = Node(4, 2, "n6")
        n7 = Node(2, 4, "n7")
        n8 = Node(0, 2, "n8")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            self.g.add_node(node)
        
        # E hyperedges (all R=0, all boundary b=1 since isolated element)
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0, b=1))
        
        # Q hyperedge (R=1)
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1, b=0))
        
        self.p5 = P5()

    def test_before(self):
        """Test input graph structure before application."""
        draw(self.g, str(DRAW_DIR / "test5-case1-before.png"))
        
        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 1
        assert q_edges[0].r == 1
        
        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert len(e_edges) == 8
        assert all(e.r == 0 for e in e_edges)

    def test_after(self):
        """
        Test graph structure after application.
        
        Expectations:
        - 1 central vertex V added.
        - 4 new Q hyperedges created (all R=0).
        - Total 9 nodes, 16 hyperedges.
        """
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-case1-after.png"))
        
        assert applied == 1, "Production should be applied exactly once"
        
        # Check node count: 8 original + 1 new center = 9
        cnt = self.g.count_nodes()
        assert cnt.normal == 9, f"Should have 9 nodes (8 original + 1 V), got {cnt.normal}"

        # Check total hyperedges:
        # Original: 8 E + 1 Q = 9
        # Removed: 1 Q = -1
        # Added: 4 Q + 4 E = +8
        # Total: 9 - 1 + 8 = 16
        assert len(self.g.hyperedges) == 16, f"Should have 16 hyperedges, got {len(self.g.hyperedges)}"
        
        # Check Q hyperedges
        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 4, f"Should have 4 Q hyperedges, got {len(q_edges)}"
        assert all(e.r == 0 for e in q_edges), "All Q hyperedges should have r=0"
        assert all(e.b == 0 for e in q_edges), "All Q hyperedges should have b=0"
        
        # Check E hyperedges - outer edges should preserve b=1, inner edges should be b=0
        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        v = [n for n in self.g.nodes if n.label.startswith("V_")][0]
        outer_edges = [e for e in e_edges if v not in e.nodes]
        inner_edges = [e for e in e_edges if v in e.nodes]
        
        assert len(outer_edges) == 8, f"Should have 8 outer edges, got {len(outer_edges)}"
        assert all(e.b == 1 for e in outer_edges), "All outer edges should preserve b=1"
        assert len(inner_edges) == 4, f"Should have 4 inner edges, got {len(inner_edges)}"
        assert all(e.b == 0 for e in inner_edges), "All inner edges should have b=0"
        
        # Check central vertex exists
        v_nodes = [n for n in self.g.nodes if n.label.startswith("V_")]
        assert len(v_nodes) == 1, "Should have exactly one central vertex V"
        v = v_nodes[0]
        assert v.x == 2.0, f"V should be at x=2.0, got {v.x}"
        assert v.y == 2.0, f"V should be at y=2.0, got {v.y}"


class TestP5NoMatchQNotMarked:
    """
    Test Case: Production rejected due to Q attribute.
    
    Checks that P5 does NOT apply if the Q hyperedge has R=0 
    (meaning it is not marked for refinement).
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 0, "n2")
        n3 = Node(4, 4, "n3")
        n4 = Node(0, 4, "n4")
        n5 = Node(2, 0, "n5")
        n6 = Node(4, 2, "n6")
        n7 = Node(2, 4, "n7")
        n8 = Node(0, 2, "n8")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            self.g.add_node(node)
        
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0, b=1))
        
        # Q with R=0 (not marked for refinement)
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0, b=0))
        
        self.p5 = P5()

    def test_no_match(self):
        """Production should not apply."""
        draw(self.g, str(DRAW_DIR / "test5-case2.png"))
        
        applied = self.g.apply(self.p5)
        assert applied == 0, "Production should not apply when Q has r=0"


class TestP5NoMatchEdgeNotBroken:
    """
    Test Case: Production rejected due to E attribute.
    
    Checks that P5 does NOT apply if any boundary edge E has R=1
    (meaning the edge itself still needs refinement).
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 0, "n2")
        n3 = Node(4, 4, "n3")
        n4 = Node(0, 4, "n4")
        n5 = Node(2, 0, "n5")
        n6 = Node(4, 2, "n6")
        n7 = Node(2, 4, "n7")
        n8 = Node(0, 2, "n8")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            self.g.add_node(node)
        
        # Some E edges with R=1 (not all broken) - first edge not broken yet
        self.g.add_edge(HyperEdge((n1, n5), "E", r=1, b=1))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0, b=1))
        
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1, b=0))
        
        self.p5 = P5()

    def test_no_match(self):
        """Production should not apply."""
        draw(self.g, str(DRAW_DIR / "test5-case3.png"))
        
        applied = self.g.apply(self.p5)
        assert applied == 0, "Production should not apply when not all E have r=0"


class TestP5MultipleConnectedComponents:
    """
    Test Case: Multiple instances applied independently.
    
    Checks if P5 applies correctly to two connected quadrilaterals.
    Tests locality of the production and ability to handle larger graphs.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        # First quadrilateral
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")
        n5 = Node(1, 0, "n5")
        n6 = Node(2, 1, "n6")
        n7 = Node(1, 2, "n7")
        n8 = Node(0, 1, "n8")
        
        # Second quadrilateral (separate)
        n9 = Node(5, 0, "n9")
        n10 = Node(7, 0, "n10")
        n11 = Node(7, 2, "n11")
        n12 = Node(5, 2, "n12")
        n13 = Node(6, 0, "n13")
        n14 = Node(7, 1, "n14")
        n15 = Node(6, 2, "n15")
        n16 = Node(5, 1, "n16")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16]:
            self.g.add_node(node)
        
        # First quadrilateral edges
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0))
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        # Second quadrilateral edges
        self.g.add_edge(HyperEdge((n9, n13), "E", r=0))
        self.g.add_edge(HyperEdge((n13, n10), "E", r=0))
        self.g.add_edge(HyperEdge((n10, n14), "E", r=0))
        self.g.add_edge(HyperEdge((n14, n11), "E", r=0))
        self.g.add_edge(HyperEdge((n11, n15), "E", r=0))
        self.g.add_edge(HyperEdge((n15, n12), "E", r=0))
        self.g.add_edge(HyperEdge((n12, n16), "E", r=0))
        self.g.add_edge(HyperEdge((n16, n9), "E", r=0))
        self.g.add_edge(HyperEdge((n9, n10, n11, n12), "Q", r=1))

        # Connection between graphs (as requested)
        self.g.add_edge(HyperEdge((n2, n9), "E", r=0))
        
        self.p5 = P5()

    def test_multiple_applications(self):
        """Production should be applied to both quadrilaterals."""
        draw(self.g, str(DRAW_DIR / "test5-case4-before.png"))
        
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-case4-after.png"))
        
        assert applied == 2, f"Production should be applied 2 times, got {applied}"
        
        # Check node count: 16 original + 2 new centers = 18
        cnt = self.g.count_nodes()
        assert cnt.normal == 18, f"Should have 18 nodes, got {cnt.normal}"

        # Check total hyperedges: 
        # Original: 8 E + 1 Q (quad 1) + 8 E + 1 Q (quad 2) + 1 E (connection) = 19
        # Removed: 1 Q per quad = -2
        # Added: 4 Q + 4 E per quad = +16
        # Total: 19 - 2 + 16 = 33
        assert len(self.g.hyperedges) == 33, f"Should have 33 hyperedges, got {len(self.g.hyperedges)}"
        
        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 8, f"Should have 8 Q hyperedges (4 per quadrilateral), got {len(q_edges)}"
        assert all(e.r == 0 for e in q_edges), "All Q hyperedges should have r=0"
        
        # Check that two central vertices exist
        v_nodes = [n for n in self.g.nodes if n.label.startswith("V_")]
        assert len(v_nodes) == 2, f"Should have 2 central vertices, got {len(v_nodes)}"


class TestP5NoMatchMissingNode:
    """
    Test Case: Structurally invalid input (Missing Node).
    
    Checks that P5 does NOT apply if a required midpoint node is missing.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 0, "n2")
        n3 = Node(4, 4, "n3")
        n4 = Node(0, 4, "n4")
        
        # Only 3 midpoints (missing n8)
        n5 = Node(2, 0, "n5")
        n6 = Node(4, 2, "n6")
        n7 = Node(2, 4, "n7")
        # n8 missing
        
        for node in [n1, n2, n3, n4, n5, n6, n7]:
            self.g.add_node(node)
        
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0))
        # Missing edges for n8
        
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        self.p5 = P5()

    def test_no_match_missing_midpoint(self):
        """Production should not apply when structure is incomplete."""
        draw(self.g, str(DRAW_DIR / "test5-case5.png"))
        
        applied = self.g.apply(self.p5)
        assert applied == 0, "Production should not apply when structure is incomplete"


class TestP5GeometricRobustness:
    """
    Test Case: Geometric Robustness.
    
    Checks if P5 applies correctly to a distorted (non-rectagonal) quadrilateral.
    Verifies that the topological match works regardless of node positions.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        # Rotated/Distorted coordinates
        # Center roughly at (3, 3)
        n1 = Node(1, 1, "n1")  # Bottom-left
        n2 = Node(5, 1, "n2")  # Bottom-right
        n3 = Node(6, 4, "n3")  # Top-right (skewed)
        n4 = Node(2, 5, "n4")  # Top-left (skewed)
        
        # Midpoints (approximate)
        n5 = Node(3, 1, "n5")    # Bottom
        n6 = Node(5.5, 2.5, "n6") # Right
        n7 = Node(4, 4.5, "n7")  # Top
        n8 = Node(1.5, 3, "n8")  # Left
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            self.g.add_node(node)
        
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0))
        
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        self.p5 = P5()

    def test_distorted_application(self):
        """Production should apply correctly to distorted shapes."""
        draw(self.g, str(DRAW_DIR / "test5-case6-before.png"))
        
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-case6-after.png"))
        
        assert applied == 1
        
        # Check node count
        cnt = self.g.count_nodes()
        assert cnt.normal == 9
        
        # Check Q edges
        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 4
        
        # Verify central vertex is inside the bounding box
        v = [n for n in self.g.nodes if n.label.startswith("V_")][0]
        assert 1 < v.x < 6
        assert 1 < v.y < 5


class TestP5BoundaryAttributes:
    """
    Test Case: Boundary Attribute (b) Preservation.
    
    Checks that the production preserves the 'b' attribute (boundary vs internal) 
    of existing E edges.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        # Standard layout
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")
        n5 = Node(1, 0, "n5")
        n6 = Node(2, 1, "n6")
        n7 = Node(1, 2, "n7")
        n8 = Node(0, 1, "n8")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            self.g.add_node(node)
        
        # E hyperedges with mixed b values
        # Bottom edge (n1-n5-n2) is boundary (b=1)
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0, b=1))
        
        # Right edge (n2-n6-n3) is internal (b=0)
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0, b=0))
        
        # Top edge (n3-n7-n4) is boundary (b=1)
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0, b=1))
        
        # Left edge (n4-n8-n1) is internal (b=0)
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0, b=0))
        
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        self.p5 = P5()

    def test_boundary_preservation(self):
        """Test that b attributes are preserved on split edges."""
        draw(self.g, str(DRAW_DIR / "test5-boundary-before.png"))
        
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-boundary-after.png"))
        
        assert applied == 1
        
        # Verify outer edges preserved their b values
        # Helper to find edge by nodes (order insensitive)
        def get_edge_b(u, v):
            for e in self.g.hyperedges:
                if e.hypertag == "E" and set(e.nodes) == {u, v}:
                    return e.b
            return None

        nodes = {n.label: n for n in self.g.nodes}
        n1, n2, n3, n4 = nodes["n1"], nodes["n2"], nodes["n3"], nodes["n4"]
        n5, n6, n7, n8 = nodes["n5"], nodes["n6"], nodes["n7"], nodes["n8"]
        
        # Bottom (b=1)
        assert get_edge_b(n1, n5) == 1
        assert get_edge_b(n5, n2) == 1
        
        # Right (b=0)
        assert get_edge_b(n2, n6) == 0
        assert get_edge_b(n6, n3) == 0
        
        # Top (b=1)
        assert get_edge_b(n3, n7) == 1
        assert get_edge_b(n7, n4) == 1
        
        # Left (b=0)
        assert get_edge_b(n4, n8) == 0
        assert get_edge_b(n8, n1) == 0
        
        # Verify new internal edges (to center) are b=0
        v = [n for n in self.g.nodes if n.label.startswith("V_")][0]
        assert get_edge_b(n5, v) == 0
        assert get_edge_b(n6, v) == 0
        assert get_edge_b(n7, v) == 0
        assert get_edge_b(n8, v) == 0


class TestP5NegativeCases:
    """
    Test Case: Structural Invalidity (Missing Edge).
    
    Checks that P5 does NOT apply if a required E hyperedge is missing.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        self.nodes = {}
        
        # Create full set of nodes
        for i, (x, y) in enumerate([(0,0), (2,0), (2,2), (0,2), (1,0), (2,1), (1,2), (0,1)]):
            n = Node(x, y, f"n{i+1}")
            self.nodes[f"n{i+1}"] = n
            self.g.add_node(n)
        
        self.p5 = P5()

    def _add_edges(self, skip_edge_idx=None):
        n = self.nodes
        edges = [
            (n["n1"], n["n5"]), (n["n5"], n["n2"]),
            (n["n2"], n["n6"]), (n["n6"], n["n3"]),
            (n["n3"], n["n7"]), (n["n7"], n["n4"]),
            (n["n4"], n["n8"]), (n["n8"], n["n1"])
        ]
        
        for i, (u, v) in enumerate(edges):
            if skip_edge_idx is not None and i == skip_edge_idx:
                continue
            self.g.add_edge(HyperEdge((u, v), "E", r=0))
            
        self.g.add_edge(HyperEdge((n["n1"], n["n2"], n["n3"], n["n4"]), "Q", r=1))

    def test_missing_edge(self):
        """Production should not apply if one E edge is missing."""
        self._add_edges(skip_edge_idx=0) # Skip first edge
        
        draw(self.g, str(DRAW_DIR / "test5-neg-missing-edge.png"))
        applied = self.g.apply(self.p5)
        assert applied == 0

class TestP5BoundaryAttributes:
    """Test: Preservation of boundary attributes (b=0/1)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        # Standard layout
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")
        n5 = Node(1, 0, "n5")
        n6 = Node(2, 1, "n6")
        n7 = Node(1, 2, "n7")
        n8 = Node(0, 1, "n8")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            self.g.add_node(node)
        
        # E hyperedges with mixed b values
        # Bottom edge (n1-n5-n2) is boundary (b=1)
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0, b=1))
        
        # Right edge (n2-n6-n3) is internal (b=0)
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0, b=0))
        
        # Top edge (n3-n7-n4) is boundary (b=1)
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0, b=1))
        
        # Left edge (n4-n8-n1) is internal (b=0)
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0, b=0))
        
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        self.p5 = P5()

    def test_boundary_preservation(self):
        """Test that b attributes are preserved on split edges."""
        draw(self.g, str(DRAW_DIR / "test5-boundary-before.png"))
        
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-boundary-after.png"))
        
        assert applied == 1
        
        # Verify outer edges preserved their b values
        # Helper to find edge by nodes (order insensitive)
        def get_edge_b(u, v):
            for e in self.g.hyperedges:
                if e.hypertag == "E" and set(e.nodes) == {u, v}:
                    return e.b
            return None

        nodes = {n.label: n for n in self.g.nodes}
        n1, n2, n3, n4 = nodes["n1"], nodes["n2"], nodes["n3"], nodes["n4"]
        n5, n6, n7, n8 = nodes["n5"], nodes["n6"], nodes["n7"], nodes["n8"]
        
        # Bottom (b=1)
        assert get_edge_b(n1, n5) == 1
        assert get_edge_b(n5, n2) == 1
        
        # Right (b=0)
        assert get_edge_b(n2, n6) == 0
        assert get_edge_b(n6, n3) == 0
        
        # Top (b=1)
        assert get_edge_b(n3, n7) == 1
        assert get_edge_b(n7, n4) == 1
        
        # Left (b=0)
        assert get_edge_b(n4, n8) == 0
        assert get_edge_b(n8, n1) == 0
        
        # Verify new internal edges (to center) are b=0
        v = [n for n in self.g.nodes if n.label.startswith("V_")][0]
        assert get_edge_b(n5, v) == 0
        assert get_edge_b(n6, v) == 0
        assert get_edge_b(n7, v) == 0
        assert get_edge_b(n8, v) == 0


class TestP5NegativeCases:
    """Test: Negative scenarios (missing edges/nodes)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        self.nodes = {}
        
        # Create full set of nodes
        for i, (x, y) in enumerate([(0,0), (2,0), (2,2), (0,2), (1,0), (2,1), (1,2), (0,1)]):
            n = Node(x, y, f"n{i+1}")
            self.nodes[f"n{i+1}"] = n
            self.g.add_node(n)
        
        self.p5 = P5()

    def _add_edges(self, skip_edge_idx=None):
        n = self.nodes
        edges = [
            (n["n1"], n["n5"]), (n["n5"], n["n2"]),
            (n["n2"], n["n6"]), (n["n6"], n["n3"]),
            (n["n3"], n["n7"]), (n["n7"], n["n4"]),
            (n["n4"], n["n8"]), (n["n8"], n["n1"])
        ]
        
        for i, (u, v) in enumerate(edges):
            if skip_edge_idx is not None and i == skip_edge_idx:
                continue
            self.g.add_edge(HyperEdge((u, v), "E", r=0))
            
        self.g.add_edge(HyperEdge((n["n1"], n["n2"], n["n3"], n["n4"]), "Q", r=1))

    def test_missing_edge(self):
        """Production should not apply if one E edge is missing."""
        self._add_edges(skip_edge_idx=0) # Skip first edge
        
        draw(self.g, str(DRAW_DIR / "test5-neg-missing-edge.png"))
        applied = self.g.apply(self.p5)
        assert applied == 0


class TestP5AllBoundaryEdges:
    """
    Test Case: All edges are boundary edges (b=1).
    
    Verifies that P5 applies correctly when all outer edges are
    boundary edges and that these b=1 values are preserved.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")
        n5 = Node(1, 0, "n5")
        n6 = Node(2, 1, "n6")
        n7 = Node(1, 2, "n7")
        n8 = Node(0, 1, "n8")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            self.g.add_node(node)
        
        # All edges are boundary (b=1)
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0, b=1))
        
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        self.p5 = P5()

    def test_all_boundary_edges(self):
        """Production should apply and preserve b=1 on all outer edges."""
        draw(self.g, str(DRAW_DIR / "test5-all-boundary-before.png"))
        
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-all-boundary-after.png"))
        
        assert applied == 1, "Production should apply regardless of b values"
        
        # All outer edges should still have b=1
        outer_edges = [e for e in self.g.hyperedges 
                       if e.hypertag == "E" and not any(n.label.startswith("V_") for n in e.nodes)]
        assert all(e.b == 1 for e in outer_edges), "All outer edges should have b=1"
        
        # New internal edges (to center) should have b=0
        v = [n for n in self.g.nodes if n.label.startswith("V_")][0]
        internal_edges = [e for e in self.g.hyperedges 
                          if e.hypertag == "E" and v in e.nodes]
        assert len(internal_edges) == 4, "Should have 4 internal edges"
        assert all(e.b == 0 for e in internal_edges), "All internal edges should have b=0"


class TestP5AllInternalEdges:
    """
    Test Case: All edges are internal edges (b=0).
    
    Verifies that P5 applies correctly when all outer edges are
    internal edges and that these b=0 values are preserved.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")
        n5 = Node(1, 0, "n5")
        n6 = Node(2, 1, "n6")
        n7 = Node(1, 2, "n7")
        n8 = Node(0, 1, "n8")
        
        for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
            self.g.add_node(node)
        
        # All edges are internal (b=0)
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0, b=0))
        
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        self.p5 = P5()

    def test_all_internal_edges(self):
        """Production should apply and preserve b=0 on all edges."""
        draw(self.g, str(DRAW_DIR / "test5-all-internal-before.png"))
        
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-all-internal-after.png"))
        
        assert applied == 1, "Production should apply regardless of b values"
        
        # All E edges should have b=0 (outer preserved, new are also b=0)
        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.b == 0 for e in e_edges), "All edges should have b=0"
