"""
Module for graph visualization.
"""

import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import networkx as nx
from graph import Graph


def draw(graph: Graph, filename: str) -> None:
    """
    Draws the graph and saves it to a file.
    
    Args:
        graph: Graph to draw
        filename: Path to output file (e.g., "draw/test1.png")
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
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
                    # print(node) removed
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
    plt.savefig(filename, dpi=150)
    plt.close()
    
    print(f"Saved graph to: {filename}")

def draw_clean(graph: Graph, filename: str) -> None:
    """
    Draws only the mesh structure (nodes and E-related edges), hiding hyperedges.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    mesh_graph = nx.Graph()
    pos = {}
    labels = {}
    
    # 1. Add all regular nodes
    for node in graph.nodes:
        # Check if node is truly a mesh node (not a hypernode)
        # In this implementation, graph.nodes property returns self._nodes.values()
        # which are regular nodes. Hypernodes are in self._hyperedges.
        # But wait, graph.add_node adds to _nodes. graph.add_edge adds hyper_node to _graph but NOT to _nodes if check_nodes=False?
        # Let's verify graph.py:
        # _nodes stores "regular" nodes.
        # _hyperedges stores "hyper" edges.
        # So iterating graph.nodes gives us the mesh vertices.
        mesh_graph.add_node(node.label)
        pos[node.label] = (node.x, node.y)
        labels[node.label] = node.label.split('_')[0] # Simplified label

    # 2. Add edges derived from E hyperedges
    # An E hyperedge connects 2 nodes. We draw a line between them.
    for edge in graph.hyperedges:
        if edge.hypertag == "E":
            if len(edge.nodes) == 2:
                u, v = edge.nodes
                mesh_graph.add_edge(u.label, v.label, b=edge.b, r=edge.r)
    
    # Drawing
    edge_colors = []
    for u, v, data in mesh_graph.edges(data=True):
        if data.get('r') == 1:
            edge_colors.append('red') # Marked for breaking
        elif data.get('b') == 1:
            edge_colors.append('green') # Boundary
        else:
            edge_colors.append('black') # Internal
            
    nx.draw(
        mesh_graph,
        pos=pos,
        ax=ax,
        with_labels=True,
        labels=labels,
        node_color='lightblue',
        node_size=500,
        font_size=8,
        font_weight='bold',
        edge_color=edge_colors,
        width=2.0
    )
    
    legend_elements = [
        plt.scatter([], [], c='lightblue', s=50, label='Node'),
        plt.Line2D([0], [0], color='black', lw=2, label='Internal edge'),
        plt.Line2D([0], [0], color='green', lw=2, label='Boundary edge'),
        plt.Line2D([0], [0], color='red', lw=2, label='Marked for breaking (r=1)')
    ]
    ax.legend(
        handles=legend_elements,
        loc='upper left',
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0.0
    )
    
    plt.title(f"Mesh: {len(mesh_graph.nodes)} vertices, {len(mesh_graph.edges)} edges")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    
    print(f"Saved clean graph to: {filename}")
