import sys
from pathlib import Path

root = Path(__file__).parent.parent.parent
sys.path.append(str(root))
sys.path.append(str(root / "src"))

from src.graph import Graph
from src.node import Node
from src.edge import HyperEdge
from src.visualization import draw, draw_edges_only
from src.productions.p0 import P0
from src.productions.p1 import P1
from src.productions.p2 import P2
from src.productions.p3 import P3
from src.productions.p4 import P4
from src.productions.p5 import P5
from src.productions.p9 import P9
from src.productions.p10 import P10
from src.productions.p11 import P11


def _find_corner_quad_match(g, production, corner_node_label=None, alternate_index=0, exclude_node=None, include_node=None, include_node_prefix=None, min_x=None, min_y=None):
    """
    Find P0/P1 match for a quad in specific region.
    Supports both match conventions: pattern->graph (keys n1,n2,n3,n4,Q) or graph->pattern.
    Returns match as pattern_label -> graph_label (for apply_one_at_match).
    
    Args:
        min_x, min_y: If provided, only match quads with centroid >= min_x and >= min_y (for bottom-right region)
    """
    left = production.get_left_side()
    matches = g.find_subgraph_isomorphisms(left)
    if not matches:
        return None
    exclude_set = {exclude_node} if isinstance(exclude_node, str) else (set(exclude_node) if exclude_node else set())
    corner_matches = []
    for match in matches:
        if "n1" in match:
            graph_corner_labels = {match[p] for p in ("n1", "n2", "n3", "n4") if p in match}
            pattern_to_graph = dict(match)
        else:
            graph_corner_labels = {k for k in match if match.get(k) in ("n1", "n2", "n3", "n4")}
            pattern_to_graph = {v: k for k, v in match.items()}
        if len(graph_corner_labels) != 4:
            continue
        if corner_node_label is not None and corner_node_label not in graph_corner_labels:
            continue
        if exclude_set and exclude_set & graph_corner_labels:
            continue
        if include_node is not None or include_node_prefix is not None:
            has_include = include_node is not None and include_node in graph_corner_labels
            has_prefix = (
                include_node_prefix is not None
                and any(
                    str(gl).startswith(include_node_prefix) and (include_node is None or include_node in str(gl))
                    for gl in graph_corner_labels
                )
            )
            if not (has_include or has_prefix):
                continue
        all_graph_labels = list(pattern_to_graph.values())
        if not all(g._graph.has_node(gl) for gl in all_graph_labels):
            continue
        candidate_graph = Graph()
        for pattern_label, graph_label in pattern_to_graph.items():
            node_data = g._graph.nodes[graph_label]
            candidate_graph._graph.add_node(pattern_label, **node_data)
            if not node_data.get('is_hyper', False):
                candidate_graph._nodes[pattern_label] = node_data['node']
            else:
                candidate_graph._hyperedges[pattern_label] = node_data.get('hyperedge')
        if not production.filter_match(candidate_graph):
            continue
        corner_nodes = [g.get_node(pattern_to_graph[p]) for p in ("n1", "n2", "n3", "n4") if p in pattern_to_graph]
        corner_nodes = [n for n in corner_nodes if n and n.hyperref is None]
        if len(corner_nodes) != 4:
            continue
        centroid_y = sum(n.y for n in corner_nodes) / 4
        centroid_x = sum(n.x for n in corner_nodes) / 4
        
        # Filter by geometric position if specified
        if min_x is not None and centroid_x < min_x:
            continue
        if min_y is not None and centroid_y < min_y:
            continue
        
        corner_matches.append(((centroid_y, -centroid_x), pattern_to_graph))
    if not corner_matches:
        return None
    corner_matches.sort(key=lambda t: t[0])
    idx = min(alternate_index, len(corner_matches) - 1)
    return corner_matches[idx][1]


def _apply_split_to_quad(g, match_quad, p1, p3, p4, p5):
    """Apply P4/P3 on quad boundary edges, then P5. P1 assumed already applied."""
    corners = {match_quad["n1"], match_quad["n2"], match_quad["n3"], match_quad["n4"]}
    quad_edge_pairs = None
    corner_nodes = []
    corner_order = []  # Store corner order from Q hyperedge
    for edge in g.hyperedges:
        if edge.hypertag != "Q" or len(edge.nodes) != 4:
            continue
        if {n.label for n in edge.nodes} == corners:
            nodes = edge.nodes
            quad_edge_pairs = [(nodes[i].label, nodes[(i + 1) % 4].label) for i in range(4)]
            corner_nodes = [g.get_node(n.label) for n in nodes]
            corner_order = [n.label for n in nodes]  # Preserve order
            break
    if quad_edge_pairs is None:
        return False
    
    # Break edges with P3/P4
    boundary_edges = []
    internal_edges = []
    for (a, b) in quad_edge_pairs:
        for e in g.hyperedges:
            if e.hypertag != "E" or len(e.nodes) != 2:
                continue
            n1, n2 = e.nodes
            if {n1.label, n2.label} == {a, b} and getattr(e, "r", 0) == 1:
                (boundary_edges if getattr(e, "b", 0) == 1 else internal_edges).append((a, b))
                break
    
    for (a, b) in boundary_edges:
        g.apply_one(p4, a, b)
    for (a, b) in internal_edges:
        g.apply_one(p3, a, b)
    
    # Apply P5 - ensure we match the correct quad
    # P5's filter_match ensures exactly 8 nodes (4 corners + 4 midpoints), so it should only match our quad
    # Use apply_one with a corner to target the specific quad
    # Note: P5's isomorphism may assign pattern labels arbitrarily, but P5's get_right_side assumes
    # n5 on n1-n2, n6 on n2-n3, n7 on n3-n4, n8 on n4-n1. If the assignment is wrong, the center
    # will connect to wrong midpoints. Since we can't modify P5, we rely on the isomorphism
    # working correctly (which it should if the graph structure matches P5's pattern exactly).
    if corner_order:
        return g.apply_one(p5, corner_order[0])
    return False


def run_derivation():
    DRAW_DIR = Path(__file__).parent.parent.parent / "draw" / "G2_bottom_right"
    DRAW_DIR.mkdir(parents=True, exist_ok=True)
    # Remove old drawings so only numbered files remain
    for f in DRAW_DIR.glob("*.png"):
        f.unlink()

    g = Graph()
    e1 = Node(2, 6, "e1")
    e2 = Node(6, 6, "e2")
    e3 = Node(6, 3, "e3")
    e4 = Node(2, 3, "e4")
    e5 = Node(0, 9, "e5")
    e6 = Node(9, 9, "e6")
    e7 = Node(12, 6, "e7")
    e8 = Node(12, 3, "e8")
    e9 = Node(9, 0, "e9")
    e10 = Node(0, 0, "e10")
    e11 = Node(-2, 3, "e11")
    e12 = Node(-2, 6, "e12")

    for n in [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12]:
        g.add_node(n)
    g.add_edge(HyperEdge((e1, e2), "E", b=0))
    g.add_edge(HyperEdge((e2, e3), "E", b=0))
    g.add_edge(HyperEdge((e3, e4), "E", b=0))
    g.add_edge(HyperEdge((e4, e1), "E", b=0))
    g.add_edge(HyperEdge((e1, e2, e3, e4), "Q", r=0))
    g.add_edge(HyperEdge((e1, e5), "E", b=0))
    g.add_edge(HyperEdge((e5, e6), "E", b=1))
    g.add_edge(HyperEdge((e6, e2), "E", b=0))
    g.add_edge(HyperEdge((e6, e7), "E", b=1))
    g.add_edge(HyperEdge((e7, e8), "E", b=1))
    g.add_edge(HyperEdge((e8, e9), "E", b=1))
    g.add_edge(HyperEdge((e9, e10), "E", b=1))
    g.add_edge(HyperEdge((e10, e4), "E", b=0))
    g.add_edge(HyperEdge((e3, e9), "E", b=0))
    g.add_edge(HyperEdge((e4, e10), "E", b=0))
    g.add_edge(HyperEdge((e10, e11), "E", b=1))
    g.add_edge(HyperEdge((e11, e12), "E", b=1))
    g.add_edge(HyperEdge((e12, e5), "E", b=1))
    g.add_edge(HyperEdge((e2, e3, e6, e7, e8, e9), "S", r=0))
    g.add_edge(HyperEdge((e10, e4, e3, e9), "Q", r=0))
    g.add_edge(HyperEdge((e10, e11, e12, e5, e4, e1), "S", r=0))
    g.add_edge(HyperEdge((e5, e6, e1, e2), "Q", r=0))

    p0, p1, p2, p3, p4, p5 = P0(), P1(), P2(), P3(), P4(), P5()
    p9, p10, p11 = P9(), P10(), P11()
    step = 1

    def save_both(gr, base_name, msg):
        draw(gr, str(DRAW_DIR / f"{base_name}.png"))
        print(f"{msg}: {base_name}.png")
        draw_edges_only(gr, str(DRAW_DIR / f"{base_name}_edges_only.png"))
        print("Edges only: " + base_name + "_edges_only.png")

    draw(g, str(DRAW_DIR / f"{step:03d}_initial_graph.png"))
    print(f"Step {step}: initial graph saved")
    step += 1

    # Bottom trapez first
    g.apply_one(p0, "e10")
    save_both(g, f"{step:03d}_p0_bottom", "P0 bottom")
    step += 1
    g.apply_one(p1, "e10")
    # P4: break boundary edges (use apply() to find all matching edges)
    p4_count = g.apply(p4)
    # P3: break internal edges (use apply() to find all matching edges)  
    p3_count = g.apply(p3)
    save_both(g, f"{step:03d}_bottom_p1_p4_p3", f"P1,P4({p4_count}x),P3({p3_count}x) bottom trapez")
    step += 1
    g.apply_one(p5, "e10")
    save_both(g, f"{step:03d}_p5_bottom", "P5 bottom")
    step += 1

    # Right hex
    g.apply_one(p9, "e6")
    draw(g, str(DRAW_DIR / f"{step:03d}_p9_right.png"))
    print(f"Step {step}: P9 right hex")
    step += 1
    g.apply_one(p10, "e6")
    # Break boundary edges with P4
    p4_count = g.apply(p4)
    save_both(g, f"{step:03d}_p10_p4_right", f"P10,P4({p4_count}x) right hex")
    step += 1
    # Break internal edges with P3
    p3_count = g.apply(p3)
    save_both(g, f"{step:03d}_p3_right", f"P3({p3_count}x) right hex")
    step += 1
    g.apply_one(p11, "e6")
    g.apply_one(p1, "e6")
    # Break edges again after P1
    p4_count2 = g.apply(p4)
    g.apply_one(p2, "e6")
    p3_count2 = g.apply(p3)
    g.apply_one(p5, "e6")
    save_both(g, f"{step:03d}_right_hex_done", f"Right hex done (P11,P1,P4({p4_count2}x),P2,P3({p3_count2}x),P5)")
    step += 1

    # Corner iterations: alternate between breaking bottom-right trapez and hex bottom
    # Break bottom-right corner of trapez AND bottom-center of hex interchangeably
    NUM_ITERATIONS = 10  # Reduced to prevent excessive generation
    
    for iteration in range(NUM_ITERATIONS):
        applied_any = False
        
        # 1. Try to break bottom-right corner of trapez (x >= 6, y <= 3)
        # Get all P0 matches and filter by geometry
        left = p0.get_left_side()
        all_matches = g.find_subgraph_isomorphisms(left)
        trap_matches = []
        for match in all_matches:
            # Convert to pattern->graph format
            if "n1" in match:
                pattern_to_graph = dict(match)
            else:
                pattern_to_graph = {v: k for k, v in match.items()}
            
            if not all(p in pattern_to_graph for p in ("n1", "n2", "n3", "n4")):
                continue
            
            # Build candidate for filter_match
            candidate = Graph()
            for pattern_label, graph_label in pattern_to_graph.items():
                if not g._graph.has_node(graph_label):
                    break
                node_data = g._graph.nodes[graph_label]
                candidate._graph.add_node(pattern_label, **node_data)
                if not node_data.get('is_hyper', False):
                    candidate._nodes[pattern_label] = node_data['node']
                else:
                    candidate._hyperedges[pattern_label] = node_data.get('hyperedge')
            else:
                if p0.filter_match(candidate):
                    corner_nodes = [g.get_node(pattern_to_graph[p]) for p in ("n1", "n2", "n3", "n4")]
                    corner_nodes = [n for n in corner_nodes if n and n.hyperref is None]
                    if len(corner_nodes) == 4:
                        cx = sum(n.x for n in corner_nodes) / 4
                        cy = sum(n.y for n in corner_nodes) / 4
                        # Bottom-right region: x >= 6, y <= 3
                        if cx >= 6.0 and cy <= 3.0:
                            trap_matches.append((cy, -cx, pattern_to_graph))  # Sort by bottom-right
        
        if trap_matches:
            trap_matches.sort(key=lambda t: t[:2], reverse=False)  # Bottom-right first: smallest y (bottom), then largest x (right)
            match_trap0 = trap_matches[0][2]
            # Get the corner nodes before applying P0
            corner_labels = {match_trap0[p] for p in ("n1", "n2", "n3", "n4")}
            g.apply_one_at_match(p0, match_trap0)
            save_both(g, f"{step:03d}_p0_trapez_bottom-right", f"P0 trapez bottom-right (iter {iteration+1})")
            step += 1
            applied_any = True
            
            # After P0, find the quad that was just marked (has r=1 now) and apply P1
            left1 = p1.get_left_side()
            all_matches1 = g.find_subgraph_isomorphisms(left1)
            for match in all_matches1:
                if "n1" in match:
                    pattern_to_graph = dict(match)
                else:
                    pattern_to_graph = {v: k for k, v in match.items()}
                
                # Check if this match corresponds to the quad we just marked
                match_corners = {pattern_to_graph[p] for p in ("n1", "n2", "n3", "n4") if p in pattern_to_graph}
                if match_corners == corner_labels:  # Same quad
                    candidate = Graph()
                    for pattern_label, graph_label in pattern_to_graph.items():
                        if not g._graph.has_node(graph_label):
                            break
                        node_data = g._graph.nodes[graph_label]
                        candidate._graph.add_node(pattern_label, **node_data)
                        if not node_data.get('is_hyper', False):
                            candidate._nodes[pattern_label] = node_data['node']
                        else:
                            candidate._hyperedges[pattern_label] = node_data.get('hyperedge')
                    else:
                        if p1.filter_match(candidate):
                            g.apply_one_at_match(p1, pattern_to_graph)
                            save_both(g, f"{step:03d}_p1_trapez_bottom-right", f"P1 trapez bottom-right (iter {iteration+1})")
                            step += 1
                            _apply_split_to_quad(g, pattern_to_graph, p1, p3, p4, p5)
                            save_both(g, f"{step:03d}_split_trapez_bottom-right", f"Split trapez bottom-right (iter {iteration+1})")
                            step += 1
                            break
        
        # 2. Try to break bottom-center of right hex (quads with center/V_ nodes, y <= 5)
        hex_matches = []
        for match in all_matches:
            if "n1" in match:
                pattern_to_graph = dict(match)
            else:
                pattern_to_graph = {v: k for k, v in match.items()}
            
            if not all(p in pattern_to_graph for p in ("n1", "n2", "n3", "n4")):
                continue
            
            # Check if quad has center/V_ node
            graph_labels = list(pattern_to_graph.values())
            has_center = any("V_" in str(gl) or "center" in str(gl) for gl in graph_labels)
            if not has_center:
                continue
            
            candidate = Graph()
            for pattern_label, graph_label in pattern_to_graph.items():
                if not g._graph.has_node(graph_label):
                    break
                node_data = g._graph.nodes[graph_label]
                candidate._graph.add_node(pattern_label, **node_data)
                if not node_data.get('is_hyper', False):
                    candidate._nodes[pattern_label] = node_data['node']
                else:
                    candidate._hyperedges[pattern_label] = node_data.get('hyperedge')
            else:
                if p0.filter_match(candidate):
                    corner_nodes = [g.get_node(pattern_to_graph[p]) for p in ("n1", "n2", "n3", "n4")]
                    corner_nodes = [n for n in corner_nodes if n and n.hyperref is None]
                    if len(corner_nodes) == 4:
                        cy = sum(n.y for n in corner_nodes) / 4
                        if cy <= 5.0:  # Bottom region
                            hex_matches.append((cy, pattern_to_graph))
        
        if hex_matches:
            hex_matches.sort(key=lambda t: t[0])  # Bottom first
            match_hex0 = hex_matches[0][1]
            # Get the corner labels before applying P0
            hex_corner_labels = {match_hex0[p] for p in ("n1", "n2", "n3", "n4") if p in match_hex0}
            g.apply_one_at_match(p0, match_hex0)
            save_both(g, f"{step:03d}_p0_hex_bottom", f"P0 hex bottom (iter {iteration+1})")
            step += 1
            applied_any = True
            
            # After P0, find the quad that was just marked and apply P1
            left1 = p1.get_left_side()
            all_matches1 = g.find_subgraph_isomorphisms(left1)
            for match in all_matches1:
                if "n1" in match:
                    pattern_to_graph = dict(match)
                else:
                    pattern_to_graph = {v: k for k, v in match.items()}
                
                # Check if this match corresponds to the quad we just marked
                match_corners = {pattern_to_graph[p] for p in ("n1", "n2", "n3", "n4") if p in pattern_to_graph}
                if match_corners == hex_corner_labels:  # Same quad
                    candidate = Graph()
                    for pattern_label, graph_label in pattern_to_graph.items():
                        if not g._graph.has_node(graph_label):
                            break
                        node_data = g._graph.nodes[graph_label]
                        candidate._graph.add_node(pattern_label, **node_data)
                        if not node_data.get('is_hyper', False):
                            candidate._nodes[pattern_label] = node_data['node']
                        else:
                            candidate._hyperedges[pattern_label] = node_data.get('hyperedge')
                    else:
                        if p1.filter_match(candidate):
                            g.apply_one_at_match(p1, pattern_to_graph)
                            save_both(g, f"{step:03d}_p1_hex_bottom", f"P1 hex bottom (iter {iteration+1})")
                            step += 1
                            _apply_split_to_quad(g, pattern_to_graph, p1, p3, p4, p5)
                            save_both(g, f"{step:03d}_split_hex_bottom", f"Split hex bottom (iter {iteration+1})")
                            step += 1
                            break
        
        if not applied_any:
            print(f"No more matches found after {iteration+1} iterations")
            break

    save_both(g, f"{step:03d}_final_graph", "Final")
    print(f"Derivation complete! Generated {step} steps.")


if __name__ == "__main__":
    run_derivation()
