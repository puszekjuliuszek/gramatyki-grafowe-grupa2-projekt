"""
Tests for production P1 - split edge E.
"""

import os
import pytest
from pathlib import Path

from node import Node
from edge import HyperEdge
from graph import Graph
from productions.p1 import P1
from visualization import draw

# Folder for visualizations - relative to project root
DRAW_DIR = Path(__file__).parent.parent / "draw"


@pytest.fixture(autouse=True)
def ensure_draw_dir():
    """Ensures the draw folder exists."""
    DRAW_DIR.mkdir(exist_ok=True)


class TestP1Case1:
    """
    Test case 1: Simple graph with two nodes connected by edge E.
    
    Input:
        n1 (0,0) ---E--- n2 (2,0)
        
    Expected output:
        n1 (0,0) ---E--- n3 (1,0) ---E--- n2 (2,0)
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Prepare test graph and production."""
        self.g = Graph()
        
        # Create two nodes
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        
        self.g.add_node(n1)
        self.g.add_node(n2)
        
        # Connect them with edge E with boundary=True
        e1 = HyperEdge((n1, n2), "E", boundary=True)
        self.g.add_edge(e1)
        
        # Create production
        self.p1 = P1()
    
    def test_stage0(self):
        """Test input graph (before applying production)."""
        # Save visualization
        draw(self.g, str(DRAW_DIR / "test1-case1-stage0.png"))
        
        # Check node count
        cnt = self.g.count_nodes()
        assert cnt.normal == 2, "Should be 2 regular nodes"
        assert cnt.hyper == 1, "Should be 1 hyperedge"
        
        # Check nodes
        assert self.g.get_node("n1") is not None
        assert self.g.get_node("n2") is not None
        
        # Check hyperedges
        assert len(self.g.hyperedges) == 1
        assert self.g.hyperedges[0].hypertag == "E"
    
    def test_stage1(self):
        """Test graph after applying production P1."""
        # Apply production
        applied = self.g.apply(self.p1)
        
        # Save visualization
        draw(self.g, str(DRAW_DIR / "test1-case1-stage1.png"))
        
        # Check if production was applied
        assert applied == 1, "Production should be applied 1 time"
        
        # Check node count
        cnt = self.g.count_nodes()
        assert cnt.normal == 3, "Should be 3 regular nodes (2 original + 1 new)"
        assert cnt.hyper == 2, "Should be 2 hyperedges"
        
        # Check if new node was added
        new_node = self.g.get_node("0_n3")
        assert new_node is not None, "New node 0_n3 should exist"
        
        # Check coordinates of new node (midpoint between (0,0) and (2,0))
        assert new_node.x == 1.0, "X coordinate of new node should be 1.0"
        assert new_node.y == 0.0, "Y coordinate of new node should be 0.0"


class TestP1Case2:
    """
    Test case 2: Graph with nodes not on X axis.
    
    Input:
        n1 (0,0) ---E--- n2 (4,4)
        
    Expected output:
        n1 (0,0) ---E--- n3 (2,2) ---E--- n2 (4,4)
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Prepare test graph and production."""
        self.g = Graph()
        
        n1 = Node(0, 0, "n1")
        n2 = Node(4, 4, "n2")
        
        self.g.add_node(n1)
        self.g.add_node(n2)
        
        # Edge without boundary
        e1 = HyperEdge((n1, n2), "E", boundary=False)
        self.g.add_edge(e1)
        
        self.p1 = P1()
    
    def test_stage0(self):
        """Test input graph."""
        draw(self.g, str(DRAW_DIR / "test1-case2-stage0.png"))
        
        cnt = self.g.count_nodes()
        assert cnt.normal == 2
        assert cnt.hyper == 1
    
    def test_stage1(self):
        """Test graph after applying production."""
        applied = self.g.apply(self.p1)
        draw(self.g, str(DRAW_DIR / "test1-case2-stage1.png"))
        
        assert applied == 1
        
        cnt = self.g.count_nodes()
        assert cnt.normal == 3
        assert cnt.hyper == 2
        
        # Check coordinates of new node
        new_node = self.g.get_node("0_n3")
        assert new_node is not None
        assert new_node.x == 2.0
        assert new_node.y == 2.0
        
        # Check that new node is hanging (because boundary=False)
        assert new_node.hanging is True, "New node should be hanging when boundary=False"


class TestNodeBasics:
    """Basic tests for Node class."""
    
    def test_node_creation(self):
        """Test node creation."""
        n = Node(1.5, 2.5, "test_node")
        assert n.x == 1.5
        assert n.y == 2.5
        assert n.label == "test_node"
        assert n.hanging is False
    
    def test_node_hanging(self):
        """Test hanging node."""
        n = Node(0, 0, "hanging_node", hanging=True)
        assert n.hanging is True
    
    def test_node_equality(self):
        """Test node comparison."""
        n1 = Node(0, 0, "same_label")
        n2 = Node(1, 1, "same_label")  # different coordinates, same label
        n3 = Node(0, 0, "different_label")
        
        assert n1 == n2, "Nodes with the same label should be equal"
        assert n1 != n3, "Nodes with different labels should not be equal"


class TestHyperEdgeBasics:
    """Basic tests for HyperEdge class."""
    
    def test_hyperedge_creation(self):
        """Test hyperedge creation."""
        n1 = Node(0, 0, "n1")
        n2 = Node(1, 1, "n2")
        
        e = HyperEdge((n1, n2), "E")
        assert e.hypertag == "E"
        assert len(e.nodes) == 2
        assert e.boundary is False
    
    def test_hyperedge_boundary(self):
        """Test boundary hyperedge."""
        n1 = Node(0, 0, "n1")
        n2 = Node(1, 1, "n2")
        
        e = HyperEdge((n1, n2), "E", boundary=True)
        assert e.boundary is True
    
    def test_hyperedge_label(self):
        """Test hyperedge label."""
        n1 = Node(0, 0, "n1")
        n2 = Node(1, 1, "n2")
        
        e = HyperEdge((n1, n2), "E")
        assert e.label == "E_n1_n2"
    
    def test_hyperedge_minimum_nodes(self):
        """Test that hyperedge requires at least 2 nodes."""
        n1 = Node(0, 0, "n1")
        
        with pytest.raises(ValueError):
            HyperEdge((n1,), "E")


class TestGraphBasics:
    """Basic tests for Graph class."""
    
    def test_graph_creation(self):
        """Test empty graph creation."""
        g = Graph()
        assert len(g.nodes) == 0
        assert len(g.hyperedges) == 0
    
    def test_add_node(self):
        """Test adding a node."""
        g = Graph()
        n = Node(0, 0, "test")
        g.add_node(n)
        
        assert len(g.nodes) == 1
        assert g.get_node("test") is not None
    
    def test_add_edge(self):
        """Test adding a hyperedge."""
        g = Graph()
        n1 = Node(0, 0, "n1")
        n2 = Node(1, 1, "n2")
        
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(HyperEdge((n1, n2), "E"))
        
        assert len(g.hyperedges) == 1
    
    def test_count_nodes(self):
        """Test node counting."""
        g = Graph()
        n1 = Node(0, 0, "n1")
        n2 = Node(1, 1, "n2")
        
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(HyperEdge((n1, n2), "E"))
        
        cnt = g.count_nodes()
        assert cnt.normal == 2
        assert cnt.hyper == 1
