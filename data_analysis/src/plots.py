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


def stats_plots_mean_heap():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)

    plt.figure(figsize=(10, 6))
    for method in heap_methods:
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["mean"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method])

    # Add n*n*lnn curve
    x_all = sorted(
        set(int(size) for method in heap_methods for size in data[method].keys())
    )
    y_lognn = [2.55 * n * n * np.log2(n) for n in x_all]
    plt.plot(x_all, y_lognn, label=r"$n^2 \log n$", linestyle="--", color="black")

    plt.title("Heap - mean")
    plt.xlabel("Vertices")
    plt.ylabel("Mean")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def stats_plots_mean_naive():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)

    plt.figure(figsize=(10, 6))
    for method in naive_methods:
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["mean"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method])

    # Add n^2 curve
    x_all_naive = sorted(
        set(int(size) for method in naive_methods for size in data[method].keys())
    )
    y_n2 = [n * n for n in x_all_naive]
    plt.plot(x_all_naive, y_n2, label=r"$n^2$", linestyle="--", color="black")

    plt.title("Naive - mean")
    plt.xlabel("Vertices")
    plt.ylabel("Mean")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def stats_plots_mean_combined():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)
    plt.figure(figsize=(12, 7))

    # Get color shades by sampling from the colormaps
    blues = cm.get_cmap("Blues")
    reds = cm.get_cmap("Reds")
    blue_shades = [
        blues(0.5 + 0.5 * i / max(len(heap_methods) - 1, 1))
        for i in range(len(heap_methods))
    ]
    red_shades = [
        reds(0.5 + 0.5 * i / max(len(naive_methods) - 1, 1))
        for i in range(len(naive_methods))
    ]

    # Plot Heap methods (shades of blue)
    for i, method in enumerate(heap_methods):
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["mean"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method], color=blue_shades[i])

    # Plot Naive methods (shades of red)
    for i, method in enumerate(naive_methods):
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["mean"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method], color=red_shades[i])

    plt.title("Heap vs Naive - mean")
    plt.xlabel("Vertices")
    plt.ylabel("Mean")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def stats_plots_median_heap():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)
    plt.figure(figsize=(10, 6))

    for method in heap_methods:
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["median"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method])

    plt.title("Heap - median")
    plt.xlabel("Vertices")
    plt.ylabel("Median")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def stats_plots_median_naive():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)

    plt.figure(figsize=(10, 6))
    for method in naive_methods:
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["median"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method])

    plt.title("Naive - median")
    plt.xlabel("Vertices")
    plt.ylabel("Median")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def stats_plots_median_combined():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)
    plt.figure(figsize=(12, 7))

    blues = cm.get_cmap("Blues")
    reds = cm.get_cmap("Reds")
    blue_shades = [
        blues(0.5 + 0.5 * i / max(len(heap_methods) - 1, 1))
        for i in range(len(heap_methods))
    ]
    red_shades = [
        reds(0.5 + 0.5 * i / max(len(naive_methods) - 1, 1))
        for i in range(len(naive_methods))
    ]

    # Plot Heap methods (shades of blue)
    for i, method in enumerate(heap_methods):
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["median"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method], color=blue_shades[i])

    # Plot Naive methods (shades of red)
    for i, method in enumerate(naive_methods):
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["median"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method], color=red_shades[i])

    plt.title("Heap vs Naive - median")
    plt.xlabel("Vertices")
    plt.ylabel("Median")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def stats_plots_std_heap():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)
    plt.figure(figsize=(8, 5))
    for method in heap_methods:
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["std"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method])
    plt.title("Heap - std")
    plt.xlabel("Vertices")
    plt.ylabel("Std")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def stats_plots_std_naive():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)

    plt.figure(figsize=(8, 5))
    for method in naive_methods:
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["std"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method])
    plt.title("Naive - std")
    plt.xlabel("Vertices")
    plt.ylabel("Std")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def stats_plots_std_combined():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    heap_methods, naive_methods, method_labels = extract_methods_and_labels(data)
    plt.figure(figsize=(10, 6))

    blues = cm.get_cmap("Blues")
    reds = cm.get_cmap("Reds")
    blue_shades = [
        blues(0.5 + 0.5 * i / max(len(heap_methods) - 1, 1))
        for i in range(len(heap_methods))
    ]
    red_shades = [
        reds(0.5 + 0.5 * i / max(len(naive_methods) - 1, 1))
        for i in range(len(naive_methods))
    ]

    # Plot Heap methods (different blue shades)
    for i, method in enumerate(heap_methods):
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["std"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method], color=blue_shades[i])

    # Plot Naive methods (different red shades)
    for i, method in enumerate(naive_methods):
        records = data[method]
        x = sorted(int(size) for size in records.keys())
        y = [records[str(size)]["std"] for size in x]
        plt.plot(x, y, marker="o", label=method_labels[method], color=red_shades[i])

    plt.title("Heap vs Naive - std")
    plt.xlabel("Vertices")
    plt.ylabel("Std")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_dijkstra_counts(results_dict):
    """
    Plot Dijkstra's algorithm operation counts for different graph types.

    Parameters
    ----------
    results_dict : dict
        Dictionary loaded from your JSON results.
        Keys are filenames (e.g., 'standard_grid.json'), and values are dicts containing:
            - 'vertices': list of number of vertices in the graph
            - 'count': list of operation counts for each graph size
    Returns
    -------
    None

    Displays
    -------
    A matplotlib line plot comparing the operation counts.
    """
    plt.figure(figsize=(10, 7))

    for key, data in results_dict.items():
        label = key.replace("standard_", "").replace(".json", "").capitalize()
        plt.plot(data["vertices"], data["count"], marker="o", label=label)

    plt.xlabel("Graph Size (vertices)")
    plt.ylabel("Operation Count")
    plt.title("Dijkstra's Algorithm Operation Count on Different Graph Types")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


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
