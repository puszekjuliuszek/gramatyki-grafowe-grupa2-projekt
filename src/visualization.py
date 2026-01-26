"""
Module for graph visualization.
"""

import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import networkx as nx
from graph import Graph


def draw_edges_only(graph: Graph, filename: str, show_labels: bool = True) -> None:
    """
    Draws only boundary and internal E edges (no Q/S hyperedges).
    Shows the mesh skeleton: regular nodes and line segments for each E hyperedge.
    Boundary edges (b=1) in one color, internal (b=0) in another.
    """
    fig, ax = plt.subplots(figsize=(15, 15))
    pos = {n.label: (n.x, n.y) for n in graph.nodes}
    boundary_edges = []
    internal_edges = []
    for edge in graph.hyperedges:
        if edge.hypertag != "E" or len(edge.nodes) != 2:
            continue
        n1, n2 = edge.nodes
        seg = [(n1.x, n1.y), (n2.x, n2.y)]
        if getattr(edge, "b", 0) == 1:
            boundary_edges.append(seg)
        else:
            internal_edges.append(seg)
    for seg in boundary_edges:
        ax.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]], "g-", linewidth=2, zorder=1)
    for seg in internal_edges:
        ax.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]], "b-", linewidth=1.2, zorder=1)
    xs = [n.x for n in graph.nodes]
    ys = [n.y for n in graph.nodes]
    ax.scatter(xs, ys, c="lightblue", s=80, zorder=2, edgecolors="black", linewidths=0.8)
    if show_labels:
        for n in graph.nodes:
            ax.annotate(n.label, (n.x, n.y), fontsize=7, ha="center", va="bottom", zorder=3)
    ax.set_aspect("equal")
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color="green", linewidth=2, label="Boundary (b=1)"),
            plt.Line2D([0], [0], color="blue", linewidth=1.2, label="Internal (b=0)"),
        ],
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
    )
    ax.set_title(f"Edges only: {len(graph.nodes)} nodes, {len(boundary_edges)} boundary, {len(internal_edges)} internal")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def draw(graph: Graph, filename: str) -> None:
    """
    Draws the graph and saves it to a file.
    
    Args:
        graph: Graph to draw
        filename: Path to output file (e.g., "draw/test1.png")
    """
    fig, ax = plt.subplots(figsize=(15, 15))
    
    pos = {}
    node_colors = []
    node_sizes = []
    labels = {}
    
    for label, data in graph._graph.nodes(data=True):
        node = data['node']
        pos[label] = (node.x, node.y)
        
        if data.get('is_hyper', False):
            node_sizes.append(400)
            if node.hyperref:
                if node.hyperref.b == 1:
                    node_colors.append('green')
                else:
                    node_colors.append('red')
                labels[label] = f"{node.hyperref.hypertag}:{node.hyperref.r}"
            else:
                labels[label] = label.split('_')[0]
        else:
            node_colors.append('lightblue')
            node_sizes.append(600)
            labels[label] = label
    
    nx.draw(
        graph._graph,
        pos=pos,
        ax=ax,
        with_labels=True,
        labels=labels,
        node_color=node_colors,
        node_size=node_sizes,
        font_size=8,
        font_weight='bold',
        edge_color='gray',
        width=1.5
    )
    
    legend_elements = [
        plt.scatter([], [], c='lightblue', s=50, label='Node'),
        plt.scatter([], [], c='red', s=50, label='Hyperedge'),
        plt.scatter([], [], c='green', s=50, label='Boundary edge')
    ]
    ax.legend(
        handles=legend_elements,
        loc='upper left',
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0.0
    )
    
    plt.title(f"Graph: {len(graph.nodes)} nodes, {len(graph.hyperedges)} hyperedges")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    
    print(f"Saved graph to: {filename}")
