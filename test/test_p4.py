import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p4 import P4
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


class TestP4Case1:
    """
    Full graph isomporphic. Production applied
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 2, "n2")

        self.g.add_node(n1)
        self.g.add_node(n2)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=1, b=1))

        self.p = P4()

    def test_stage0(self):
        """Test input graph (before applying production)."""
        draw(self.g, str(DRAW_DIR / "test4-case1-stage0.png"))

        cnt = self.g.count_nodes()

        assert cnt.normal == 2, "Should be 2 regular nodes"
        assert cnt.hyper == 1, "Should be 1 hyperedge (E)"
        assert self.g.hyperedges[0].hypertag == "E"
        assert self.g.hyperedges[0].r == 1
        assert self.g.hyperedges[0].b == 1

    def test_stage1(self):
        """Test graph after applying production."""
        applied = self.g.apply(self.p)
        draw(self.g, str(DRAW_DIR / "test4-case1-stage1.png"))

        cnt = self.g.count_nodes()

        assert applied == 1, "Production should be applied 1 time"
        assert cnt.normal == 3, "Should be 3 regular nodes"
        assert cnt.hyper == 2, "Should be 2 hyperedges"
        assert self.g.hyperedges[0].hypertag == "E"
        assert self.g.hyperedges[1].hypertag == "E"
        assert self.g.hyperedges[0].r == 0
        assert self.g.hyperedges[0].b == 1
        assert self.g.hyperedges[1].r == 0
        assert self.g.hyperedges[1].b == 1


class TestP4Case2:
    "Subgraphs isomorphic. Production applied twice to subgraphs with r == 1"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 2, "n2")
        n1_extra = Node(2, 0, "n1_extra")
        n2_extra = Node(2, 2, "n2_extra")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n1_extra)
        self.g.add_node(n2_extra)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=1, b=1))
        self.g.add_edge(HyperEdge((n2, n2_extra), "E", r=1, b=1))
        self.g.add_edge(HyperEdge((n2_extra, n1_extra), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n1_extra, n1), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n1, n2, n2_extra, n1_extra), "Q", r=0, b=0))

        self.p = P4()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test4-case2-stage0.png"))

        cnt = self.g.count_nodes()
        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]

        assert cnt.normal == 4
        assert cnt.hyper == 5
        assert len(e_edges) == 4

    def test_stage1(self):
        applied = self.g.apply(self.p)
        draw(self.g, str(DRAW_DIR / "test4-case2-stage1.png"))

        cnt = self.g.count_nodes()
        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]

        assert cnt.normal == 6, "Should have 6 (2 new) nodes"
        assert cnt.hyper == 7, "Should have 7 (2 new) hypeeredges"
        assert len(e_edges) == 6, "Should have 6 (2 new) E hyperedges"
        assert applied == 2, "Should be applied twice"
        for edge in e_edges:
            assert edge.b == 1, "B parameter should have same value as in left side"
            assert edge.r == 0, "R parameter should be 0 for all E edges"


class TestP4Case3:
    "Graph missing hyperedge. Production not applied"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 2, "n2")

        self.g.add_node(n1)
        self.g.add_node(n2)

        self.p = P4()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test4-case3-stage0.png"))

        cnt = self.g.count_nodes()

        assert cnt.normal == 2
        assert cnt.hyper == 0

    def test_stage1(self):
        applied = self.g.apply(self.p)
        draw(self.g, str(DRAW_DIR / "test4-case3-stage1.png"))

        cnt = self.g.count_nodes()

        assert applied == 0, "Production should not be applied"
        assert cnt.normal == 2
        assert cnt.hyper == 0


class TestP4Case4:
    "Isomorphic graph, but wrong attribute. Hyperedge is Q, when it should be E. Production not applied"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 2, "n2")

        self.g.add_node(n1)
        self.g.add_node(n2)

        self.g.add_edge(HyperEdge((n1, n2), "Q", r=1, b=1))

        self.p = P4()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test4-case4-stage0.png"))

        cnt = self.g.count_nodes()

        assert cnt.normal == 2, "Should be 2 regular nodes"
        assert cnt.hyper == 1, "Should be 1 hyperedge (E)"
        assert self.g.hyperedges[0].hypertag == "Q"
        assert self.g.hyperedges[0].r == 1
        assert self.g.hyperedges[0].b == 1

    def test_stage1(self):
        applied = self.g.apply(self.p)
        draw(self.g, str(DRAW_DIR / "test4-case4-stage1.png"))

        cnt = self.g.count_nodes()

        assert applied == 0, "Production should not be applied"
        assert cnt.normal == 2, "Should be 2 regular nodes"
        assert cnt.hyper == 1, "Should be 1 hyperedge"
        assert self.g.hyperedges[0].hypertag == "Q"
        assert self.g.hyperedges[0].r == 1
        assert self.g.hyperedges[0].b == 1
