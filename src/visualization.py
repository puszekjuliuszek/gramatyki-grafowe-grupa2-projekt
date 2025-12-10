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
            node_colors.append('red')
            node_sizes.append(200)
            if node.hyperref:
                labels[label] = node.hyperref.hypertag
            else:
                labels[label] = label.split('_')[0]
        else:
            node_colors.append('lightblue')
            node_sizes.append(500)
            labels[label] = label
            
            if node.hanging:
                node_colors[-1] = 'yellow'
    
    # Draw grap
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
        plt.scatter([], [], c='lightblue', s=100, label='Node'),
        plt.scatter([], [], c='yellow', s=100, label='Hanging node'),
        plt.scatter([], [], c='red', s=50, label='Hyperedge'),
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.title(f"Graph: {len(graph.nodes)} nodes, {len(graph.hyperedges)} hyperedges")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    
    print(f"Saved graph to: {filename}")
