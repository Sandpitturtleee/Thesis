import random
from typing import Dict, List, Tuple

from config import RANDOM, WORST_CASE

"""
Graph Generation Utilities
-------------------------

This module provides functions to generate random weighted graphs (as dictionaries)
and save them in JSON-compatible structures for use in algorithms or testing.

Functions:
----------
- generate_graph_dict: Generate a random undirected weighted graph.
- generate_graph_worst_case_dict: Generate a dense 'worst-case' random graph.
- generate_graphs_dict: Generate and save graphs for a range of sizes.

Dependencies:
-------------
- `config.py` (expects RANDOM and WORST_CASE to be defined, e.g., as '_R' and '_W')
- Data.src.helpers (expects create_frequency and save_graph_to_json_dict)

Types:
------
- GraphDict: type alias for Dict[str, List[Tuple[str, int]]]
"""

from Data.src.helpers import create_frequency, save_graph_to_json_dict

GraphDict = Dict[str, List[Tuple[str, int]]]


def generate_graph_dict(num_vertices: int, min_weight: int = 1) -> GraphDict:
    """
    Generate an undirected random weighted graph represented as a dictionary.

    Each node is labeled as 'V0', 'V1', ..., and a random set of edges with random weights
    are generated for each node.

    Parameters
    ----------
    num_vertices : int
        Number of vertices in the graph.
    min_weight : int, optional
        Minimum weight for any edge (default is 1).

    Returns
    -------
    GraphDict
        Dictionary mapping node labels to lists of (neighbor, weight) tuples.
    """
    max_weight = num_vertices
    nodes = [f"V{i}" for i in range(num_vertices)]
    graph = {node: [] for node in nodes}

    for i, node in enumerate(nodes):
        num_edges = random.randint(1, num_vertices - 1)
        neighbors = set()
        while len(neighbors) < num_edges:
            neighbor = random.choice(nodes)
            if neighbor != node:
                neighbors.add(neighbor)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            if (neighbor, weight) not in graph[node]:
                graph[node].append((neighbor, weight))
            if (node, weight) not in graph[neighbor]:
                graph[neighbor].append((node, weight))

    return graph


def generate_graph_worst_case_dict(num_vertices: int, min_weight: int = 1) -> GraphDict:
    """
    Generate a densely connected 'worst-case' undirected random weighted graph.

    In this context, a 'worst-case' graph is a nearly complete (dense) undirected weighted graph,
    where each node is connected to almost all other nodes, with edge weights generated randomly.

    Parameters
    ----------
    num_vertices : int
        Number of vertices (nodes) in the generated graph. Each node is labeled as 'V0', 'V1', ..., 'V{N-1}'.
    min_weight : int, optional
        Minimum possible weight assigned to any edge (default is 1).
        The actual maximum weight is set to the value of 'num_vertices'.

    Returns
    -------
    GraphDict
        Dictionary mapping node labels to lists of (neighbor, weight) tuples.
    """
    max_weight = num_vertices
    nodes = [f"V{i}" for i in range(num_vertices)]
    graph = {node: [] for node in nodes}

    for i, node in enumerate(nodes):
        num_edges = num_vertices - 1
        neighbors = set()
        while len(neighbors) < num_edges:
            neighbor = random.choice(nodes)
            if neighbor != node:
                neighbors.add(neighbor)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            if (neighbor, weight) not in graph[node]:
                graph[node].append((neighbor, weight))
            if (node, weight) not in graph[neighbor]:
                graph[neighbor].append((node, weight))

    return graph


def generate_graphs_dict() -> None:
    """
    Generate and save random and worst-case graphs for a range of sizes.

    For each value returned by create_frequency(), generates one random graph and
    one dense worst-case graph; both are saved using save_graph_to_json_dict.

    Returns
    -------
    None
    """
    frequency = create_frequency()
    frequency = [10]
    for i in frequency:
        random_graph = generate_graph_dict(num_vertices=i)
        worst_case_graph = generate_graph_worst_case_dict(num_vertices=i)
        save_graph_to_json_dict(graph=random_graph, name=f"{i}{RANDOM}")
        save_graph_to_json_dict(graph=worst_case_graph, name=f"{i}{WORST_CASE}")
