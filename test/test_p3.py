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
        
        nodes = self.g.nodes
        assert nodes[2].x == 0
        assert nodes[2].y == 2

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

        assert applied == 0, "Production P3 should be applied exactly 0 times"

        cnt = self.g.count_nodes()
        assert cnt.normal == 2
        assert cnt.hyper == 1

class TestP3Case3:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 4, "n2")

        self.g.add_node(n1)
        self.g.add_node(n2)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=1, b=0))

        n3 = Node(2, 0, "n3")
        n4 = Node(2, 4, "n4")

        self.g.add_node(n3)
        self.g.add_node(n4)

        self.g.add_edge(HyperEdge((n3, n4), "E", r=1, b=0))

        self.p3 = P3()

    def test_stage0(self):
        """Test input graph."""
        draw(self.g, str(DRAW_DIR / "test3-case3-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 4
        assert cnt.hyper == 2

        edges = self.g.hyperedges
        assert len(edges) == 2
        assert edges[0].hypertag == "E"
        assert edges[0].r == 1
        assert edges[0].b == 0

        assert edges[1].hypertag == "E"
        assert edges[1].r == 1
        assert edges[1].b == 0
    
    def test_stage1(self):
        applied = self.g.apply(self.p3)

        draw(self.g, str(DRAW_DIR / "test3-case3-stage1.png"))

        assert applied == 2, "Production P3 should be applied exactly two times"

        cnt = self.g.count_nodes()
        assert cnt.normal == 6
        assert cnt.hyper == 6

        edges = self.g.hyperedges
        for e in edges:
            assert e.hypertag == "E", f"All edges must be E"
            assert e.r == 0, f"All E edges must have r=0"
            assert e.b == 0, f"All edges must have b=0"

class TestP3Case4:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(0, 4, "n2")
        n3 = Node(4, 4, "n3")
        n4 = Node(4, 0, "n4")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n3)
        self.g.add_node(n4)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n2, n3), "E", r=1, b=0))
        self.g.add_edge(HyperEdge((n3, n4), "E", r=1, b=0))
        self.g.add_edge(HyperEdge((n4, n1), "E", r=1, b=1))

        self.p3 = P3()

    def test_stage0(self):
        """Test input graph."""
        draw(self.g, str(DRAW_DIR / "test3-case4-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 4
        assert cnt.hyper == 4

        edges = self.g.hyperedges
        assert len(edges) == 4
        assert edges[0].hypertag == "E"
        assert edges[0].r == 0
        assert edges[0].b == 1

        assert edges[1].hypertag == "E"
        assert edges[1].r == 1
        assert edges[1].b == 0

        assert edges[2].hypertag == "E"
        assert edges[2].r == 1
        assert edges[2].b == 0

        assert edges[3].hypertag == "E"
        assert edges[3].r == 1
        assert edges[3].b == 1
    
    def test_stage1(self):
        applied = self.g.apply(self.p3)

        draw(self.g, str(DRAW_DIR / "test3-case4-stage1.png"))

        assert applied == 2, "Production P3 should be applied exactly two times"

        cnt = self.g.count_nodes()
        assert cnt.normal == 6
        assert cnt.hyper == 8

        for edge in self.g.hyperedges:
            assert not (edge.r == 1 and edge.b == 0), "All r=1,b=0 edges should be consumed by P3"

        for edge in self.g.hyperedges:
            assert edge.hypertag == "E"

        nodes = {node.label: node for node in self.g.nodes}

        assert "n1" in nodes
        assert "n2" in nodes
        assert "n3" in nodes
        assert "n4" in nodes

        new_nodes = [n for n in nodes.values() if n.label not in {"n1", "n2", "n3", "n4"}]
        assert len(new_nodes) == 2

        expected_positions = {
            ((0 + 4) / 2, (4 + 4) / 2),  # środek n2–n3 (2,4)
            ((4 + 4) / 2, (4 + 0) / 2),  # środek n3–n4 (4,2)
        }

        actual_positions = {(n.x, n.y) for n in new_nodes}

        assert actual_positions == expected_positions