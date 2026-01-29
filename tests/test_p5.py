"""
Tests for P5 production - ensures V is connected to midpoints, not corners.
"""

import sys
sys.path.insert(0, 'src')

from graph import Graph
from node import Node
from edge import HyperEdge
from productions.p5 import P5
from productions.p1 import P1
from productions.p3 import P3
from productions.p4 import P4


def create_simple_quad_with_midpoints():
    """Create a simple quad that has been marked and broken (ready for P5)."""
    g = Graph()
    
    # Corners
    c1 = Node(0, 0, "c1")
    c2 = Node(2, 0, "c2")
    c3 = Node(2, 2, "c3")
    c4 = Node(0, 2, "c4")
    
    # Midpoints (on edges between corners)
    m12 = Node(1, 0, "m12")  # between c1-c2
    m23 = Node(2, 1, "m23")  # between c2-c3
    m34 = Node(1, 2, "m34")  # between c3-c4
    m41 = Node(0, 1, "m41")  # between c4-c1
    
    for n in [c1, c2, c3, c4, m12, m23, m34, m41]:
        g.add_node(n)
    
    # E edges (all broken, r=0)
    g.add_edge(HyperEdge((c1, m12), "E", r=0, b=1))
    g.add_edge(HyperEdge((m12, c2), "E", r=0, b=1))
    g.add_edge(HyperEdge((c2, m23), "E", r=0, b=0))
    g.add_edge(HyperEdge((m23, c3), "E", r=0, b=0))
    g.add_edge(HyperEdge((c3, m34), "E", r=0, b=1))
    g.add_edge(HyperEdge((m34, c4), "E", r=0, b=1))
    g.add_edge(HyperEdge((c4, m41), "E", r=0, b=0))
    g.add_edge(HyperEdge((m41, c1), "E", r=0, b=0))
    
    # Q hyperedge (marked for splitting, r=1)
    g.add_edge(HyperEdge((c1, c2, c3, c4), "Q", r=1))
    
    return g


def test_p5_connects_v_to_midpoints():
    """Test that P5 connects the new center V to midpoints, not corners."""
    g = create_simple_quad_with_midpoints()
    
    p5 = P5()
    count = g.apply(p5)
    
    assert count == 1, f"P5 should apply exactly once, applied {count} times"
    
    # Find the center V node
    v_node = None
    for node in g.nodes:
        if node.label.startswith("V_"):
            v_node = node
            break
    
    assert v_node is not None, "V node should be created"
    
    # Check V's position (should be at centroid)
    expected_x = (0 + 2 + 2 + 0) / 4  # = 1
    expected_y = (0 + 0 + 2 + 2) / 4  # = 1
    assert abs(v_node.x - expected_x) < 0.01, f"V x should be {expected_x}, got {v_node.x}"
    assert abs(v_node.y - expected_y) < 0.01, f"V y should be {expected_y}, got {v_node.y}"
    
    # Find E edges connected to V
    v_edges = []
    for edge in g.hyperedges:
        if edge.hypertag == "E" and len(edge.nodes) == 2:
            if v_node.label in [n.label for n in edge.nodes]:
                other = [n for n in edge.nodes if n.label != v_node.label][0]
                v_edges.append(other)
    
    # V should be connected to 4 midpoints (m12, m23, m34, m41)
    assert len(v_edges) == 4, f"V should connect to 4 midpoints, connects to {len(v_edges)}"
    
    v_neighbor_labels = {n.label for n in v_edges}
    expected_midpoints = {"m12", "m23", "m34", "m41"}
    
    assert v_neighbor_labels == expected_midpoints, \
        f"V should connect to {expected_midpoints}, connects to {v_neighbor_labels}"
    
    print("✓ P5 correctly connects V to midpoints")
    return True


def test_p5_creates_4_subquads():
    """Test that P5 creates exactly 4 sub-quads."""
    g = create_simple_quad_with_midpoints()
    
    p5 = P5()
    g.apply(p5)
    
    q_edges = [e for e in g.hyperedges if e.hypertag == "Q"]
    
    assert len(q_edges) == 4, f"Should create 4 Q hyperedges, got {len(q_edges)}"
    
    # All should have r=0 (not marked)
    for q in q_edges:
        assert q.r == 0, f"New Q hyperedges should have r=0"
    
    print("✓ P5 creates 4 sub-quads correctly")
    return True


def test_p5_multiple_iterations():
    """Test that P5 works correctly for multiple refinement iterations."""
    g = create_simple_quad_with_midpoints()
    
    p1 = P1()
    p3 = P3()
    p4 = P4()
    p5 = P5()
    
    # First application
    g.apply(p5)
    
    for iteration in range(3):
        # Mark one of the sub-quads for refinement
        q_edge = None
        for edge in g.hyperedges:
            if edge.hypertag == "Q" and edge.r == 0:
                q_edge = edge
                break
        
        if q_edge is None:
            print(f"No more quads to refine at iteration {iteration}")
            break
        
        q_edge.r = 1
        
        # Apply P1 to mark edges
        g.apply(p1)
        
        # Break edges
        while True:
            c3 = g.apply(p3)
            c4 = g.apply(p4)
            if c3 == 0 and c4 == 0:
                break
        
        # Apply P5
        count = g.apply(p5)
        assert count > 0, f"P5 should apply in iteration {iteration}"
        
        # Verify structure
        for edge in g.hyperedges:
            if edge.hypertag == "E":
                assert len(edge.nodes) == 2, "All E edges should have 2 nodes"
        
        print(f"✓ Iteration {iteration + 1} completed successfully")
    
    print("✓ Multiple P5 iterations work correctly")
    return True


if __name__ == "__main__":
    print("Running P5 tests...\n")
    
    tests = [
        test_p5_connects_v_to_midpoints,
        test_p5_creates_4_subquads,
        test_p5_multiple_iterations,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
