import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p8 import P8
from src.productions.p0 import P0
from src.productions.p1 import P1
from src.productions.p4 import P4
from src.productions.p5 import P5
from src.productions.p6 import P6
from src.productions.p7 import P7
from src.productions.p8 import P8
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


class TestCase1:
    """
    Test case 1
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
            Node(1, 4, "n1"),
            Node(5, 4, "n2"),
            Node(0, 3, "n3"),
            Node(2, 3, "n4"),
            Node(4, 3, "n5"),
            Node(6, 2, "n6"),
            Node(0, 1, "n7"),
            Node(2, 1, "n8"),
            Node(4, 1, "n9"),
            Node(1, 0, "n10"),
            Node(5, 0, "n11")
        ] 

        for node in nodes:
            self.g.add_node(node)

        self.g.add_edge(HyperEdge((nodes[0], nodes[1]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[0], nodes[2]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[0], nodes[3]), "E", r=0, b=1))

        self.g.add_edge(HyperEdge((nodes[1], nodes[5]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[1], nodes[5]), "E", r=0, b=1))

        self.g.add_edge(HyperEdge((nodes[1], nodes[4]), "E", r=0, b=1))

        self.g.add_edge(HyperEdge((nodes[3], nodes[7]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[3], nodes[4]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[6], nodes[2]), "E", r=0, b=1))

        self.g.add_edge(HyperEdge((nodes[6], nodes[9]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[9], nodes[10]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[9], nodes[7]), "E", r=0, b=1))

        self.g.add_edge(HyperEdge((nodes[10], nodes[5]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[10], nodes[8]), "E", r=0, b=1))

        self.g.add_edge(HyperEdge((nodes[7], nodes[8]), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((nodes[8], nodes[4]), "E", r=0, b=1))


        self.g.add_edge(HyperEdge((nodes[0], nodes[1], nodes[3], nodes[4]), "Q", r=0, b=0))
        self.g.add_edge(HyperEdge((nodes[7], nodes[8], nodes[3], nodes[4]), "Q", r=0, b=0))
        self.g.add_edge(HyperEdge((nodes[7], nodes[8], nodes[9], nodes[10]), "Q", r=0, b=0))
        self.g.add_edge(HyperEdge((nodes[1], nodes[4], nodes[8], nodes[10], nodes[5]), "P", r=0, b=0))
        self.g.add_edge(HyperEdge((nodes[0], nodes[2], nodes[6], nodes[9], nodes[7], nodes[3]), "P", r=0, b=0))
    
    
    def test_full_sequence(self):
        """Test full sequence of productions."""
        draw(self.g, str(DRAW_DIR / "gr6-stage0.png"))

        p6 = P6()
        result = p6.apply(self.g)
        draw(self.g, str(DRAW_DIR / "gr6-stage1.png"))

        p0 = P0()
        result = self.g.apply(p0)
        draw(self.g, str(DRAW_DIR / "gr6-stage2.png"))

        p7 = P7()
        self.g.apply(p7)
        draw(self.g, str(DRAW_DIR / "gr6-stage3.png"))

        p1 = P1()
        self.g.apply(p1)
        draw(self.g, str(DRAW_DIR / "gr6-stage4.png"))

        p4 = P4()
        self.g.apply(p4)
        draw(self.g, str(DRAW_DIR / "gr6-stage5.png"))
        
        p8 = P8()
        self.g.apply(p8)
        draw(self.g, str(DRAW_DIR / "gr6-stage6.png"))

        p5 = P5()
        self.g.apply(p5)
        draw(self.g, str(DRAW_DIR / "gr6-stage7.png"))

        p0 = P0()
        result = self.g.apply(p0)
        draw(self.g, str(DRAW_DIR / "gr6-stage8.png"))

        p1 = P1()
        self.g.apply(p1)
        draw(self.g, str(DRAW_DIR / "gr6-stage9.png"))

        p4 = P4()
        self.g.apply(p4)
        draw(self.g, str(DRAW_DIR / "gr6-stage10.png"))

        p5 = P5()
        self.g.apply(p5)
        draw(self.g, str(DRAW_DIR / "gr6-stage11.png"))
