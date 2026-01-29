
import networkx as nx
from graph import Graph
from node import Node
from edge import HyperEdge
from productions.p1 import P1
from productions.p3 import P3
from productions.p4 import P4
from productions.p5 import P5
from productions.p9 import P9
from productions.p10 import P10
from productions.p11 import P11
import os

def check_step3():
    # ... Copying setup from group2_derivation ...
    g = Graph()
    ic_bl = Node(2, 2, "ic_bl")
    ic_br = Node(4, 2, "ic_br")
    ic_tr = Node(4, 4, "ic_tr")
    ic_tl = Node(2, 4, "ic_tl")
    oc_bl = Node(1, 1, "oc_bl")
    oc_br = Node(5, 1, "oc_br")
    oc_tl = Node(1, 5, "oc_tl")
    oc_tr = Node(5, 5, "oc_tr")
    hex_r_top = Node(7, 4, "hex_r_top")
    hex_r_bot = Node(7, 2, "hex_r_bot")
    nodes = [ic_bl, ic_br, ic_tr, ic_tl, oc_bl, oc_br, oc_tl, oc_tr, hex_r_top, hex_r_bot]
    for n in nodes: g.add_node(n)
    
    g.add_edge(HyperEdge((ic_bl, ic_br, ic_tr, ic_tl), "Q", r=0))
    g.add_edge(HyperEdge((ic_bl, ic_br), "E", r=0))
    g.add_edge(HyperEdge((ic_br, ic_tr), "E", r=0))
    g.add_edge(HyperEdge((ic_tr, ic_tl), "E", r=0))
    g.add_edge(HyperEdge((ic_tl, ic_bl), "E", r=0))
    # ... Top/Bottom/Left Quads omitted as they are not focal ...
    
    # Right Hexagon
    g.add_edge(HyperEdge((ic_br, oc_br, hex_r_bot, hex_r_top, oc_tr, ic_tr), "S", r=0))
    g.add_edge(HyperEdge((oc_br, hex_r_bot), "E", r=0, b=1))
    g.add_edge(HyperEdge((hex_r_bot, hex_r_top), "E", r=0, b=1))
    g.add_edge(HyperEdge((hex_r_top, oc_tr), "E", r=0, b=1))
    # Add connecting edges for Hex that missed in minimal setup?
    # (ic_br, oc_br), (oc_tr, ic_tr), (ic_tr, ic_br) E edges?
    # In original script they are part of Quads.
    g.add_edge(HyperEdge((oc_br, ic_br), "E", r=0, b=0)) # From Bottom Quad
    g.add_edge(HyperEdge((ic_tr, oc_tr), "E", r=0, b=0)) # From Top Quad
    g.add_edge(HyperEdge((ic_br, ic_tr), "E", r=0))      # From Center Rect
    
    print("Graph setup complete.")
    
    # Step 2: Split Hexagon
    p9 = P9()
    g.apply(p9)
    p10 = P10()
    g.apply(p10)
    p3, p4 = P3(), P4()
    while True:
        if g.apply(p3) == 0 and g.apply(p4) == 0: break
    p11 = P11()
    g.apply(p11)
    
    print("Step 2 complete. Checking Quads...")
    
    focal_node_label = "ic_br"
    
    # Find the target Quad for Step 3
    target_q = None
    for edge in g.hyperedges:
        if edge.hypertag == "Q" and edge.r == 0:
             if any(n.label == focal_node_label for n in edge.nodes):
                 # Filter central
                 cx = sum(n.x for n in edge.nodes) / len(edge.nodes)
                 if not (abs(cx - 3) < 0.1): 
                     target_q = edge
                     break
    
    if not target_q:
        print("Target Quad not found!")
        return
        
    print(f"Target Quad Found: Nodes {[n.label for n in target_q.nodes]}")
    
    # Prepare for Step 3
    target_q.r = 1
    p1 = P1()
    g.apply(p1)
    
    print("Applied P1. Breaking edges...")
    p3, p4 = P3(), P4()
    while True:
        if g.apply(p3) == 0 and g.apply(p4) == 0: break
        
    print("Edges broken. Inspecting state before P5.")
    
    # Inspect the environment of the Target Quad
    # It should have 4 corners (original nodes of target_q)
    # And 4 midpoints (newly created)
    # And E edges connecting them
    
    corners = target_q.nodes
    print(f"Corners: {[n.label for n in corners]}")
    
    for i in range(len(corners)):
        u = corners[i]
        v = corners[(i+1)%4]
        print(f"Checking path between {u.label} and {v.label}...")
        
        # Look for E edges involving u
        adj_u = []
        for e in g.hyperedges:
            if e.hypertag == "E" and u in e.nodes:
                other = e.nodes[0] if e.nodes[1] == u else e.nodes[1]
                adj_u.append((other, e))
        
        found_path = False
        for mid, e1 in adj_u:
            # Check if mid connects to v
            for e2 in g.hyperedges:
                if e2.hypertag == "E" and midpoint_connects(e2, mid, v):
                    print(f"  Path Found: {u.label} --({e1.r})-- {mid.label} --({e2.r})-- {v.label}")
                    # Check if mid is connected to Q?
                    is_in_Q = False
                    for q in g.hyperedges:
                        if q.hypertag == "Q" and mid in q.nodes:
                            is_in_Q = True
                    print(f"    Midpoint in any Q? {is_in_Q}")
                    found_path = True
                    
        if not found_path:
            print(f"  NO PATH found between {u.label} and {v.label} via a midpoint!")
            # Check direct connection?
            for e in g.hyperedges:
                 if e.hypertag == "E" and u in e.nodes and v in e.nodes:
                     print(f"  Direct connection exists (r={e.r}). Edge splitting failed!")

def midpoint_connects(edge, n1, n2):
    return (edge.nodes[0] == n1 and edge.nodes[1] == n2) or (edge.nodes[1] == n1 and edge.nodes[0] == n2)

if __name__ == "__main__":
    check_step3()
