import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from config import DIJKSTRA_STATS_DIRECTORY
from data_analysis.src.helpers import (
    extract_methods_and_labels,
    read_results_by_vertex,
    read_results_by_vertices,
    read_results_from_json,
)


def plot_all_other():
    plot_vertex_counts(file_name="standard_naive_sparse.json", vertex_number=10)
    plot_vertices_counts(
        file_name="standard_naive_sparse.json", vertices_number=[10, 50, 100]
    )


def plot_vertex_counts(file_name: str, vertex_number: int):
    """
    Plots the count values for a specific number of vertices.

    Parameters
    ----------
    data : dict
        Dictionary with keys 'vertices' (int) and 'count' (list of int).
    """
    data = read_results_by_vertex(file_name=file_name, vertex_number=vertex_number)
    if data is None:
        print("No data available to plot.")
        return

    counts = data["count"]
    trials = list(range(1, len(counts) + 1))

    plt.figure(figsize=(8, 5))
    plt.plot(trials, counts, marker="o", linestyle="-")
    plt.title(f"Results for {data['vertices']} Vertices")
    plt.xlabel("Trial")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_vertices_counts(file_name: str, vertices_number: list):
    """
    Plots the count values for multiple numbers of vertices on one plot.
    """
    data = read_results_by_vertices(file_name, vertices_number)
    if not data:
        print("No data available to plot.")
        return

    plt.figure(figsize=(10, 6))
    for v, counts in data.items():
        trials = list(range(1, len(counts) + 1))
        plt.plot(trials, counts, marker="o", linestyle="-", label=f"{v} vertices")

    plt.title("Results for Multiple Vertex Counts")
    plt.xlabel("Trial")
    plt.ylabel("Count")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def draw_graph_big(graph):
    g = nx.DiGraph()
    g.add_nodes_from(range(len(graph)))
    for node, edges in enumerate(graph):
        for dest, weight in edges:
            g.add_edge(node, dest, weight=weight)
    plt.figure(figsize=(12, 8))
    pos = nx.kamada_kawai_layout(g)
    nx.draw(g, pos, node_size=100, edge_color="gray", alpha=0.6, arrows=False)
    plt.title("Graph", fontsize=20)
    plt.axis("off")
    plt.show()


def draw_graph_small(graph):
    g = nx.DiGraph()
    g.add_nodes_from(range(len(graph)))
    for node, edges in enumerate(graph):
        for dest, weight in edges:
            g.add_edge(node, dest, weight=weight)
    pos = nx.spring_layout(g, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(
        g, pos, with_labels=True, node_color="lightblue", node_size=100, arrowsize=20
    )
    edge_labels = nx.get_edge_attributes(g, "weight")
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_color="red")
    plt.title("Graph")
    plt.show()
