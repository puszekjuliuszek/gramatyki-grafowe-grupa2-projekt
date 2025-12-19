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


class TestP5Case1:
    """Test: Basic quadrilateral with all edges broken."""

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
        
        # E hyperedges (all R=0)
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0))
        
        # Q hyperedge (R=1)
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        self.p5 = P5()

    def test_before(self):
        """Test input graph."""
        draw(self.g, str(DRAW_DIR / "test5-case1-before.png"))
        
        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 1
        assert q_edges[0].r == 1
        
        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert len(e_edges) == 8
        assert all(e.r == 0 for e in e_edges)

    def test_after(self):
        """Test after applying production."""
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-case1-after.png"))
        
        assert applied == 1, "Production should be applied exactly once"
        
        # Check node count
        cnt = self.g.count_nodes()
        assert cnt.normal == 9, f"Should have 9 nodes (8 original + 1 V), got {cnt.normal}"
        
        # Check Q hyperedges
        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 5, f"Should have 5 Q hyperedges, got {len(q_edges)}"
        assert all(e.r == 0 for e in q_edges), "All Q hyperedges should have r=0"
        
        # Check central vertex exists
        v_nodes = [n for n in self.g.nodes if n.label.startswith("V_")]
        assert len(v_nodes) == 1, "Should have exactly one central vertex V"
        v = v_nodes[0]
        assert v.x == 2.0, f"V should be at x=2.0, got {v.x}"
        assert v.y == 2.0, f"V should be at y=2.0, got {v.y}"


class TestP5Case2:
    """Test: Q with R=0 - production should NOT apply."""

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
        
        self.g.add_edge(HyperEdge((n1, n5), "E", r=0))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0))
        
        # Q with R=0 (not marked for refinement)
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0))
        
        self.p5 = P5()

    def test_no_match(self):
        """Production should not apply."""
        draw(self.g, str(DRAW_DIR / "test5-case2.png"))
        
        applied = self.g.apply(self.p5)
        assert applied == 0, "Production should not apply when Q has r=0"


class TestP5Case3:
    """Test: Not all edges broken - production should NOT apply."""

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
        
        # Some E edges with R=1 (not all broken)
        self.g.add_edge(HyperEdge((n1, n5), "E", r=1))
        self.g.add_edge(HyperEdge((n5, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n6), "E", r=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n7), "E", r=0))
        self.g.add_edge(HyperEdge((n7, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n8), "E", r=0))
        self.g.add_edge(HyperEdge((n8, n1), "E", r=0))
        
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))
        
        self.p5 = P5()

    def test_no_match(self):
        """Production should not apply."""
        draw(self.g, str(DRAW_DIR / "test5-case3.png"))
        
        applied = self.g.apply(self.p5)
        assert applied == 0, "Production should not apply when not all E have r=0"


class TestP5Case4:
    """Test: Two separate quadrilaterals, both ready for P5."""

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
        
        self.p5 = P5()

    def test_multiple_applications(self):
        """Production should be applied to both quadrilaterals."""
        draw(self.g, str(DRAW_DIR / "test5-case4-before.png"))
        
        applied = self.g.apply(self.p5)
        
        draw(self.g, str(DRAW_DIR / "test5-case4-after.png"))
        
        assert applied == 2, f"Production should be applied 2 times, got {applied}"
        
        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 10, f"Should have 10 Q hyperedges (5 per quadrilateral), got {len(q_edges)}"
        assert all(e.r == 0 for e in q_edges), "All Q hyperedges should have r=0"
        
        # Check that two central vertices exist
        v_nodes = [n for n in self.g.nodes if n.label.startswith("V_")]
        assert len(v_nodes) == 2, f"Should have 2 central vertices, got {len(v_nodes)}"


class TestP5Case5:
    """Test: Quadrilateral missing a midpoint node."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 0, "n2")
        n3 = Node(4, 4, "n3")
        n4 = Node(0, 4, "n4")
        
        # Only 3 midpoints (missing one)
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
