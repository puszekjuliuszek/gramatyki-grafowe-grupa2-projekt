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
    Test case 1
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

        assert applied == 1, "Production should be applied 1 time"

        cnt = self.g.count_nodes()
        assert cnt.normal == 3, "Should be 3 regular nodes"
        assert cnt.hyper == 2, "Should be 2 hyperedges"

        assert self.g.hyperedges[0].hypertag == "E"
        assert self.g.hyperedges[1].hypertag == "E"
        assert self.g.hyperedges[0].r == 0
        assert self.g.hyperedges[0].b == 1
        assert self.g.hyperedges[1].r == 0
        assert self.g.hyperedges[1].b == 1


# class TestP0Case2:
#     """
#     Test case 2: Square with Q hyperedge already having r=1.
#     Production should NOT be applied.
#     """

#     @pytest.fixture(autouse=True)
#     def setup(self):
#         self.g = Graph()

#         n1 = Node(0, 0, "n1")
#         n2 = Node(2, 0, "n2")
#         n3 = Node(2, 2, "n3")
#         n4 = Node(0, 2, "n4")

#         self.g.add_node(n1)
#         self.g.add_node(n2)
#         self.g.add_node(n3)
#         self.g.add_node(n4)

#         self.g.add_edge(HyperEdge((n1, n2), "E"))
#         self.g.add_edge(HyperEdge((n2, n3), "E"))
#         self.g.add_edge(HyperEdge((n3, n4), "E"))
#         self.g.add_edge(HyperEdge((n4, n1), "E"))

#         self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))

#         self.p0 = P0()

#     def test_no_match(self):
#         """Production should not be applied when Q has r=1."""
#         draw(self.g, str(DRAW_DIR / "test0-case2-stage0.png"))

#         applied = self.g.apply(self.p0)

#         assert applied == 0, "Production should NOT be applied when r=1"

#         q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
#         assert len(q_edges) == 1
#         assert q_edges[0].r == 1


# class TestP0Case3:
#     """
#     Test case 3: Two separate squares, both with r=0.
#     Production should be applied twice.
#     """

#     @pytest.fixture(autouse=True)
#     def setup(self):
#         self.g = Graph()

#         n1 = Node(0, 0, "n1")
#         n2 = Node(2, 0, "n2")
#         n3 = Node(2, 2, "n3")
#         n4 = Node(0, 2, "n4")

#         n5 = Node(5, 0, "n5")
#         n6 = Node(7, 0, "n6")
#         n7 = Node(7, 2, "n7")
#         n8 = Node(5, 2, "n8")

#         self.g.add_node(n1)
#         self.g.add_node(n2)
#         self.g.add_node(n3)
#         self.g.add_node(n4)
#         self.g.add_node(n5)
#         self.g.add_node(n6)
#         self.g.add_node(n7)
#         self.g.add_node(n8)

#         self.g.add_edge(HyperEdge((n1, n2), "E"))
#         self.g.add_edge(HyperEdge((n2, n3), "E"))
#         self.g.add_edge(HyperEdge((n3, n4), "E"))
#         self.g.add_edge(HyperEdge((n4, n1), "E"))
#         self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0))

#         self.g.add_edge(HyperEdge((n5, n6), "E"))
#         self.g.add_edge(HyperEdge((n6, n7), "E"))
#         self.g.add_edge(HyperEdge((n7, n8), "E"))
#         self.g.add_edge(HyperEdge((n8, n5), "E"))
#         self.g.add_edge(HyperEdge((n5, n6, n7, n8), "Q", r=0))

#         self.p0 = P0()

#     def test_multiple_applications(self):
#         """Production should be applied to both squares."""
#         draw(self.g, str(DRAW_DIR / "test0-case3-stage0.png"))

#         applied = self.g.apply(self.p0)

#         draw(self.g, str(DRAW_DIR / "test0-case3-stage1.png"))

#         assert applied == 2, "Production should be applied 2 times"

#         q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
#         assert len(q_edges) == 2
#         assert all(e.r == 1 for e in q_edges), "All Q hyperedges should have r=1"


# class TestHyperEdgeR:
#     """Basic tests for HyperEdge r attribute."""

#     def test_default_r(self):
#         """Test default r value is 0."""
#         n1 = Node(0, 0, "n1")
#         n2 = Node(1, 1, "n2")

#         e = HyperEdge((n1, n2), "E")
#         assert e.r == 0

#     def test_custom_r(self):
#         """Test custom r value."""
#         n1 = Node(0, 0, "n1")
#         n2 = Node(1, 1, "n2")

#         e = HyperEdge((n1, n2), "E", r=1)
#         assert e.r == 1
