
import sys
import os

# Ensure we can import from current directory
sys.path.append(os.getcwd())

import networkx as nx
from graph import Graph
from node import Node
from edge import HyperEdge
from productions.p11 import P11

def verify_p11():
    print("Setting up Graph for P11...")
    g = Graph()
    
    # Create the 12 nodes in a ring
    pattern_nodes_def = [
        (0, 1, "n1"), (0.5, 1.5, "n8"), (1, 2, "n6"), (1.5, 1.5, "n9"),
        (2, 1, "n4"), (2, 0.5, "n10"), (2, 0, "n3"), (1.5, -0.5, "n11"),
        (1, -1, "n5"), (0.5, -0.5, "n12"), (0, 0, "n2"), (0, 0.5, "n7")
    ]
    
    import random
    
    # Shuffle the definitions to prevent insertion-order luck
    node_indices = list(range(12))
    random.shuffle(node_indices)
    
    real_nodes = [None] * 12
    
    for idx in node_indices:
        x, y, label = pattern_nodes_def[idx]
        n = Node(x, y, label + "_real")
        g.add_node(n)
        real_nodes[idx] = n
        
    # Connect them with E edges (r=0) based on correct indices
    for i in range(12):
        u = real_nodes[i]
        v = real_nodes[(i+1)%12]
        g.add_edge(HyperEdge((u, v), "E", r=0))
        
    # Connect corners with S edge (r=1)
    corners = [real_nodes[i] for i in range(0, 12, 2)]
    g.add_edge(HyperEdge(tuple(corners), "S", r=1))
    
    print("Graph created.")
    
    p11 = P11()
    print("Applying P11...")
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
        
        center = next((n for n in ns if "center" in n.label), None)
        ring_nodes = [n for n in ns if n != center]
        
        if not center or len(ring_nodes) != 3:
            print(f"Quad {i} -> Invalid structure!")
            continue
            
        indices = sorted([real_nodes.index(n) for n in ring_nodes])
        print(f"Quad {i} indices: {indices}")
        
        # Check consecutive
        is_consecutive = False
        if len(indices) == 3:
             if (indices[1] == indices[0] + 1 and indices[2] == indices[1] + 1):
                 is_consecutive = True
             elif indices == [0, 1, 11]:
                 is_consecutive = True
        
        if is_consecutive:
            print("  -> OK")
            valid_quads += 1
        else:
            print("  -> BROKEN ADJACENCY")

    if valid_quads == 6:
        print("\nSUCCESS: P11 produced 6 topologically valid Quads.")
    else:
        print(f"\nFAILURE: P11 produced only {valid_quads}/6 valid Quads. ORDERING BUG CONFIRMED.")

if __name__ == "__main__":
    verify_p11()
