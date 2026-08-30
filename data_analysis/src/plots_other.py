"""
Dijkstra Results Plotting Utilities
-----------------------------------

This module provides utility functions for visualizing and reading results from JSON files corresponding to Dijkstra algorithm runs across graphs of various sizes.

Functions:
----------
- plot_all_other: Convenience function to run standard plotting routines for sparse graph result files.
- plot_vertex_counts: Plots the count values for a specific number of vertices from a result file.
- plot_vertices_counts: Plots the count values for multiple numbers of vertices on a single figure.
- draw_graph_big: Visualizes large graphs with a node-link diagram layout.
- draw_graph_small: Visualizes small graphs with labeled nodes and edge weights.
- read_results_by_vertex: Loads and returns result data for a specific vertex number.
- read_results_by_vertices: Loads and returns results for multiple vertex counts as a dictionary.

Types:
------
- None exposed directly; see individual function typing signatures.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import networkx as nx

from config import DATA_DIRECTORY, RESULTS_DIRECTORY_STANDARD_NAIVE, RESULTS_DIRECTORY_STANDARD_HEAP, \
    RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT


def plot_all_other() -> None:
    """
    Runs typical plotting routines for the standard naive Dijkstra results (sparse).
    Shows count plots for 10 vertices and for [10, 50, 100] vertices from the corresponding JSON file.
    """
    # plot_vertex_counts(
    #     directory=RESULTS_DIRECTORY_STANDARD_NAIVE,
    #     file_name="standard_naive_sparse.json",
    #     vertex_number=10,
    # )
    plot_vertices_counts(
        directory=RESULTS_DIRECTORY_STANDARD_NAIVE,
        file_name="standard_naive_sparse.json",
        vertices_number=[50, 70, 100],
    )
    plot_vertices_counts(
        directory=RESULTS_DIRECTORY_STANDARD_HEAP,
        file_name="standard_heap_sparse.json",
        vertices_number=[50, 70, 100],
    )
    # plot_vertices_counts(
    #     directory=RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT,
    #     file_name="quantum_time_limit_sparse.json",
    #     vertices_number=[50, 70, 100],
    # )


def plot_vertex_counts(file_name: str, vertex_number: int, directory: str) -> None:
    """
    Plots the count values for a specific number of vertices.

    Parameters
    ----------
    file_name : str
        Name of the .json result file to read (e.g., "some_results.json")
    vertex_number : int
        Number of vertices to visualize results for.
    directory : str
        Subdirectory under DATA_DIRECTORY where the results file is located.
    """
    data = read_results_by_vertex(
        file_name=file_name, vertex_number=vertex_number, directory=directory
    )
    if data is None:
        print("No data available to plot.")
        return

    counts = data["count"]
    trials = list(range(1, len(counts) + 1))

    plt.figure(figsize=(8, 5))
    plt.plot(trials, counts, marker="o", linestyle="-")
    plt.title(f"Wynik dla grafu o {data['vertices']} wierzchołkach")
    plt.xlabel("Numer grafu")
    plt.ylabel("Liczba operacji")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_vertices_counts(
    file_name: str, vertices_number: List[int], directory: str
) -> None:
    """
    Plots the count values for multiple numbers of vertices on one plot.

    Parameters
    ----------
    file_name : str
        Result file to read
    vertices_number : List[int]
        List of vertex counts to plot
    directory : str
        Subdirectory under DATA_DIRECTORY
    """
    """
    Plots the count values for multiple numbers of vertices on one plot.
    """
    data = read_results_by_vertices(file_name, vertices_number, directory=directory)
    if not data:
        print("No data available to plot.")
        return

    plt.figure(figsize=(10, 6))
    for v, counts in data.items():
        trials = list(range(1, len(counts) + 1))
        plt.plot(trials, counts, marker="o", linestyle="-", label=f"{v} wierzchołków")

    plt.title("Wyniki dla różnej liczby wierzchołków")
    plt.xlabel("Numer grafu")
    plt.ylabel("Liczba operacji")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def draw_graph_big(graph: List[List[List[int]]]) -> None:
    """
    Visualizes a large directed graph (adjacency list format) with a force-directed layout. Node labels hidden.

    Parameters
    ----------
    graph : List[List[Tuple[int, int]]]
        Adjacency list: graph[u] = list of (v, weight)
    """
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


def draw_graph_small(graph: List[List[List[int]]]) -> None:
    """
    Visualizes a small directed graph (adjacency list format) with visible labels and edge weights.

    Parameters
    ----------
    graph : List[List[Tuple[int, int]]]
        Adjacency list: graph[u] = list of (v, weight)
    """
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


def read_results_by_vertex(
    file_name: str, vertex_number: int, directory: str
) -> Optional[Dict[str, Any]]:
    """
    Reads a JSON result file for Dijkstra runs and returns data for a selected vertex number.

    Parameters
    ----------
    file_name : str
        Name of the result JSON file (e.g., "some_results.json")
    vertex_number : int
        Number of vertices to look for in the file.
    directory : str
        Subdirectory under DATA_DIRECTORY

    Returns
    -------
    Optional[dict]
        A dictionary with the matching 'vertices' value and corresponding 'count' list, or None if not found.
    """
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / DATA_DIRECTORY / directory / file_name

    # Read and load the JSON file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Find the index for the given vertex_number
    idx = data["vertices"].index(vertex_number)
    return {"vertices": data["vertices"][idx], "count": data["count"][idx]}


def read_results_by_vertices(
    file_name: str, vertices_number: List[int], directory: str
) -> Dict[int, List[int]]:
    """
    Reads counts for multiple vertex numbers from the given JSON results file.

    Parameters
    ----------
    file_name : str
        Name of the result JSON file (e.g., "some_results.json")
    vertices_number : List[int]
        List of vertex counts to extract.
    directory : str
        Subdirectory under DATA_DIRECTORY

    Returns
    -------
    Dict[int, List[int]]
        Dictionary mapping vertex count to list of counts. Only includes found items.
    """
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / DATA_DIRECTORY / directory / file_name

    with open(file_path, "r") as file:
        data = json.load(file)

    results = {}
    for v in vertices_number:
        if v in data["vertices"]:
            idx = data["vertices"].index(v)
            if "quantum" in file_name:
                results[v] = data["cost"][idx]
            else:
                results[v] = data["count"][idx]
        else:
            print(f"Vertex {v} not found in file.")
    return results
