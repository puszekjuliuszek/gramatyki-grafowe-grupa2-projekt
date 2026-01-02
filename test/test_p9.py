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

# NEW TESTS


class TestP9Negative:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.p9 = P9()
        self.g = Graph()
        
        self.nodes = [
            Node(1, 0, "n1"), Node(0.5, 0.866, "n2"), Node(-0.5, 0.866, "n3"),
            Node(-1, 0, "n4"), Node(-0.5, -0.866, "n5"), Node(0.5, -0.866, "n6")
        ]
        for n in self.nodes:
            self.g.add_node(n)

    def test_missing_boundary_edge(self):
        """
		Test: The hexagon is missing one peripheral edge 'E'. 
		Expected: The production should not be applied (no isomorphism).
        """
        boundary = self.nodes
        for i in range(len(boundary) - 1): # <--- only 5 edges
            curr_n = boundary[i]
            next_n = boundary[i + 1]
            self.g.add_edge(HyperEdge((curr_n, next_n), "E"))

        # Dodajemy poprawne wnętrze S
        self.g.add_edge(HyperEdge(tuple(self.nodes), "S", r=0))

        draw(self.g, str(DRAW_DIR / "test9-neg-missing-edge-stage0.png"))
        
        applied = self.g.apply(self.p9)
        
        assert applied == 0, "Production should not work with a broken edge loop"

    def test_wrong_central_label(self):
        """
		Test: The geometric structure is correct, but the center label is 'X' instead of 'S'. 
		Expected: The output should not be applied.
        """
        boundary = self.nodes
        for i in range(len(boundary)):
            curr_n = boundary[i]
            next_n = boundary[(i + 1) % len(boundary)]
            self.g.add_edge(HyperEdge((curr_n, next_n), "E"))

        self.g.add_edge(HyperEdge(tuple(self.nodes), "X", r=0))

        draw(self.g, str(DRAW_DIR / "test9-neg-wrong-label-stage0.png"))

        applied = self.g.apply(self.p9)

        assert applied == 0, "Produkcja nie powinna zadziałać dla etykiety 'X'"


class TestP9Complex:
    """
	Tests with a more complex graph structure.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.p9 = P9()
        self.g = Graph()

    def test_hexagon_embedded_in_larger_graph(self):
        """
		Test: A hexagon (satisfying P9) is connected to other vertices
		to form a larger structure (e.g., "a hexagon with a square attached").
		Structure:
		- Nodes 1-6 form hexagon P9 (S, r=0).
		- Nodes 1, 6, and the new nodes 7, 8 form an additional quadrangle next to it.

		Expected: The production should find a subgraph (hexagon) and change S to r=1 in it,
		without affecting the rest of the graph.
        """
        
        # Nodes 1-6
        h_nodes = [
            Node(1, 0, "n1"), Node(0.5, 0.866, "n2"), Node(-0.5, 0.866, "n3"),
            Node(-1, 0, "n4"), Node(-0.5, -0.866, "n5"), Node(0.5, -0.866, "n6")
        ]
        for n in h_nodes:
            self.g.add_node(n)
            
        for i in range(6):
            self.g.add_edge(HyperEdge((h_nodes[i], h_nodes[(i+1)%6]), "E"))
            
        # Hexagon's inside
        self.g.add_edge(HyperEdge(tuple(h_nodes), "S", r=0))

        # nodes 7 & 8
        n7 = Node(1.5, -0.866, "n7")
        n8 = Node(2.0, 0, "n8")
        self.g.add_node(n7)
        self.g.add_node(n8)

        # Adding n7 & n8 with hexagon (nodes n6 & n1), creating new shape
        # Edge n6 -> n7
        self.g.add_edge(HyperEdge((h_nodes[5], n7), "E")) 
        # Edge n7 -> n8
        self.g.add_edge(HyperEdge((n7, n8), "E"))
        # Edge n8 -> n1
        self.g.add_edge(HyperEdge((n8, h_nodes[0]), "E"))
        
        # Optional: The inside of this attachment (e.g. "Q") - should not be in the way
        quad_nodes = [h_nodes[0], h_nodes[5], n7, n8] # n1, n6, n7, n8
        self.g.add_edge(HyperEdge(tuple(quad_nodes), "Q", r=0))

        draw(self.g, str(DRAW_DIR / "test9-complex-stage0.png"))

        s_edges = [e for e in self.g.hyperedges if e.hypertag == "S"]
        assert len(s_edges) == 1
        assert s_edges[0].r == 0

        applied = self.g.apply(self.p9)

        draw(self.g, str(DRAW_DIR / "test9-complex-stage1.png"))

        assert applied == 1, "The production should find the hexagon despite the extra edges"
        
        s_edges_after = [e for e in self.g.hyperedges if e.hypertag == "S"]
        assert len(s_edges_after) == 1
        assert s_edges_after[0].r == 1
        
        q_edges = [e for e in self.g.hyperedges if e.hypertag == "Q"]
        assert len(q_edges) == 1
        assert q_edges[0].r == 0


class TestP9Attributes:
    """
    Tests verifying that the production is independent of additional edge attributes 
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.p9 = P9()
        self.g = Graph()
        
        # Create standard hexagon nodes
        self.nodes = [
            Node(1, 0, "n1"), Node(0.5, 0.866, "n2"), Node(-0.5, 0.866, "n3"),
            Node(-1, 0, "n4"), Node(-0.5, -0.866, "n5"), Node(0.5, -0.866, "n6")
        ]
        for n in self.nodes:
            self.g.add_node(n)

    def test_production_ignores_B_param(self):
        """
        Test: 'E' type edges possess a 'B' attribute with varying values.
        
        The matching algorithm should ignore attributes that are not explicitly 
        restricted by the left side of production P9.
        """
        
        # Create boundary edges and assign the 'B' attribute
        boundary = self.nodes
        for i in range(len(boundary)):
            curr_n = boundary[i]
            next_n = boundary[(i + 1) % len(boundary)]
            
            edge = HyperEdge((curr_n, next_n), "E")
            
            # Simulate the existence of parameter B.
            # We assign different values to ensure the match isn't 
            # dependent on a specific value.
            edge.B = (i % 2) + 1  # Values: 1, 2, 1, 2...
            
            self.g.add_edge(edge)

        # Add the central 'S' hyperedge
        self.g.add_edge(HyperEdge(tuple(self.nodes), "S", r=0))

        # Check if the edges actually have the B attribute (sanity check for the test setup)
        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(hasattr(e, 'B') for e in e_edges), "Edges should have attribute B for this test"

        # Apply the production
        applied = self.g.apply(self.p9)

        # Assertion: Production should apply successfully (return 1) 
        # despite the presence of the B parameter.
        assert applied == 1, "Production should apply regardless of the B parameter on edges"
        
        # Verify the transformation (S should have r=1)
        s_edges = [e for e in self.g.hyperedges if e.hypertag == "S"]
        assert s_edges[0].r == 1