import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions import p6, p0, p7, p4, p4, p3, p3, p2, p8, p1, p5
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


class TestW5:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
            Node(1, 0, "n1"),
            Node(9, 0, "n2"),
            Node(12, 3, "n3"),
            Node(9, 6, "n4"),
            Node(1, 6, "n5"),
            Node(0, 4, "n6"),
            Node(0, 2, "n7"),
            Node(2, 2, "n8"),
            Node(6, 2, "n9"),
            Node(6, 4, "n10"),
            Node(2, 4, "n11")
        ] 

        for node in nodes:
            self.g.add_node(node)

        for i in range(7):
            self.g.add_edge(HyperEdge((nodes[i], nodes[(i+1)%7]), "E", r=0, b=1))

        for i in range(4):
            self.g.add_edge(HyperEdge((nodes[7+i], nodes[7+(i+1)%4]), "E", r=0, b=0))

        for i in [0, 1]:
            self.g.add_edge(HyperEdge((nodes[i], nodes[i+7]), "E", r=0, b=0))

        for i in [3, 4]:
            self.g.add_edge(HyperEdge((nodes[i], nodes[i+6]), "E", r=0, b=0))

        self.g.add_edge(HyperEdge((nodes[0], nodes[7], nodes[10], nodes[4], nodes[5], nodes[6]), "S", r=0, b=0))
        self.g.add_edge(HyperEdge((nodes[0], nodes[1], nodes[8], nodes[7]), "Q", r=0, b=0))
        self.g.add_edge(HyperEdge((nodes[10], nodes[9], nodes[3], nodes[4]), "Q", r=0, b=0))
        self.g.add_edge(HyperEdge((nodes[7], nodes[8], nodes[9], nodes[10]), "Q", r=0, b=0))
        self.g.add_edge(HyperEdge((nodes[1], nodes[2], nodes[3], nodes[8], nodes[9]), "P", r=0, b=0))

    def test(self):
        draw(self.g, str(DRAW_DIR / "test_w5-stage0.png"))

        p6.P6().apply(self.g)
        draw(self.g, str(DRAW_DIR / "test_w5-stage1.png"))

        self.g.apply_one(p0.P0(), "n4")
        draw(self.g, str(DRAW_DIR / "test_w5-stage2.png"))

        self.g.apply(p7.P7())
        draw(self.g, str(DRAW_DIR / "test_w5-stage3.png"))

        self.g.apply(p4.P4())
        draw(self.g, str(DRAW_DIR / "test_w5-stage4.png"))

        self.g.apply(p3.P3())
        draw(self.g, str(DRAW_DIR / "test_w5-stage5.png"))

        self.g.apply(p8.P8())
        draw(self.g, str(DRAW_DIR / "test_w5-stage6.png"))

        self.g.apply(p1.P1())
        draw(self.g, str(DRAW_DIR / "test_w5-stage7.png"))

        self.g.apply(p4.P4())
        draw(self.g, str(DRAW_DIR / "test_w5-stage8.png"))

        p2.P2().apply(self.g)
        draw(self.g, str(DRAW_DIR / "test_w5-stage9.png"))

        self.g.apply(p3.P3())
        draw(self.g, str(DRAW_DIR / "test_w5-stage10.png"))

        self.g.apply(p5.P5())
        draw(self.g, str(DRAW_DIR / "test_w5-stage11.png"))

        self.g.apply_one(p0.P0(), "n4")
        self.g.apply_one(p0.P0(), "n4")
        draw(self.g, str(DRAW_DIR / "test_w5-stage12.png"))

        self.g.apply_one(p1.P1(), "n4")
        draw(self.g, str(DRAW_DIR / "test_w5-stage13.png"))

        self.g.apply(p4.P4())
        draw(self.g, str(DRAW_DIR / "test_w5-stage14.png"))

        self.g.apply(p3.P3())
        draw(self.g, str(DRAW_DIR / "test_w5-stage15.png"))

        self.g.apply(p5.P5())
        draw(self.g, str(DRAW_DIR / "test_w5-stage16.png"))

        self.g.apply(p1.P1())
        draw(self.g, str(DRAW_DIR / "test_w5-stage17.png"))

        self.g.apply(p4.P4())
        draw(self.g, str(DRAW_DIR / "test_w5-stage18.png"))

        p2.P2().apply(self.g)
        draw(self.g, str(DRAW_DIR / "test_w5-stage19.png"))

        self.g.apply(p3.P3())
        draw(self.g, str(DRAW_DIR / "test_w5-stage20.png"))

        self.g.apply(p5.P5())
        draw(self.g, str(DRAW_DIR / "test_w5-stage21.png"))