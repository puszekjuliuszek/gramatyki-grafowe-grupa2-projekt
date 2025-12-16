import pytest
from pathlib import Path

from src.node import Node
from src.edge import HyperEdge
from src.graph import Graph
from src.productions.p9 import P9
from src.visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


class TestP9Case1:
    """
    Test case 1: Single hexagonal element with S hyperedge (r=0).
    
    Input: 6 outer nodes + S hyperedge (r=0).
    Expected: Same structure, S has r=1.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(1, 0, "n1")
        n2 = Node(0.5, 0.866, "n2")
        n3 = Node(-0.5, 0.866, "n3")
        n4 = Node(-1, 0, "n4")
        n5 = Node(-0.5, -0.866, "n5")
        n6 = Node(0.5, -0.866, "n6")

        nodes = [n1, n2, n3, n4, n5, n6]
        for n in nodes:
            self.g.add_node(n)

        boundary = [n1, n2, n3, n4, n5, n6]
        for i in range(len(boundary)):
            curr_n = boundary[i]
            next_n = boundary[(i + 1) % len(boundary)]
            self.g.add_edge(HyperEdge((curr_n, next_n), "E"))

        self.g.add_edge(HyperEdge(tuple(nodes), "S", r=0))

        self.p9 = P9()

    def test_stage0(self):
        """Test input graph state."""
        draw(self.g, str(DRAW_DIR / "test9-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 6, "Should be 6 nodes"
        assert cnt.hyper == 7, "Should be 7 hyperedges (6 E + 1 S)"

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "S"]
        assert len(s_edges) == 1
        assert s_edges[0].r == 0

    def test_stage1(self):
        """Test application of P9."""
        applied = self.g.apply(self.p9)

        draw(self.g, str(DRAW_DIR / "test9-case1-stage1.png"))

        assert applied == 1, "Should apply exactly once"

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "S"]
        assert len(s_edges) == 1
        assert s_edges[0].r == 1, "S hyperedge should have r=1"


class TestP9Case2:
    """
    Test case 2: Hexagon with S hyperedge already having r=1.
    Production should NOT be applied.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(1, 0, "n1")
        n2 = Node(0.5, 0.866, "n2")
        n3 = Node(-0.5, 0.866, "n3")
        n4 = Node(-1, 0, "n4")
        n5 = Node(-0.5, -0.866, "n5")
        n6 = Node(0.5, -0.866, "n6")

        nodes = [n1, n2, n3, n4, n5, n6]
        for n in nodes:
            self.g.add_node(n)

        boundary = [n1, n2, n3, n4, n5, n6]
        for i in range(len(boundary)):
            curr_n = boundary[i]
            next_n = boundary[(i + 1) % len(boundary)]
            self.g.add_edge(HyperEdge((curr_n, next_n), "E"))

        self.g.add_edge(HyperEdge(tuple(nodes), "S", r=1))

        self.p9 = P9()

    def test_no_match(self):
        """Production should not apply if r=1."""
        draw(self.g, str(DRAW_DIR / "test9-case2-stage0.png"))

        applied = self.g.apply(self.p9)

        assert applied == 0, "Should NOT apply when r=1"

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "S"]
        assert len(s_edges) == 1
        assert s_edges[0].r == 1


class TestP9Case3:
    """
    Test case 3: Two separate hexagons, both with r=0.
    Production should be applied twice.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        h1_nodes = [
            Node(0.5, -0.866, "n1"), Node(1, 0, "n2"), Node(0.5, 0.866, "n3"),
            Node(-0.5, 0.866, "n4"), Node(-1, 0, "n5"), Node(-0.5, -0.866, "n6")
        ]
        for n in h1_nodes:
            self.g.add_node(n)
            
        for i in range(6):
            self.g.add_edge(HyperEdge((h1_nodes[i], h1_nodes[(i+1)%6]), "E"))
        self.g.add_edge(HyperEdge(tuple(h1_nodes), "S", r=0))

        h2_nodes = [
            Node(5.5, -0.866, "n7"), Node(6, 0, "n8"), Node(5.5, 0.866, "n9"),
            Node(4.5, 0.866, "n10"), Node(4, 0, "n11"), Node(4.5, -0.866, "n12")
        ]
        for n in h2_nodes:
            self.g.add_node(n)
            
        for i in range(6):
            self.g.add_edge(HyperEdge((h2_nodes[i], h2_nodes[(i+1)%6]), "E"))
        self.g.add_edge(HyperEdge(tuple(h2_nodes), "S", r=0))

        self.p9 = P9()

    def test_multiple_applications(self):
        """Should apply to both hexagons."""
        draw(self.g, str(DRAW_DIR / "test9-case3-stage0.png"))

        applied = self.g.apply(self.p9)

        draw(self.g, str(DRAW_DIR / "test9-case3-stage1.png"))

        assert applied == 2, "Should apply 2 times"

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "S"]
        assert len(s_edges) == 2
        assert all(e.r == 1 for e in s_edges)