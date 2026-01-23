import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p1 import P1
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)


class TestP1Case1:
    """
    Test case 1: Simple square with Q hyperedge (r=0) and E edges (r=0).
    
    Input:
        n1 (0,0) ---E(r=0)--- n2 (2,0)
        |                     |
        E(r=0)      Q(r=0)    E(r=0)
        |                     |
        n4 (0,2) ---E(r=0)--- n3 (2,2)

    Expected output:
        Same structure but all E edges have r=1. Q remains r=0.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n3)
        self.g.add_node(n4)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n1), "E", r=0))

        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0))

    def test_production_application(self):
        draw(self.g, DRAW_DIR / "p1_case1_before.png")
        
        p1 = P1()
        assert self.g.apply(p1) == 1
        
        draw(self.g, DRAW_DIR / "p1_case1_after.png")

        # Check if all E edges have r=1
        for edge in self.g.hyperedges:
            if edge.hypertag == "E":
                assert edge.r == 1
            if edge.hypertag == "Q":
                assert edge.r == 0 # Should remain 0

        # Applying again should return 0
        assert self.g.apply(p1) == 0

# class TestP1Case2:
#     """
#     Test case 2: Square where Q has r=1 and some E edges have r=1.
    
#     Input:
#         n1 ---E(r=1)--- n2
#         |               |
#         E(r=0)  Q(r=1)  E(r=1)
#         |               |
#         n4 ---E(r=0)--- n3

#     Expected output:
#         All E edges become r=1. Q remains r=1.
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

#         self.g.add_edge(HyperEdge((n1, n2), "E", r=1))
#         self.g.add_edge(HyperEdge((n2, n3), "E", r=1))
#         self.g.add_edge(HyperEdge((n3, n4), "E", r=0))
#         self.g.add_edge(HyperEdge((n4, n1), "E", r=0))

#         self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=1))

#     def test_production_application(self):
#         draw(self.g, DRAW_DIR / "p1_case2_before.png")
        
#         p1 = P1()
#         assert self.g.apply(p1) == 1
        
#         draw(self.g, DRAW_DIR / "p1_case2_after.png")

#         for edge in self.g.hyperedges:
#             if edge.hypertag == "E":
#                 assert edge.r == 1
#             if edge.hypertag == "Q":
#                 assert edge.r == 1

#         assert self.g.apply(p1) == 0

class TestP1Case3:
    """
    Test case 3: Two separate squares.
    Square 1: All E edges r=0.
    Square 2: All E edges r=0.
    
    Expected output:
        Production applied twice. All E edges become r=1.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        # Square 1
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n3)
        self.g.add_node(n4)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n1), "E", r=0))
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0))

        # Square 2
        n5 = Node(5, 0, "n5")
        n6 = Node(7, 0, "n6")
        n7 = Node(7, 2, "n7")
        n8 = Node(5, 2, "n8")

        self.g.add_node(n5)
        self.g.add_node(n6)
        self.g.add_node(n7)
        self.g.add_node(n8)

        self.g.add_edge(HyperEdge((n5, n6), "E", r=0))
        self.g.add_edge(HyperEdge((n6, n7), "E", r=0))
        self.g.add_edge(HyperEdge((n7, n8), "E", r=0))
        self.g.add_edge(HyperEdge((n8, n5), "E", r=0))
        self.g.add_edge(HyperEdge((n5, n6, n7, n8), "Q", r=0))

    def test_production_application(self):
        draw(self.g, DRAW_DIR / "p1_case3_before.png")
        
        p1 = P1()
        assert self.g.apply(p1) == 2
        
        draw(self.g, DRAW_DIR / "p1_case3_after.png")

        for edge in self.g.hyperedges:
            if edge.hypertag == "E":
                assert edge.r == 1

        assert self.g.apply(p1) == 0

class TestP1Case4:
    """
    Test case 4: Two connected squares.
    Square 1: All E edges r=1 (should not apply).
    Square 2: All E edges r=0 (should apply).
    
    Expected output:
        Production applied once. All E edges become r=1.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        # Square 1 (r=1)
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n3)
        self.g.add_node(n4)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=1))
        self.g.add_edge(HyperEdge((n2, n3), "E", r=1))
        self.g.add_edge(HyperEdge((n3, n4), "E", r=1))
        self.g.add_edge(HyperEdge((n4, n1), "E", r=1))
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0))

        # Square 2 (r=0) - connected to Square 1 via n2, n3
        n5 = Node(4, 0, "n5")
        n6 = Node(4, 2, "n6")

        self.g.add_node(n5)
        self.g.add_node(n6)

        # Edges for Square 2
        # n2-n5, n5-n6, n6-n3, n3-n2 (shared)
        self.g.add_edge(HyperEdge((n2, n5), "E", r=0))
        self.g.add_edge(HyperEdge((n5, n6), "E", r=0))
        self.g.add_edge(HyperEdge((n6, n3), "E", r=0))
        # n2-n3 is shared, it has r=1 from Square 1.
        
        self.g.add_edge(HyperEdge((n2, n5, n6, n3), "Q", r=0))

    def test_production_application(self):
        draw(self.g, DRAW_DIR / "p1_case4_before.png")
        
        p1 = P1()
        
        assert self.g.apply(p1) == 1
        
        draw(self.g, DRAW_DIR / "p1_case4_after.png")

        for edge in self.g.hyperedges:
            if edge.hypertag == "E":
                assert edge.r == 1

        assert self.g.apply(p1) == 0

class TestP1Case5:
    """
    Test case 5: Square where central hyperedge has wrong label ('X' instead of 'Q').
    
    Structure:
        n1 ---E--- n2
        |          |
        E     X    E
        |          |
        n4 ---E--- n3

    Expected output:
        Production should not apply. apply(p1) == 0.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n3)
        self.g.add_node(n4)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=0))
        self.g.add_edge(HyperEdge((n2, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n1), "E", r=0))

        # Wrong hyperedge label 'X'
        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "X", r=0))

    def test_production_application(self):
        draw(self.g, DRAW_DIR / "p1_case5_before.png")

        p1 = P1()
        # Should return 0 because structure matches but tag 'Q' is 'X'
        
        assert self.g.apply(p1) == 0
        
        draw(self.g, DRAW_DIR / "p1_case5_after.png")


class TestP1Case6:
    """
    Test case 6: Square where one of the E edges is missing.
    
    Structure:
        n1 ---E--- n2
        |          |
        E     Q    (missing)
        |          |
        n4 ---E--- n3

    Expected output:
        Production should not apply. apply(p1) == 0.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n3)
        self.g.add_node(n4)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=0))
        # Missing edge n2-n3
        # self.g.add_edge(HyperEdge((n2, n3), "E", r=0))
        self.g.add_edge(HyperEdge((n3, n4), "E", r=0))
        self.g.add_edge(HyperEdge((n4, n1), "E", r=0))

        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0))

    def test_production_application(self):
        draw(self.g, DRAW_DIR / "p1_case6_before.png")

        p1 = P1()
        # Should return 0 because one edge is missing
        
        assert self.g.apply(p1) == 0
        
        draw(self.g, DRAW_DIR / "p1_case6_after.png")


class TestP1Case7:
    """
    Test case 7: Square where all E edges already have r=1.
    
    Structure:
        n1 ---E(r=1)--- n2
        |               |
        E(r=1)  Q(r=0)  E(r=1)
        |               |
        n4 ---E(r=1)--- n3

    Expected output:
        Production should not apply. apply(p1) == 0.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n3)
        self.g.add_node(n4)

        self.g.add_edge(HyperEdge((n1, n2), "E", r=1))
        self.g.add_edge(HyperEdge((n2, n3), "E", r=1))
        self.g.add_edge(HyperEdge((n3, n4), "E", r=1))
        self.g.add_edge(HyperEdge((n4, n1), "E", r=1))

        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0))

    def test_production_application(self):
        draw(self.g, DRAW_DIR / "p1_case7_before.png")

        p1 = P1()
        
        assert self.g.apply(p1) == 0
        
        draw(self.g, DRAW_DIR / "p1_case7_after.png")


class TestP1Case8:
    """
    Test case 8: Square with b parameter test - edges on boundary vs internal.
    
    Structure:
        n1 ---E(r=0,b=1)--- n2
        |                   |
        E(r=0,b=1)  Q(r=0)  E(r=0,b=1)
        |                   |
        n4 ---E(r=0,b=0)--- n3

    Expected output:
        Production should apply and set r=1 for all E edges.
        The b parameter should remain unchanged (preserved from original).
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        n3 = Node(2, 2, "n3")
        n4 = Node(0, 2, "n4")

        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_node(n3)
        self.g.add_node(n4)

        # Three boundary edges (b=1) and one internal edge (b=0)
        self.g.add_edge(HyperEdge((n1, n2), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n2, n3), "E", r=0, b=1))
        self.g.add_edge(HyperEdge((n3, n4), "E", r=0, b=0))
        self.g.add_edge(HyperEdge((n4, n1), "E", r=0, b=1))

        self.g.add_edge(HyperEdge((n1, n2, n3, n4), "Q", r=0))

    def test_production_application(self):
        draw(self.g, DRAW_DIR / "p1_case8_before.png")

        p1 = P1()
        assert self.g.apply(p1) == 1
        
        draw(self.g, DRAW_DIR / "p1_case8_after.png")

        # Check that all E edges have r=1
        for edge in self.g.hyperedges:
            if edge.hypertag == "E":
                assert edge.r == 1
        
        # Check that b parameter is preserved
        edge_b_values = {edge.label: edge.b for edge in self.g.hyperedges if edge.hypertag == "E"}
        
        # Verify specific b values (if edges can be identified)
        # n1-n2 should have b=1, n2-n3 should have b=1, n3-n4 should have b=0, n4-n1 should have b=1
        assert 1 in edge_b_values.values()  # At least one boundary edge exists
        assert 0 in edge_b_values.values()  # At least one internal edge exists
        
        # Applying again should return 0
        assert self.g.apply(p1) == 0
