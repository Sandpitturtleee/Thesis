import json
from pathlib import Path
import time

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def create_file_path(name):
    base_path = Path(__file__).parent.parent / "data" / "json"
    base_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.json"
    file_path = base_path / file_name
    return file_path


def save_graph_to_json(graph, name):
    graph = {node: [list(edge) for edge in edges] for node, edges in graph.items()}
    file_path = create_file_path(name=name)
    with open(file_path, 'w') as f:
        json.dump(graph, f, indent=2)


def load_graph_from_json(name):
    file_path = create_file_path(name=name)
    with open(file_path, 'r') as f:
        data = json.load(f)
    graph = {node: [tuple(edge) for edge in edges] for node, edges in data.items()}
    return graph


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        # print(f"{func.__name__} executed in {elapsed:.6f} seconds")
        return result, elapsed

    return wrapper


def get_path_and_length(previous, graph, source, target):
    """Reconstruct path from source to target using predecessors and calculate length."""
    path = []
    total_length = 0
    curr = target
    while curr != source and curr is not None:
        pred = previous[curr]
        if pred is None:
            return [], float('inf')
        # Find corresponding weight in adjacency list (graph)
        for neighbor, weight in graph[pred]:
            if neighbor == curr:
                total_length += weight
                break
        path.append((pred, curr))
        curr = pred
    path.reverse()
    return path, total_length


def illustrate_dijkstra_multi_color_legend(graph, previous, source):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors:
            G.add_edge(node, neighbor, weight=weight)
    pos = nx.spring_layout(G, seed=42)

    # Draw full graph in gray
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='gray', alpha=0.3)

    # Prepare for drawing and legend
    nodes = [n for n in G.nodes if n != source]
    colors = cm.get_cmap('tab10', len(nodes))
    legend_entries = []

    for idx, target in enumerate(nodes):
        path_edges, length = get_path_and_length(previous, graph, source, target)
        if not path_edges:
            continue
        color = colors(idx)
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color=[color],
            width=3,
            alpha=0.9,
            label=f"{source}→{target}: {length}"
        )
        legend_entries.append((f"{source}→{target}: {length}", color))

    # Draw only names as labels
    node_labels = {node: node for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_color='black')

    # Draw legend
    handles = [plt.Line2D([0], [0], color=c, lw=3, label=lbl) for lbl, c in legend_entries]
    plt.legend(handles=handles, loc='best')

    plt.title(f"Shortest paths from {source} (legend = path length)")
    plt.show()
