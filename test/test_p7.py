import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p7 import P7
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"

@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)

class TestP7Case1:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5")
        ]
        
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        for i, (start, end) in enumerate(edges_indices):
            e = HyperEdge((nodes[start], nodes[end]), "E", r=0)
            self.g.add_edge(e)

        p_edge = HyperEdge(tuple(nodes), "P", r=1)
        self.g.add_edge(p_edge)

        self.p7 = P7()

    def test_stage0(self):
        """Verify initial state."""
        draw(self.g, str(DRAW_DIR / "test7-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 5
        assert cnt.hyper == 6

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1
        assert p_edges[0].r == 1

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.r == 0 for e in e_edges)

    def test_stage1(self):
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case1-stage1.png"))

        assert applied == 1, "Production P7 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 5
        assert cnt.hyper == 6

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 1, "P edge should retain r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 1, f"All E edges must now have r=1. Found r={e.r}"


class TestP7Case2:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5")
        ]
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=0))

        self.p7 = P7()

    def test_no_match(self):
        draw(self.g, str(DRAW_DIR / "test7-case2-stage0.png"))
        
        applied = self.g.apply(self.p7)
        
        assert applied == 0, "Production should NOT be applied when P has r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.r == 0 for e in e_edges), "Edges should remain untouched"
        
    def test_stage1(self):
        """Verify graph after applying P7."""
        applied = self.g.apply(self.p7)

        draw(self.g, str(DRAW_DIR / "test7-case2-stage1.png"))

        assert applied == 0, "Production P7 should not be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 5
        assert cnt.hyper == 6

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 0, "P edge should retain r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 0, f"All E edges must now have r=1. Found r={e.r}"