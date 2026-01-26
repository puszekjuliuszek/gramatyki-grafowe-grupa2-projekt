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


def _find_corner_quad_match(g, production, corner_node_label=None, alternate_index=0, exclude_node=None, include_node=None, include_node_prefix=None):
    """
    Find P0 match for a quad in the bottom-right region.
    Supports both match conventions: pattern->graph (keys n1,n2,n3,n4,Q) or graph->pattern.
    Returns match as pattern_label -> graph_label (for apply_one_at_match).
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
    for edge in g.hyperedges:
        if edge.hypertag != "Q" or len(edge.nodes) != 4:
            continue
        if {n.label for n in edge.nodes} == corners:
            nodes = edge.nodes
            quad_edge_pairs = [(nodes[i].label, nodes[(i + 1) % 4].label) for i in range(4)]
            break
    if quad_edge_pairs is None:
        return False
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
    corner_list = list(corners)
    return g.apply_one(p5, corner_list[0]) if corner_list else False


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
    g.apply_one(p4, "e9")
    g.apply_one(p3, "e10", "e4")
    g.apply_one(p3, "e4", "e3")
    g.apply_one(p3, "e3", "e9")
    save_both(g, f"{step:03d}_bottom_p1_p4_p3", "P1,P4,P3 bottom trapez")
    step += 1
    g.apply_one(p5, "e10")
    save_both(g, f"{step:03d}_p5_bottom", "P5 bottom")
    step += 1

    # Right hex
    g.apply_one(p9, "e6")
    draw(g, str(DRAW_DIR / f"{step:03d}_p9_right.png"))
    step += 1
    g.apply_one(p10, "e6")
    g.apply_one(p4, "e6")
    g.apply_one(p4, "e8")
    g.apply_one(p4, "e9")
    save_both(g, f"{step:03d}_p10_p4_right", "P10,P4 right hex")
    step += 1
    g.apply_one(p3, "e6", "e2")
    g.apply_one(p3, "e2", "e3")
    g.apply_one(p3, "e3", "e9")
    save_both(g, f"{step:03d}_p3_right", "P3 right hex")
    step += 1
    g.apply_one(p11, "e6")
    g.apply_one(p1, "e6")
    g.apply_one(p4, "e6")
    g.apply_one(p2, "e6")
    g.apply_one(p3, "e5", "e2")
    g.apply_one(p5, "e6")
    save_both(g, f"{step:03d}_right_hex_done", "Right hex done (P11,P1,P4,P2,P3,P5)")
    step += 1

    # Corner iterations: trapez -> hex bottom -> split trapez
    NUM_CORNER_ITERATIONS = 6
    exclude_trap, corner = ["e8", "e10"], "e9"
    for _ in range(NUM_CORNER_ITERATIONS):
        match_trap0 = _find_corner_quad_match(g, p0, corner_node_label=corner, alternate_index=0,
                                             exclude_node=exclude_trap, include_node=None)
        if match_trap0 is None:
            print("No P0 match for bottom-right trapez - end.")
            break
        g.apply_one_at_match(p0, match_trap0)
        save_both(g, f"{step:03d}_p0_corner_bottom-right-of-trapez", "P0 corner trapez")
        step += 1

        match_hex0 = _find_corner_quad_match(g, p0, alternate_index=0, include_node="center", include_node_prefix="V_")
        if match_hex0 is not None:
            g.apply_one_at_match(p0, match_hex0)
            save_both(g, f"{step:03d}_p0_corner_right-hex-bottom", "P0 corner hex bottom")
            step += 1
            match_hex1 = _find_corner_quad_match(g, p1, alternate_index=0, include_node="center", include_node_prefix="V_")
            if match_hex1 is not None:
                g.apply_one_at_match(p1, match_hex1)
                _apply_split_to_quad(g, match_hex1, p1, p3, p4, p5)
                save_both(g, f"{step:03d}_corner_split_right-hex-bottom", "Split right-hex bottom")
                step += 1

        match_trap1 = _find_corner_quad_match(g, p1, corner_node_label=corner, alternate_index=0,
                                              exclude_node=exclude_trap, include_node=None)
        if match_trap1 is not None:
            g.apply_one_at_match(p1, match_trap1)
            _apply_split_to_quad(g, match_trap1, p1, p3, p4, p5)
            save_both(g, f"{step:03d}_corner_split_bottom-right-of-trapez", "Split trapez")
            step += 1

    save_both(g, f"{step:03d}_final_graph", "Final")


if __name__ == "__main__":
    run_derivation()
