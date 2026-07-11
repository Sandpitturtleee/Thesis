"""
Graph Generation Utilities (List Adjacency Format)
--------------------------------------------------

This module provides functions to generate random weighted graphs
in a **list-based adjacency format**. It also provides tools for saving
such graphs using external helper functions.

Functions:
----------
- generate_graph_sparse:      Generate a sparse graph with `num_edges = num_vertices`
- generate_graph_half_edges:  Generate a graph with half the possible simple edges
- generate_graph_dense:       Generate a complete (dense) random-weighted graph
- generate_graph_worstcase:   Generate a specifically structured 'worst-case' complete graph
- generate_graphs:            Generate and save graphs of various sizes/batches

Dependencies:
-------------
- config.py          (expects: SPARSE, WORSTCASE, HALF_EDGES, DENSE constants)
- graphs_creation.src.helpers
    - create_frequency
    - save_graph_to_json

Types:
------
- GraphList: List[List[Tuple[int, int]]]
"""

import random
from typing import List, Set, Tuple

from config import DENSE, HALF_EDGES, SPARSE, WORSTCASE
from graphs_creation.src.helpers import create_frequency, save_graph_to_json

GraphList = List[List[Tuple[int, int]]]


def generate_graphs(times: int = 1) -> None:
    """
    Generate and save random, dense worst-case, half-edge, and sparse graphs for several sizes.

    For each value returned by create_frequency(), generates 'times' number of:
         - sparse
         - half-edges (half density)
         - dense (complete)
         - worst-case (specific structure)
    graphs, and saves them with appropriate file names.

    Parameters
    ----------
    times : int
        Number of times to generate and save each graph type per frequency.

    Returns
    -------
    None
    """
    frequency = create_frequency()
    for n in frequency:
        for run in range(times):
            max_weight = n * n  # You may adjust this as needed per experiment

            sparse_graph = generate_graph_sparse(num_vertices=n, max_weight=max_weight)
            half_edges_graph = generate_graph_half_edges(
                num_vertices=n, max_weight=max_weight
            )
            dense_graph = generate_graph_dense(num_vertices=n, max_weight=max_weight)
            worst_case_graph = generate_graph_worstcase(num_vertices=n)

            save_graph_to_json(sparse_graph, name=f"{n}{SPARSE}_{run + 1}")
            save_graph_to_json(half_edges_graph, name=f"{n}{HALF_EDGES}_{run + 1}")
            save_graph_to_json(dense_graph, name=f"{n}{DENSE}_{run + 1}")
            save_graph_to_json(worst_case_graph, name=f"{n}{WORSTCASE}_{run + 1}")


def generate_graph_sparse(
    num_vertices: int, max_weight: int, min_weight: int = 1
) -> GraphList:
    """
    Generate an undirected sparse random weighted graph as an adjacency list.

    The total number of edges will be equal to the number of vertices.

    Parameters
    ----------
    num_vertices : int
        Number of vertices in the graph.
    max_weight : int
        Maximum possible edge weight assigned to any edge.
    min_weight : int, optional
        Minimum weight assigned to any edge (default is 1).

    Returns
    -------
    GraphList
        List of adjacency lists, each containing (neighbor_index, weight) tuples.
    """
    if num_vertices < 2:
        return [[] for _ in range(num_vertices)]

    graph = [[] for _ in range(num_vertices)]
    existing_edges: Set[Tuple[int, int]] = set()
    max_possible = num_vertices * (num_vertices - 1) // 2

    num_edges = min(num_vertices, max_possible)  # Simple graph has at most C(n,2) edges

    while len(existing_edges) < num_edges:
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u == v:
            continue
        a, b = min(u, v), max(u, v)
        if (a, b) in existing_edges:
            continue
        weight = random.randint(min_weight, max_weight)
        graph[a].append((b, weight))
        graph[b].append((a, weight))
        existing_edges.add((a, b))
    return graph


def generate_graph_half_edges(
    num_vertices: int, max_weight: int, min_weight: int = 1
) -> GraphList:
    """
    Generate an undirected random weighted graph with half of the possible edges.

    Parameters
    ----------
    num_vertices : int
        Number of vertices in the graph.
    max_weight : int
        Maximum possible weight for any edge.
    min_weight : int, optional
        Minimum possible edge weight (default is 1).

    Returns
    -------
    GraphList
        List of adjacency lists, each (neighbor_index, weight) tuples.
    """
    if num_vertices < 2:
        return [[] for _ in range(num_vertices)]

    graph = [[] for _ in range(num_vertices)]
    existing_edges: Set[Tuple[int, int]] = set()

    max_possible = num_vertices * (num_vertices - 1) // 2
    num_edges = max_possible // 2

    while len(existing_edges) < num_edges:
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u == v:
            continue
        a, b = min(u, v), max(u, v)
        if (a, b) in existing_edges:
            continue
        weight = random.randint(min_weight, max_weight)
        graph[a].append((b, weight))
        graph[b].append((a, weight))
        existing_edges.add((a, b))
    return graph


def generate_graph_dense(
    num_vertices: int, max_weight: int, min_weight: int = 1
) -> GraphList:
    """
    Generate a complete (dense) undirected random weighted graph as an adjacency list.

    Each vertex is connected to every other vertex (no self-loops or duplicate edges).

    Parameters
    ----------
    num_vertices : int
        Number of vertices in the graph.
    max_weight : int
        Maximum possible edge weight.
    min_weight : int, optional
        Minimum possible edge weight (default is 1).

    Returns
    -------
    GraphList
        List of adjacency lists, each (neighbor_index, weight) tuples.
    """
    graph = [[] for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            weight = random.randint(min_weight, max_weight)
            graph[i].append((j, weight))
            graph[j].append((i, weight))
    return graph


def generate_graph_worstcase(num_vertices: int) -> GraphList:
    """
    Generate a specifically structured 'worst-case' complete graph for Dijkstra's algorithm.

    For each vertex i and j > i:
        - Edge (i, j) has weight 1 if j == i + 1
        - Edge (i, j) has weight 2*(num_vertices - i) if j > i + 1

    Parameters
    ----------
    num_vertices : int
        Number of vertices in the graph.

    Returns
    -------
    GraphList
        List of adjacency lists, each (neighbor_index, weight) tuples.
    """
    graph = [[] for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if j == i + 1:
                weight = 1
            else:
                weight = 2 * (num_vertices - i)
            graph[i].append((j, weight))
            graph[j].append((i, weight))
    return graph
