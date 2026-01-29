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
from visualization import draw as draw_graph, draw_clean
import os

def run_derivation():
    # Ensure draw directory exists
    os.makedirs("draw", exist_ok=True)

    # --- Initial Graph Construction ---
    g = Graph()

    # Central Rectangle Nodes (Inner)
    ic_bl = Node(2, 2, "ic_bl")
    ic_br = Node(4, 2, "ic_br")
    ic_tr = Node(4, 4, "ic_tr")
    ic_tl = Node(2, 4, "ic_tl")

    # Outer Boundary Nodes
    oc_bl = Node(1, 1, "oc_bl")
    oc_br = Node(5, 1, "oc_br")
    oc_tl = Node(1, 5, "oc_tl")
    oc_tr = Node(5, 5, "oc_tr")
    
    # Right Hexagon extra nodes
    hex_r_top = Node(7, 4, "hex_r_top")
    hex_r_bot = Node(7, 2, "hex_r_bot")

    # Add all nodes
    nodes = [
        ic_bl, ic_br, ic_tr, ic_tl,
        oc_bl, oc_br, oc_tl, oc_tr,
        hex_r_top, hex_r_bot
    ]
    for n in nodes:
        g.add_node(n)

    # --- Define Faces (Hyperedges) ---

    # 1. Central Rectangle
    g.add_edge(HyperEdge((ic_bl, ic_br, ic_tr, ic_tl), "Q", r=0))
    g.add_edge(HyperEdge((ic_bl, ic_br), "E", r=0))
    g.add_edge(HyperEdge((ic_br, ic_tr), "E", r=0))
    g.add_edge(HyperEdge((ic_tr, ic_tl), "E", r=0))
    g.add_edge(HyperEdge((ic_tl, ic_bl), "E", r=0))

    # 2. Bottom Quad
    g.add_edge(HyperEdge((oc_bl, oc_br, ic_br, ic_bl), "Q", r=0))
    g.add_edge(HyperEdge((oc_bl, oc_br), "E", r=0, b=1))
    g.add_edge(HyperEdge((oc_br, ic_br), "E", r=0, b=0))
    g.add_edge(HyperEdge((ic_bl, oc_bl), "E", r=0, b=0))
        
    # 3. Top Quad
    g.add_edge(HyperEdge((ic_tl, ic_tr, oc_tr, oc_tl), "Q", r=0))
    g.add_edge(HyperEdge((oc_tr, oc_tl), "E", r=0, b=1))
    g.add_edge(HyperEdge((oc_tl, ic_tl), "E", r=0, b=0))
    g.add_edge(HyperEdge((ic_tr, oc_tr), "E", r=0, b=0))

    # 4. Left Quad
    g.add_edge(HyperEdge((oc_bl, ic_bl, ic_tl, oc_tl), "Q", r=0))
    g.add_edge(HyperEdge((oc_bl, oc_tl), "E", r=0, b=1))

    # 5. Right Hexagon
    g.add_edge(HyperEdge((ic_br, oc_br, hex_r_bot, hex_r_top, oc_tr, ic_tr), "S", r=0))
    g.add_edge(HyperEdge((oc_br, hex_r_bot), "E", r=0, b=1))
    g.add_edge(HyperEdge((hex_r_bot, hex_r_top), "E", r=0, b=1))
    g.add_edge(HyperEdge((hex_r_top, oc_tr), "E", r=0, b=1))
    
    draw_graph(g, "draw/group2_step0_initial")
    print("Initial graph created.")

    # --- Step 1: Split Bottom Quad ---
    print("\n--- Step 1: Split Bottom Quad ---")
    
    bottom_q = None
    for edge in g.hyperedges:
        if edge.hypertag == "Q":
            cy = sum(n.y for n in edge.nodes) / len(edge.nodes)
            if 1.2 < cy < 1.8:
                bottom_q = edge
                break
    
    if bottom_q:
        bottom_q.r = 1
        print("Marked Bottom Quad for splitting.")
        draw_graph(g, "draw/group2_step1_1_marked")
        
        p1 = P1()
        g.apply(p1)
        draw_graph(g, "draw/group2_step1_2_p1")
        
        p3, p4 = P3(), P4()
        while True:
            c3 = g.apply(p3)
            c4 = g.apply(p4)
            if c3 == 0 and c4 == 0:
                break
        draw_graph(g, "draw/group2_step1_3_broken")
        
        p5 = P5()
        g.apply(p5)
        draw_graph(g, "draw/group2_step1_4_split")
        draw_clean(g, "draw/group2_step1_4_split_clean")
        print("Bottom Quad split complete.")
    else:
        print("Error: Bottom Quad not found.")

    # --- Step 2: Split Right Hexagon ---
    print("\n--- Step 2: Split Right Hexagon ---")
    
    p9 = P9()
    if g.apply(p9) > 0:
        print("Marked Right Hexagon with P9.")
        draw_graph(g, "draw/group2_step2_1_marked")
        
        p10 = P10()
        g.apply(p10)
        draw_graph(g, "draw/group2_step2_2_p10")

        p3, p4 = P3(), P4()
        while True:
            c3 = g.apply(p3)
            c4 = g.apply(p4)
            if c3 == 0 and c4 == 0:
                break
        draw_graph(g, "draw/group2_step2_3_broken")
        
        p11 = P11()
        g.apply(p11)
        draw_graph(g, "draw/group2_step2_4_split")
        draw_clean(g, "draw/group2_step2_4_split_clean")
        print("Right Hexagon split complete.")
    else:
        print("Error: Right Hexagon not found.")

    # --- Step 3: Refine Corner Quads (Iterative) ---
    print("\n--- Step 3: Refine Corner Quads ---")
    
    focal_node_label = "oc_br"
    
    for iteration in range(5):
        print(f"\nRefinement Iteration {iteration + 1}")
        
        quads_to_split = []
        for edge in g.hyperedges:
            if edge.hypertag == "Q" and edge.r == 0:
                has_focal = any(n.label == focal_node_label for n in edge.nodes)
                
                # Exclude Central Rect
                cx = sum(n.x for n in edge.nodes) / len(edge.nodes)
                cy = sum(n.y for n in edge.nodes) / len(edge.nodes)
                is_central = abs(cx - 3) < 0.1 and abs(cy - 3) < 0.1
                
                # Exclude P11-origin Quads (they already have a center vertex)
                has_center = any("center" in n.label for n in edge.nodes)
                
                if has_focal and not is_central and not has_center:
                    quads_to_split.append(edge)

        print(f"Found {len(quads_to_split)} Quads to split at Corner.")
        
        if quads_to_split:
            for q in quads_to_split:
                q.r = 1
            
            draw_graph(g, f"draw/group2_step3_iter{iteration+1}_1_marked")
            
            p1 = P1()
            g.apply(p1)
            draw_graph(g, f"draw/group2_step3_iter{iteration+1}_2_p1")
            
            p3, p4 = P3(), P4()
            while True:
                c3 = g.apply(p3)
                c4 = g.apply(p4)
                if c3 == 0 and c4 == 0:
                    break
            
            draw_graph(g, f"draw/group2_step3_iter{iteration+1}_3_broken")
            
            p5 = P5()
            g.apply(p5)
            draw_graph(g, f"draw/group2_step3_iter{iteration+1}_4_split")
            draw_clean(g, f"draw/group2_step3_iter{iteration+1}_4_split_clean")
            print(f"Corner Refinement Iteration {iteration + 1} complete.")
        else:
            print(f"No quads found to split in Iteration {iteration + 1}.")
            break
        
    print("Derivation finished.")

if __name__ == "__main__":
    run_derivation()
