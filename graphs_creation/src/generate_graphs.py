"""
Graph Generation Utilities (List Adjacency Format)
-------------------------------------------------

This module provides functions to generate random weighted graphs in a **list-based adjacency format**.
It also provides tools for saving such graphs using external helper functions.

Functions:
----------
- generate_graph_random: Generate a random undirected weighted graph as an adjacency list.
- generate_graph_worstcase: Generate a densely connected 'worst-case' random graph as an adjacency list.
- generate_graphs: Generate and save graphs of varying sizes.

Dependencies:
-------------
- config.py (expects RANDOM and WORSTCASE for filename suffixes)
- graphs_creation.src.helpers (expects create_frequency and save_graph_to_json)

Types:
------
- GraphList: type alias for List[List[Tuple[int, int]]]
"""

import random
from typing import List, Tuple

from config import RANDOM, WORSTCASE
from graphs_creation.src.helpers import create_frequency, save_graph_to_json

GraphList = List[List[Tuple[int, int]]]


def generate_graphs() -> None:
    """
    Generate and save random and dense worst-case graphs for several sizes.

    For each value returned by create_frequency(), generates one random and one densely connected
    (worst-case) graph and saves them using save_graph_to_json_list().

    Returns
    -------
    None
    """
    frequency = create_frequency()
    for i in frequency:
        random_graph = generate_graph_random(num_vertices=i)
        worst_case_graph = generate_graph_worstcase(num_vertices=i)
        save_graph_to_json(graph=random_graph, name=f"{i}{RANDOM}")
        save_graph_to_json(graph=worst_case_graph, name=f"{i}{WORSTCASE}")


def generate_graph_random(num_vertices: int, min_weight: int = 1) -> GraphList:
    """
    Generate an undirected random weighted graph as an adjacency list.

    Each vertex will have a random set of neighbors and edge weights.
    The adjacency list ensures bidirectional edges and no self-loops.

    Parameters
    ----------
    num_vertices : int
        Number of vertices in the graph.
    min_weight : int, optional
        The minimum weight assigned to any edge (default is 1).

    Returns
    -------
    GraphList
        A list of adjacency lists, each containing (neighbor_index, weight) tuples.
    """
    max_weight = num_vertices
    graph = [[] for _ in range(num_vertices)]

    for i in range(num_vertices):
        num_edges = random.randint(1, num_vertices - 1)
        neighbors = set()
        while len(neighbors) < num_edges:
            neighbor = random.randint(0, num_vertices - 1)
            if neighbor != i:
                neighbors.add(neighbor)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            if neighbor not in [v for v, w in graph[i]]:
                graph[i].append((neighbor, weight))
            if i not in [v for v, w in graph[neighbor]]:
                graph[neighbor].append((i, weight))
    return graph


def generate_graph_worstcase(num_vertices: int, min_weight: int = 1) -> GraphList:
    """
    Generate a dense (worst-case) undirected random weighted graph as an adjacency list.

    In this context, 'worst-case' means the graph is as dense as possible: each vertex is
    connected to every other vertex (i.e., the graph is complete). The result is presented
    as a list of adjacency lists, where each adjacency list contains tuples representing
    (neighbor_index, edge_weight).

    Parameters
    ----------
    num_vertices : int
        Number of vertices in the graph.
        Each vertex will be indexed from 0 to (num_vertices - 1).
    min_weight : int, optional
        Minimum possible edge weight (default is 1).
        The effective maximum edge weight is set to num_vertices.

    Returns
    -------
    GraphList
        A list of adjacency lists, each containing (neighbor_index, weight) tuples.
    """
    max_weight = num_vertices
    graph = [[] for _ in range(num_vertices)]
    for i in range(num_vertices):
        neighbors = set(j for j in range(num_vertices) if j != i)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            if neighbor not in [v for v, w in graph[i]]:
                graph[i].append((neighbor, weight))
            if i not in [v for v, w in graph[neighbor]]:
                graph[neighbor].append((i, weight))
    return graph
