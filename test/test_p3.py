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

        self.g.add_edge(HyperEdge((n1, n2), "E", r=1))

        self.p3 = P3()

    def test_stage0(self):
        """Test input graph."""
        draw(self.g, str(DRAW_DIR / "test3-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 2
        assert cnt.hyper == 1

        edges = self.g.hyperedges
        assert edges[0].r == 1
