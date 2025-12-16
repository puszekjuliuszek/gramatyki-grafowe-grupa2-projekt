import pytest
from pathlib import Path

from src.node import Node
from src.edge import HyperEdge
from src.graph import Graph
from src.productions.p9 import P9
from src.visualization import draw

# Define path for saving visualization images
DRAW_DIR = Path(__file__).parent.parent / "draw"

@pytest.fixture(autouse=True)
def ensure_draw_dir():
    """Ensures the draw directory exists before running tests."""
    DRAW_DIR.mkdir(exist_ok=True)


class TestP9Case1:
    """
    Test case 1: Single hexagonal element with Q hyperedge (r=0).

    Input:
        Hexagonal mesh element with a central node and Q hyperedge (r=0).

    Expected output:
        Same structure but Q hyperedge has r=1.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        # Center node
        n0 = Node(0, 0, "n0")
        
        # Boundary nodes (counter-clockwise)
        n1 = Node(1, 0, "n1")
        n2 = Node(0.5, 0.866, "n2")
        n3 = Node(-0.5, 0.866, "n3")
        n4 = Node(-1, 0, "n4")
        n5 = Node(-0.5, -0.866, "n5")
        n6 = Node(0.5, -0.866, "n6")

        nodes = [n0, n1, n2, n3, n4, n5, n6]
        for n in nodes:
            self.g.add_node(n)

        # Boundary edges
        boundary = [n1, n2, n3, n4, n5, n6]
        for i in range(len(boundary)):
            curr_n = boundary[i]
            next_n = boundary[(i + 1) % len(boundary)]
            self.g.add_edge(HyperEdge((curr_n, next_n), "E"))

        # Central S hyperedge connecting all nodes with r=0
        self.g.add_edge(HyperEdge(tuple(nodes), "Q", r=0))

        self.p9 = P9()

    def test_stage0(self):
        """Test input graph (before applying production)."""
        draw(self.g, str(DRAW_DIR / "test9-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 7, "Should be 7 regular nodes (1 center + 6 boundary)"
        assert cnt.hyper == 7, "Should be 7 hyperedges (6 E + 1 Q)"

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(s_edges) == 1
        assert s_edges[0].r == 0

    def test_stage1(self):
        """Test graph after applying production P9."""
        applied = self.g.apply(self.p9)

        draw(self.g, str(DRAW_DIR / "test9-case1-stage1.png"))

        assert applied == 1, "Production should be applied 1 time"

        cnt = self.g.count_nodes()
        assert cnt.normal == 7, "Structure should remain unchanged"
        assert cnt.hyper == 7

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(s_edges) == 1
        assert s_edges[0].r == 1, "Q hyperedge should have r=1 after production"


class TestP9Case2:
    """
    Test case 2: Hexagonal element with Q hyperedge already having r=1.
    Production should NOT be applied.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        # Center node
        n0 = Node(0, 0, "n0")
        # Boundary nodes
        n1 = Node(1, 0, "n1")
        n2 = Node(0.5, 0.866, "n2")
        n3 = Node(-0.5, 0.866, "n3")
        n4 = Node(-1, 0, "n4")
        n5 = Node(-0.5, -0.866, "n5")
        n6 = Node(0.5, -0.866, "n6")

        nodes = [n0, n1, n2, n3, n4, n5, n6]
        for n in nodes:
            self.g.add_node(n)

        # Boundary edges
        boundary = [n1, n2, n3, n4, n5, n6]
        for i in range(len(boundary)):
            curr_n = boundary[i]
            next_n = boundary[(i + 1) % len(boundary)]
            self.g.add_edge(HyperEdge((curr_n, next_n), "E"))

        # Central Q hyperedge ALREADY set to r=1
        self.g.add_edge(HyperEdge(tuple(nodes), "Q", r=1))

        self.p9 = P9()

    def test_no_match(self):
        """Production should not be applied when Q has r=1."""
        draw(self.g, str(DRAW_DIR / "test9-case2-stage0.png"))

        applied = self.g.apply(self.p9)

        assert applied == 0, "Production should NOT be applied when r=1"

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(s_edges) == 1
        assert s_edges[0].r == 1


class TestP9Case3:
    """
    Test case 3: Two separate hexagonal elements, both with r=0.
    Production should be applied twice.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        # --- Hexagon 1 ---
        h1_nodes = [
            Node(0, 0, "n0"), Node(1, 0, "n1"), Node(0.5, 0.866, "n2"),
            Node(-0.5, 0.866, "n3"), Node(-1, 0, "n4"), Node(-0.5, -0.866, "n5"), Node(0.5, -0.866, "n6")
        ]
        for n in h1_nodes:
            self.g.add_node(n)
            
        boundary_1 = h1_nodes[1:]
        for i in range(len(boundary_1)):
            self.g.add_edge(HyperEdge((boundary_1[i], boundary_1[(i+1)%6]), "E"))
        self.g.add_edge(HyperEdge(tuple(h1_nodes), "Q", r=0))

        # --- Hexagon 2 (Shifted by x=5) ---
        h2_nodes = [
            Node(5, 0, "n7"), Node(6, 0, "n8"), Node(5.5, 0.866, "n9"),
            Node(4.5, 0.866, "n10"), Node(4, 0, "n11"), Node(4.5, -0.866, "n12"),
            Node(5.5, -0.866, "n13")
        ]
        for n in h2_nodes:
            self.g.add_node(n)
            
        boundary_2 = h2_nodes[1:]
        for i in range(len(boundary_2)):
            self.g.add_edge(HyperEdge((boundary_2[i], boundary_2[(i+1)%6]), "E"))
        self.g.add_edge(HyperEdge(tuple(h2_nodes), "Q", r=0))

        self.p9 = P9()

    def test_multiple_applications(self):
        """Production should be applied to both hexagonal elements."""
        draw(self.g, str(DRAW_DIR / "test9-case3-stage0.png"))

        applied = self.g.apply(self.p9)

        draw(self.g, str(DRAW_DIR / "test9-case3-stage1.png"))

        assert applied == 2, "Production should be applied 2 times"

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(s_edges) == 2
        assert all(e.r == 1 for e in s_edges), "All Q hyperedges should have r=1"