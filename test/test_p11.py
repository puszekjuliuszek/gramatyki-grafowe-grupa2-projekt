import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p11 import P11
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)

class TestP11Case1:
    "Isomorphic with left side"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1  = Node(0, 1, "n1")
        n8  = Node(0.5, 1.5, "n8")
        n6  = Node(1, 2, "n6")
        n9  = Node(1.5, 1.5, "n9")
        n4  = Node(2, 1, "n4")
        n10 = Node(2, 0.5, "n10")
        n3  = Node(2, 0, "n3")
        n11 = Node(1.5, -0.5, "n11")
        n5  = Node(1, -1, "n5")
        n12 = Node(0.5, -0.5, "n12")
        n2  = Node(0, 0, "n2")
        n7  = Node(0, 0.5, "n7")

        nodes = [n1, n8, n6, n9, n4, n10, n3, n11, n5, n12, n2, n7]

        for n in nodes:
            self.g.add_node(n)


        for i in range(len(nodes)):
            self.g.add_edge(HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), "E", r=0))

        self.g.add_edge(HyperEdge((n1, n6, n4, n3, n5, n2), "S", r=1))

        self.p11 = P11()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test11-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 12
        assert cnt.hyper == 13

    def test_stage1(self):
        applied = self.g.apply(self.p11)

        draw(self.g, str(DRAW_DIR / "test11-case1-stage1.png"))

        assert applied == 1

        cnt = self.g.count_nodes()
        assert cnt.normal == 13
        assert cnt.hyper == 24

        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 6
        assert all(e.r == 0 for e in q_edges)

class TestP11Case2:
    "Contains subgraph isomorphic with left side"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1  = Node(0, 1, "n1")
        n8  = Node(0.5, 1.5, "n8")
        n6  = Node(1, 2, "n6")
        n9  = Node(1.5, 1.5, "n9")
        n4  = Node(2, 1, "n4")
        n10 = Node(2, 0.5, "n10")
        n3  = Node(2, 0, "n3")
        n11 = Node(1.5, -0.5, "n11")
        n5  = Node(1, -1, "n5")
        n12 = Node(0.5, -0.5, "n12")
        n2  = Node(0, 0, "n2")
        n7  = Node(0, 0.5, "n7")

        extra1 = Node(-1, 1, "extra1")
        extra2 = Node(-1, 0, "extra2")

        nodes = [
            n1, n8, n6, n9, n4, n10,
            n3, n11, n5, n12, n2, n7,
            extra1, extra2
        ]

        for n in nodes:
            self.g.add_node(n)

        base_nodes = nodes[:12]

        for i in range(len(base_nodes)):
            self.g.add_edge(
                HyperEdge((base_nodes[i], base_nodes[(i + 1) % len(base_nodes)]), "E", r=0)
            )

        self.g.add_edge(HyperEdge((n1, n6, n4, n3, n5, n2), "S", r=1))

        # extra
        self.g.add_edge(HyperEdge((extra1, n1), "E", r=0))
        self.g.add_edge(HyperEdge((extra2, n2), "E", r=0))
        self.g.add_edge(HyperEdge((extra1, extra2), "E", r=0))
        self.g.add_edge(HyperEdge((n1, n2, extra1, extra2), "Q", r=0))

        self.p11 = P11()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test11-case2-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 14 # 12 + 2 extra
        assert cnt.hyper == 17 # 13 + 4 extra

    def test_stage1(self):
        applied = self.g.apply(self.p11)
        draw(self.g, str(DRAW_DIR / "test11-case2-stage1.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 15 # 13 + 2 extra
        assert cnt.hyper == 28 # 24 + 4 extra
        assert applied == 1

class TestP11Case3:
    "Isomorphic left side, missing one vertex"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1  = Node(0, 1, "n1")
        n8  = Node(0.5, 1.5, "n8")
        n6  = Node(1, 2, "n6")
        n9  = Node(1.5, 1.5, "n9")
        n4  = Node(2, 1, "n4")
        n10 = Node(2, 0.5, "n10")
        n3  = Node(2, 0, "n3")
        n11 = Node(1.5, -0.5, "n11")
        n5  = Node(1, -1, "n5")
        n12 = Node(0.5, -0.5, "n12")
        n2  = Node(0, 0, "n2")
        # n7 missing

        nodes = [n1, n8, n6, n9, n4, n10, n3, n11, n5, n12, n2]

        for n in nodes:
            self.g.add_node(n)

        for i in range(len(nodes)):
            self.g.add_edge(
                HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), "E", r=0)
            )

        self.g.add_edge(HyperEdge((n1, n6, n4, n3, n5, n2), "S", r=1))
        self.p11 = P11()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test11-case3-stage0.png"))

    def test_stage1(self):
        applied = self.g.apply(self.p11)
        draw(self.g, str(DRAW_DIR / "test11-case3-stage1.png"))

        assert applied == 0

class TestP11Case4:
    "Isomorphic left side, missing one edge"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1  = Node(0, 1, "n1")
        n8  = Node(0.5, 1.5, "n8")
        n6  = Node(1, 2, "n6")
        n9  = Node(1.5, 1.5, "n9")
        n4  = Node(2, 1, "n4")
        n10 = Node(2, 0.5, "n10")
        n3  = Node(2, 0, "n3")
        n11 = Node(1.5, -0.5, "n11")
        n5  = Node(1, -1, "n5")
        n12 = Node(0.5, -0.5, "n12")
        n2  = Node(0, 0, "n2")
        n7  = Node(0, 0.5, "n7")

        nodes = [n1, n8, n6, n9, n4, n10, n3, n11, n5, n12, n2, n7]

        for n in nodes:
            self.g.add_node(n)

        for i in range(len(nodes)):
            if i == 5:
                continue  # missing edge
            self.g.add_edge(
                HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), "E", r=0)
            )

        self.g.add_edge(HyperEdge((n1, n6, n4, n3, n5, n2), "S", r=1))
        self.p11 = P11()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test11-case4-stage0.png"))

    def test_stage1(self):
        applied = self.g.apply(self.p11)
        draw(self.g, str(DRAW_DIR / "test11-case4-stage1.png"))

        assert applied == 0

class TestP11Case5_1:
    "Isomorphic left side, wrong attribute - one hyperedge is Q, when it should be E"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1  = Node(0, 1, "n1")
        n8  = Node(0.5, 1.5, "n8")
        n6  = Node(1, 2, "n6")
        n9  = Node(1.5, 1.5, "n9")
        n4  = Node(2, 1, "n4")
        n10 = Node(2, 0.5, "n10")
        n3  = Node(2, 0, "n3")
        n11 = Node(1.5, -0.5, "n11")
        n5  = Node(1, -1, "n5")
        n12 = Node(0.5, -0.5, "n12")
        n2  = Node(0, 0, "n2")
        n7  = Node(0, 0.5, "n7")

        nodes = [n1, n8, n6, n9, n4, n10, n3, n11, n5, n12, n2, n7]

        for n in nodes:
            self.g.add_node(n)

        for i in range(len(nodes)):
            label = "Q" if i == 0 else "E"
            self.g.add_edge(
                HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), label, r=0)
            )

        self.g.add_edge(HyperEdge((n1, n6, n4, n3, n5, n2), "S", r=1))

        self.p11 = P11()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test11-case5_1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 12
        assert cnt.hyper == 13

    def test_stage1(self):
        applied = self.g.apply(self.p11)

        draw(self.g, str(DRAW_DIR / "test11-case5_1-stage1.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 12
        assert cnt.hyper == 13


class TestP11Case5_2:
    "Isomorphic left side, wrong label - hyperedge S has r==1, when S should have r==0"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1  = Node(0, 1, "n1")
        n8  = Node(0.5, 1.5, "n8")
        n6  = Node(1, 2, "n6")
        n9  = Node(1.5, 1.5, "n9")
        n4  = Node(2, 1, "n4")
        n10 = Node(2, 0.5, "n10")
        n3  = Node(2, 0, "n3")
        n11 = Node(1.5, -0.5, "n11")
        n5  = Node(1, -1, "n5")
        n12 = Node(0.5, -0.5, "n12")
        n2  = Node(0, 0, "n2")
        n7  = Node(0, 0.5, "n7")

        nodes = [n1, n8, n6, n9, n4, n10, n3, n11, n5, n12, n2, n7]

        for n in nodes:
            self.g.add_node(n)

        for i in range(len(nodes)):
            self.g.add_edge(
                HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), "E", r=0)
            )

        self.g.add_edge(HyperEdge((n1, n6, n4, n3, n5, n2), "S", r=0))

        self.p11 = P11()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test11-case5_2-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 12
        assert cnt.hyper == 13

    def test_stage1(self):
        applied = self.g.apply(self.p11)

        draw(self.g, str(DRAW_DIR / "test11-case5_2-stage1.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 12
        assert cnt.hyper == 13