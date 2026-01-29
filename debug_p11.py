
import networkx as nx
from graph import Graph
from node import Node
from edge import HyperEdge
from productions.p11 import P11

def verify_p11():
    print("Setting up Graph for P11...")
    g = Graph()
    
    # Create the 12 nodes in a ring (simulate a hexagon with broken edges)
    # Coordinates roughly matching P11 left side to ensure match
    # P11 left side: n1(0,1), n8(0.5, 1.5), n6(1,2), ...
    
    # We'll just define them in a list and add them
    pattern_nodes_def = [
        (0, 1, "n1"), (0.5, 1.5, "n8"), (1, 2, "n6"), (1.5, 1.5, "n9"),
        (2, 1, "n4"), (2, 0.5, "n10"), (2, 0, "n3"), (1.5, -0.5, "n11"),
        (1, -1, "n5"), (0.5, -0.5, "n12"), (0, 0, "n2"), (0, 0.5, "n7")
    ]
    
    real_nodes = []
    for x, y, label in pattern_nodes_def:
        n = Node(x, y, label + "_real")
        g.add_node(n)
        real_nodes.append(n)
        
    # Connect them with E edges (r=0)
    for i in range(12):
        u = real_nodes[i]
        v = real_nodes[(i+1)%12]
        g.add_edge(HyperEdge((u, v), "E", r=0))
        
    # Connect corners with S edge (r=1)
    # Corners are indices 0, 2, 4, 6, 8, 10
    corners = [real_nodes[i] for i in range(0, 12, 2)]
    g.add_edge(HyperEdge(tuple(corners), "S", r=1))
    
    print("Graph created. Nodes:", [n.label for n in g.nodes])
    print("Applying P11...")
    
    p11 = P11()
    count = g.apply(p11)
    print(f"P11 applied {count} times.")
    
    if count == 0:
        print("P11 failed to match!")
        return

    # Check the produced Quads
    quads = [e for e in g.hyperedges if e.hypertag == "Q"]
    print(f"Generated {len(quads)} Quads.")
    
    valid_quads = 0
    for i, q in enumerate(quads):
        ns = q.nodes
        print(f"Quad {i} nodes: {[n.label for n in ns]}")
        # A valid quad from P11 should have 4 nodes: 3 from the ring + center
        # The 3 from the ring must be adjacent in the ring.
        
        # Identify the center node (it starts with "center")
        center = next((n for n in ns if "center" in n.label), None)
        ring_nodes = [n for n in ns if n != center]
        
        if not center or len(ring_nodes) != 3:
            print(f"  -> Invalid structure! Center: {center}, RingNodes: {len(ring_nodes)}")
            continue
            
        # Check adjacency of ring nodes
        # They should form a chain A-B-C in the original ring
        # We can check distance in the 'real_nodes' list
        indices = sorted([real_nodes.index(n) for n in ring_nodes])
        
        # Check if indices are consecutive (allowing for wrap-around)
        is_consecutive = False
        if indices[1] == indices[0] + 1 and indices[2] == indices[1] + 1:
            is_consecutive = True
        # Wrap around case: [0, 1, 11]
        elif indices == [0, 1, 11]:
            is_consecutive = True
        
        if is_consecutive:
            print("  -> Adjacency OK.")
            valid_quads += 1
        else:
            print(f"  -> Adjacency BROKEN! Indices: {indices}")

    if valid_quads == 6:
        print("\nSUCCESS: P11 produced 6 topologically valid Quads.")
    else:
        print(f"\nFAILURE: P11 produced only {valid_quads}/6 valid Quads. ORDERING BUG CONFIRMED.")

if __name__ == "__main__":
    verify_p11()
