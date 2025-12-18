import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p3 import P3
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


class TestP3Case1:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 4, "n2")

        self.g.add_node(n1)
        self.g.add_node(n2)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=1, b=0))

        self.p3 = P3()

    def test_stage0(self):
        """Test input graph."""
        draw(self.g, str(DRAW_DIR / "test3-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 2
        assert cnt.hyper == 1

        edges = self.g.hyperedges
        assert len(edges) == 1
        assert edges[0].hypertag == "E"
        assert edges[0].r == 1
        assert edges[0].b == 0
    
    def test_stage1(self):
        applied = self.g.apply(self.p3)

        draw(self.g, str(DRAW_DIR / "test3-case1-stage1.png"))

        assert applied == 1, "Production P3 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 3
        assert cnt.hyper == 3

        edges = self.g.hyperedges
        for e in edges:
            assert e.hypertag == "E", f"All edges must be E"
            assert e.r == 0, f"All E edges must have r=0"
            assert e.b == 0, f"All edges must have b=0"

class TestP3Case2:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 4, "n2")

        self.g.add_node(n1)
        self.g.add_node(n2)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=0, b=0))

        self.p3 = P3()

    def test_stage0(self):
        """Test input graph."""
        draw(self.g, str(DRAW_DIR / "test3-case2-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 2
        assert cnt.hyper == 1

        edges = self.g.hyperedges
        assert len(edges) == 1
        assert edges[0].hypertag == "E"
        assert edges[0].r == 0
        assert edges[0].b == 0
    
    def test_stage1(self):
        applied = self.g.apply(self.p3)

        draw(self.g, str(DRAW_DIR / "test3-case2-stage1.png"))

        assert applied == 0, "Production P3 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 2
        assert cnt.hyper == 1

