import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p8 import P8
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


class TestP8Case1:
    """
    Test case 1
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
            Node(0, 0, "n1"),
            Node(1, 0, "n2"),
            Node(1, 1, "n3"),
            Node(0, 1, "n4"),
            Node(1.5, 0.5, "n5"),
            Node(0.5, 0, "n6"),
            Node(0, 0.5, "n7"),
            Node(0.5, 1, "n8"),
            Node(1.25, 0.75, "n9"),
            Node(1.25, 0.25, "n10")
        ] 

        for node in nodes:
            self.g.add_node(node)

        self.g.add_edge(HyperEdge((nodes[0], nodes[5]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[5], nodes[1]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[1], nodes[9]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[9], nodes[4]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[4], nodes[8]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[8], nodes[2]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[2], nodes[7]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[7], nodes[3]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[3], nodes[6]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[6], nodes[0]), "E", b=1))
        self.g.add_edge(HyperEdge((nodes[0], nodes[1], nodes[2], nodes[3], nodes[4]), "P", r=1, b=0))

        self.p = P8()

    def test_stage0(self):
        """Test input graph (before applying production)."""
        draw(self.g, str(DRAW_DIR / "test8-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 10, "Should be 2 regular nodes"
        assert cnt.hyper == 11, "Should be 11 hyperedge (10E + 1P)"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1
        assert p_edges[0].r == 1

    def test_stage1(self):
        """Test graph after applying production."""
        applied = self.g.apply(self.p)

        draw(self.g, str(DRAW_DIR / "test8-case1-stage1.png"))

        assert applied == 1, "Production should be applied 1 time"

        cnt = self.g.count_nodes()
        assert cnt.normal == 11, "Should be 11 regular nodes"
        assert cnt.hyper == 20, "Should be 20 hyperedges"

        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 5
        for i in range(5):
            assert q_edges[i].r == 0
