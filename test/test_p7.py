import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p7 import P7
from visualization import draw

DRAW_DIR = Path(__file__).parent.parent / "draw"

@pytest.fixture(autouse=True)
def ensure_draw_dir():
    DRAW_DIR.mkdir(exist_ok=True)

class TestP7Case1:
    """
    Check if production P7 correctly updates all 'E' edges to r=1
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5")
        ]
        
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        for i, (start, end) in enumerate(edges_indices):
            e = HyperEdge((nodes[start], nodes[end]), "E", r=0)
            self.g.add_edge(e)

        p_edge = HyperEdge(tuple(nodes), "P", r=1)
        self.g.add_edge(p_edge)

        self.p7 = P7()

    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case1-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 5
        assert cnt.hyper == 6

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1
        assert p_edges[0].r == 1

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.r == 0 for e in e_edges)

    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case1-stage1.png"))

        assert applied == 1, "Production P7 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 5
        assert cnt.hyper == 6

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 1, "P edge should retain r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 1, f"All E edges must now have r=1. Found r={e.r}"


class TestP7Case2:
    """
    Check that production P7 is not applied when HyperEgde 'P'=0
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5")
        ]
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=0))

        self.p7 = P7()

    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case2-stage0.png"))
        
        cnt = self.g.count_nodes()
        assert cnt.normal == 5
        assert cnt.hyper == 6

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 0, "P edge should be r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 0, f"All E edges must now have r=0. Found r={e.r}"
        
    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)

        draw(self.g, str(DRAW_DIR / "test7-case2-stage1.png"))

        assert applied == 0, "Production P7 should not be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 5
        assert cnt.hyper == 6

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 0, "P edge should retain r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 0, f"All E edges must now have r=0. Found r={e.r}"
            

class TestP7Case3:
    """
    Check that production P7 is applied to both subgraphs if both have HyperEdge 'P'=0
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5")
        ]
        
        nodes1 = [
        Node(2, 0, "n6"),
        Node(3, 0, "n7"),
        Node(3, 1, "n8"),
        Node(2, 1, "n9"),
        Node(3 + (2 ** 0.5)/2 , 1/2, "n10")
        ]
        for n in nodes:
            self.g.add_node(n)

        for n in nodes1:
            self.g.add_node(n)
            
        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))
        
        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes1[start], nodes1[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=0))
        self.g.add_edge(HyperEdge(tuple(nodes1), "P", r=0))

        self.p7 = P7()

    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case3-stage0.png"))
        
        cnt = self.g.count_nodes()
        assert cnt.normal == 10
        assert cnt.hyper == 12

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 0, "P edge should retain r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 0, f"All E edges must have r=0. Found r={e.r}"
        
    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)

        draw(self.g, str(DRAW_DIR / "test7-case3-stage1.png"))

        assert applied == 0, "Production P7 should not be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 10
        assert cnt.hyper == 12

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 0, "P edge should retain r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 0, f"All E edges must have r=0. Found r={e.r}"
        
class TestP7Case4:
    """
    Check that production P7 is applied to both subgraphs if both have HyperEdge 'P'=1
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5")
        ]
        
        nodes1 = [
        Node(2, 0, "n6"),
        Node(3, 0, "n7"),
        Node(3, 1, "n8"),
        Node(2, 1, "n9"),
        Node(3 + (2 ** 0.5)/2 , 1/2, "n10")
        ]
        for n in nodes:
            self.g.add_node(n)

        for n in nodes1:
            self.g.add_node(n)
            
        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]

        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))
        
        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes1[start], nodes1[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=1))
        self.g.add_edge(HyperEdge(tuple(nodes1), "P", r=1))
        self.p7 = P7()

    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case4-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 10, "There should be 10 normal nodes"
        assert cnt.hyper == 12, "There should be 12 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 2, "There should be two P HyperEdges"
        assert p_edges[0].r == 1, "P edge should be r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.r == 0 for e in e_edges), f"All E edges must have r=0. Found {[e.r for e in e_edges]}"

    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case4-stage1.png"))

        assert applied == 2, "Production P7 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 10, "There should be 10 normal nodes"
        assert cnt.hyper == 12, "There should be 12 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 1, "P edge should retain r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 1, f"All E edges must now have r=1. Found r={e.r}"
            
class TestP7Case5:
    """
    Check that production P7 is not applied when grapth is missing one node
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4")
        ]
        
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (2, 3), (3, 0)]
        for i, (start, end) in enumerate(edges_indices):
            e = HyperEdge((nodes[start], nodes[end]), "E", r=0)
            self.g.add_edge(e)

        p_edge = HyperEdge(tuple(nodes), "P", r=1)
        self.g.add_edge(p_edge)

        self.p7 = P7()

    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case5-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 4, "There should be 4 normal nodes"
        assert cnt.hyper == 4, "There should be 4 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1, "There should be one P HyperEdge"
        assert p_edges[0].r == 1, "P edge should be r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.r == 0 for e in e_edges), f"All E edges must have r=0. Found {[e.r for e in e_edges]}"

    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case5-stage1.png"))

        assert applied == 0, "Production P7 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 4, "There should be 4 normal nodes"
        assert cnt.hyper == 4, "There should be 4 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 1, "P edge should retain r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 0, f"All E edges must have r=0. Found r={e.r}"
            
class TestP7Case6:
    """
    Check that production P7 is applied when one 'E' edge has r=1 and rest have r=0
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5")
        ]
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        for start, end in edges_indices:
            if start == 1 and end == 4:
                self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=1))
            else:
                self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=1))

        self.p7 = P7()

    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case6-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 5
        assert cnt.hyper == 6

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1, "There should be one P HyperEdge"
        assert p_edges[0].r == 1, "P edge should be r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        counter = sum(1 for e in e_edges if e.r == 1)
        ct = 0
        assert counter == 1, "There should be exactly one E edge with r=1"
        for e in e_edges:
            if e.r == 0:
                continue
            if ct == 1 and e.r == 1:
                assert False, "There should be exactly one E edge with r=1"
            if e.r == 1:
                ct += 1
            

    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case6-stage1.png"))

        assert applied == 1, "Production P7 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 5, "There should be 5 normal nodes"
        assert cnt.hyper == 6, "There should be 6 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 1, "P edge should retain r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 1, f"All E edges must now have r=1. Found r={e.r}"
            

class TestP7Case7:
    """
    Check that production P7 is applied when one 'E' edge has r=1 and rest have r=0 and 'P' edge has r=0
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5")
        ]
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        for start, end in edges_indices:
            if start == 1 and end == 4:
                self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=1))
            else:
                self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=0))

        self.p7 = P7()

    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case7-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 5, "There should be 5 normal nodes"
        assert cnt.hyper == 6, "There should be 6 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1, "There should be one P HyperEdge"
        assert p_edges[0].r == 0, "P edge should be r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        counter = sum(1 for e in e_edges if e.r == 1)
        ct = 0
        assert counter == 1, "There should be exactly one E edge with r=1"
        for e in e_edges:
            if e.r == 0:
                continue
            if ct == 1 and e.r == 1:
                assert False, "There should be exactly one E edge with r=1"
            if e.r == 1:
                ct += 1

    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case7-stage1.png"))

        assert applied == 0, "Production P7 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 5, "There should be 5 normal nodes"
        assert cnt.hyper == 6, "There should be 6 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 0, "P edge should retain r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        counter = sum(1 for e in e_edges if e.r == 1)
        ct = 0
        assert counter == 1, "There should be exactly one E edge with r=1"
        for e in e_edges:
            if e.r == 0:
                continue
            if ct == 1 and e.r == 1:
                assert False, "There should be exactly one E edge with r=1"
            if e.r == 1:
                ct += 1
                
class TestP7Case8:
    """
    Check that production P7 is applied when left graph is a part of a bigger graph
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5"),
        Node(-1,0, "n6"),
        Node(-1, 1, "n7"),
        ]
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0), (5, 0), (5, 6)]
        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=1))

        self.p7 = P7()
        
    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case8-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 7, "There should be 7 normal nodes"
        assert cnt.hyper == 8, "There should be 8 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1, "There should be one P HyperEdge"
        assert p_edges[0].r == 1, "P edge should be r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.r == 0 for e in e_edges), f"All E edges must have r=0. Found {[e.r for e in e_edges]}"
        
    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5"),
        Node(-1,0, "n6"),
        Node(-1, 1, "n7"),
        ]
        
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case8-stage1.png"))

        assert applied == 1, "Production P7 should be applied exactly once"

        cnt = self.g.count_nodes()
        assert cnt.normal == 7, "There should be 7 normal nodes"
        assert cnt.hyper == 8, "There should be 8 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 1, "P edge should retain r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        # Check that only the edges of the left graph were updated
        left_graph_edges = set()
        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0)]
        for start, end in edges_indices:
            left_graph_edges.add( (nodes[start].label, nodes[end].label) )
        for e in e_edges:
            edge_tuple = (e.nodes[0].label, e.nodes[1].label)
            if edge_tuple in left_graph_edges:
                assert e.r == 1, f"All E edges in left graph must now have r=1. Found r={e.r}"
            else:
                assert e.r == 0, f"E edges outside left graph must retain r=0. Found r={e.r}"
            
class TestP7Case9:
    """
    Chck that production P7 is applied in graph containing 2 subgraphs matching left side
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5"),
        Node(-1, 0, "n6"),
        Node(-1, 1, "n7"),
        Node(-1 * (1 + (2 ** 0.5)/2) , 1/2, "n8"),
        ]
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0), (0,5), (5, 7), (6, 7), (3, 6)]
        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=1))

        self.p7 = P7()
        
    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case9-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 8, "There should be 8 normal nodes"
        assert cnt.hyper == 10, "There should be 10 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1, "There should be one P HyperEdge"
        assert p_edges[0].r == 1, "P edge should be r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.r == 0 for e in e_edges), f"All E edges must have r=0. Found {[e.r for e in e_edges]}"
        
    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case9-stage1.png"))

        assert applied == 2, "Production P7 should be applied exactly twice"

        cnt = self.g.count_nodes()
        assert cnt.normal == 8, "There should be 8 normal nodes"
        assert cnt.hyper == 10, "There should be 10 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 1, "P edge should retain r=1"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 1, f"All E edges must now have r=1. Found r={e.r}"
            
class TestP7Case10:
    """
    Chck that production P7 is applied in graph containing 2 subgraphs matching left side
    """
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()

        nodes = [
        Node(0, 0, "n1"),
        Node(1, 0, "n2"),
        Node(1, 1, "n3"),
        Node(0, 1, "n4"),
        Node(1 + (2 ** 0.5)/2 , 1/2, "n5"),
        Node(-1, 0, "n6"),
        Node(-1, 1, "n7"),
        Node(-1 * (1 + (2 ** 0.5)/2) , 1/2, "n8"),
        ]
        for n in nodes:
            self.g.add_node(n)

        edges_indices = [(0, 1), (1, 4), (4, 2), (2, 3), (3, 0), (0,5), (5, 7), (6, 7), (3, 6)]
        for start, end in edges_indices:
            self.g.add_edge(HyperEdge((nodes[start], nodes[end]), "E", r=0))

        self.g.add_edge(HyperEdge(tuple(nodes), "P", r=0))

        self.p7 = P7()
        
    def test_initial_state(self):
        """
        Verify initial state.
        """
        draw(self.g, str(DRAW_DIR / "test7-case9-stage0.png"))

        cnt = self.g.count_nodes()
        assert cnt.normal == 8, "There should be 8 normal nodes"
        assert cnt.hyper == 10, "There should be 10 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert len(p_edges) == 1, "There should be one P HyperEdge"
        assert p_edges[0].r == 0, "P edge should be r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        assert all(e.r == 0 for e in e_edges), f"All E edges must have r=0. Found {[e.r for e in e_edges]}"
        
    def test_applying_production(self):
        """
        Verify graph after applying P7.
        """
        applied = self.g.apply(self.p7)
        
        draw(self.g, str(DRAW_DIR / "test7-case9-stage1.png"))

        assert applied == 0, "Production P7 should be applied exactly twice"

        cnt = self.g.count_nodes()
        assert cnt.normal == 8, "There should be 8 normal nodes"
        assert cnt.hyper == 10, "There should be 10 hyperedges"

        p_edges = [e for e in self.g.hyperedges if e.hypertag == "P"]
        assert p_edges[0].r == 0, "P edge should retain r=0"

        e_edges = [e for e in self.g.hyperedges if e.hypertag == "E"]
        for e in e_edges:
            assert e.r == 0, f"All E edges must have r=0. Found r={e.r}"
