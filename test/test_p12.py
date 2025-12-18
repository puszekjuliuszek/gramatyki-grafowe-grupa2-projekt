import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p12 import P12
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


def build_base_p12_graph(T_r: int = 0) -> Graph:
    """
    Base graph matching P12 left side:
    - 7 nodes in cycle with E edges
    - central T connects all nodes
    """
    g = Graph()

    n1 = Node(0, 0, "n1")
    n2 = Node(1, 0, "n2")
    n3 = Node(1.5, 0.5, "n3")
    n4 = Node(1, 1, "n4")
    n5 = Node(0.5, 1.25, "n5")
    n6 = Node(0, 1, "n6")
    n7 = Node(-0.5, 0.5, "n7")

    nodes = [n1, n2, n3, n4, n5, n6, n7]
    for n in nodes:
        g.add_node(n)

    # boundary cycle
    for i in range(len(nodes)):
        g.add_edge(HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), "E", r=0))

    # central T includes all nodes
    g.add_edge(HyperEdge((n1, n2, n3, n4, n5, n6, n7), "T", r=T_r))

    return g


class TestP12Case1:
    "Isomorphic with left side"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = build_base_p12_graph(T_r=0)
        self.p12 = P12()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test12-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 7
        assert cnt.hyper == 8  # 7xE + 1xT

        t_edges = [e for e in self.g.hyperedges if e.hypertag == "T"]
        assert len(t_edges) == 1
        assert t_edges[0].r == 0

    def test_stage1(self):
        applied = self.g.apply(self.p12)
        draw(self.g, str(DRAW_DIR / "test12-case1-stage1.png"))

        assert applied == 1

        # counts should remain the same (replace hyperedges, not add new nodes)
        cnt = self.g.count_nodes()
        assert cnt.normal == 7
        assert cnt.hyper == 8

        # T should be set to r=1
        t_edges = [e for e in self.g.hyperedges if e.hypertag == "T"]
        assert len(t_edges) == 1
        assert t_edges[0].r == 1

        # boundary E edges unchanged
        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert len(e_edges) == 7
        assert all(e.r == 0 for e in e_edges)


class TestP12Case2:
    "Contains subgraph isomorphic with left side"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = build_base_p12_graph(T_r=0)

        extra1 = Node(-1.5, 0.2, "extra1")
        extra2 = Node(-1.8, 0.8, "extra2")
        self.g.add_node(extra1)
        self.g.add_node(extra2)

        # some extra structure
        self.g.add_edge(HyperEdge((extra1, extra2), "E", r=0))
        self.g.add_edge(HyperEdge((extra1, self.g.get_node("n1")), "E", r=0))
        self.g.add_edge(HyperEdge((extra2, self.g.get_node("n6")), "E", r=0))

        self.p12 = P12()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test12-case2-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 9   # 7 + 2 extra
        assert cnt.hyper == 11   # 8 base + 3 extra

    def test_stage1(self):
        applied = self.g.apply(self.p12)
        draw(self.g, str(DRAW_DIR / "test12-case2-stage1.png"))

        assert applied == 1

        cnt = self.g.count_nodes()
        assert cnt.normal == 9
        assert cnt.hyper == 11

        t_edges = [e for e in self.g.hyperedges if e.hypertag == "T"]
        assert len(t_edges) == 1
        assert t_edges[0].r == 1


class TestP12Case3:
    "Isomorphic left side, missing one vertex"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()


        n1 = Node(0, 0, "n1")
        n2 = Node(1, 0, "n2")
        n3 = Node(1.5, 0.5, "n3")
        n4 = Node(1, 1, "n4")
        n5 = Node(0.5, 1.25, "n5")
        n6 = Node(0, 1, "n6")
        # n7 missing

        nodes = [n1, n2, n3, n4, n5, n6]
        for n in nodes:
            self.g.add_node(n)

        for i in range(len(nodes)):
            self.g.add_edge(HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), "E", r=0))

        self.g.add_edge(HyperEdge((n1, n2, n3, n4, n5, n6), "T", r=0))
        self.p12 = P12()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test12-case3-stage0.png"))

    def test_stage1(self):
        applied = self.g.apply(self.p12)
        draw(self.g, str(DRAW_DIR / "test12-case3-stage1.png"))

        assert applied == 0


class TestP12Case4:
    "Isomorphic left side, missing one edge"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = build_base_p12_graph(T_r=0)

        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(1, 0, "n2")
        n3 = Node(1.5, 0.5, "n3")
        n4 = Node(1, 1, "n4")
        n5 = Node(0.5, 1.25, "n5")
        n6 = Node(0, 1, "n6")
        n7 = Node(-0.5, 0.5, "n7")

        nodes = [n1, n2, n3, n4, n5, n6, n7]
        for n in nodes:
            self.g.add_node(n)

        for i in range(len(nodes)):
            if i == 2:
                continue  # missing edge
            self.g.add_edge(HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), "E", r=0))

        self.g.add_edge(HyperEdge((n1, n2, n3, n4, n5, n6, n7), "T", r=0))
        self.p12 = P12()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test12-case4-stage0.png"))

    def test_stage1(self):
        applied = self.g.apply(self.p12)
        draw(self.g, str(DRAW_DIR / "test12-case4-stage1.png"))

        assert applied == 0


class TestP12Case5_1:
    "Isomorphic left side, wrong attribute - one hyperedge is Q, when it should be E (so it has wrong tag)"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(1, 0, "n2")
        n3 = Node(1.5, 0.5, "n3")
        n4 = Node(1, 1, "n4")
        n5 = Node(0.5, 1.25, "n5")
        n6 = Node(0, 1, "n6")
        n7 = Node(-0.5, 0.5, "n7")

        nodes = [n1, n2, n3, n4, n5, n6, n7]
        for n in nodes:
            self.g.add_node(n)

        # first edge has wrong tag
        for i in range(len(nodes)):
            tag = "Q" if i == 0 else "E"
            self.g.add_edge(HyperEdge((nodes[i], nodes[(i + 1) % len(nodes)]), tag, r=0))

        self.g.add_edge(HyperEdge((n1, n2, n3, n4, n5, n6, n7), "T", r=0))
        self.p12 = P12()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test12-case5_1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 7
        assert cnt.hyper == 8

    def test_stage1(self):
        applied = self.g.apply(self.p12)
        
        draw(self.g, str(DRAW_DIR / "test12-case5_1-stage1.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 7
        assert cnt.hyper == 8
        assert applied == 0

class TestP12Case5_2:
    "Isomorphic left side, wrong label - hyperedge T has r==1, when T should have r==0"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = build_base_p12_graph(T_r=1)  
        self.p12 = P12()

    def test_stage0(self):
        draw(self.g, str(DRAW_DIR / "test12-case5_2-stage0.png"))

        t_edges = [e for e in self.g.hyperedges if e.hypertag == "T"]
        assert len(t_edges) == 1
        assert t_edges[0].r == 1
        cnt = self.g.count_nodes()
        assert cnt.normal == 7
        assert cnt.hyper == 8

    def test_stage1(self):
        applied = self.g.apply(self.p12)
        draw(self.g, str(DRAW_DIR / "test12-case5_2-stage1.png"))
        cnt = self.g.count_nodes()
        assert cnt.normal == 7
        assert cnt.hyper == 8
        assert applied == 0
