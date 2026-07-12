"""
Shortest Path Reconstruction & Dijkstra Validation Utilities
-----------------------------------------------------------

This module provides tools for reconstructing all shortest paths from a predecessor (previous) array,
computing the shortest paths using NetworkX's Dijkstra, and checking for correctness of two sets of path reconstructions.

Dependencies:
-------------
- networkx

Functions:
----------
- reconstruct_paths_dict: Recover all shortest paths from a 'previous' node array.
- dijkstra_lib: Use networkx to compute the shortest paths and actual paths from a source node.
- compare_dijkstra_result_dicts: Compare two path dictionaries for path-equivalence.
- is_dijkstra_valid: Compare the output of a custom dijkstra to networkx for correctness.

Typings:
--------
- The "graph" argument is an adjacency list: List[List[Tuple[int, int]]] (edges as [to_idx, weight]).
"""

from collections import defaultdict
from typing import Any, Dict, List, Tuple

import networkx as nx


def reconstruct_paths_dict(
    previous: List[Any], start_node: int
) -> Dict[int, List[List[int]]]:
    """
    Reconstruct all shortest paths from 'start_node' to every other node using a 'previous' predecessor array.

    Handles both flat and list-of-lists 'previous' arrays. The result does NOT include the path to start_node itself.

    Parameters
    ----------
    previous : list
        Each entry previous[i] is either None, a single integer predecessor, or a list of predecessor indices.
    start_node : int
        The source node index.

    Returns
    -------
    Dict[int, List[List[int]]]
        Mapping: target node index -> List of all shortest paths (each as list of node indices).
    """
    n = len(previous)
    all_paths = defaultdict(list)

    previous_in = []
    for p in previous:
        if p is None:
            previous_in.append([])
        elif isinstance(p, list):
            previous_in.append(p)
        else:
            previous_in.append([p])

    def build_paths(node: int) -> List[List[int]]:
        if node == start_node:
            return [[start_node]]
        if not previous_in[node]:
            return []
        paths = []
        for pred in previous_in[node]:
            for subpath in build_paths(pred):
                paths.append(subpath + [node])
        return paths

    for target in range(n):
        if target != start_node:
            all_paths[target] = build_paths(target)
    return dict(all_paths)


def dijkstra_lib(
    graph: List[List[List[int]]], start_node: int
) -> Tuple[List[float], Dict[int, List[List[int]]]]:
    """
    Compute the shortest path lengths and enumerate all shortest paths from 'start_node' using networkx's Dijkstra.

    Parameters
    ----------
    graph : List[List[Tuple[int, int]]]
        Adjacency list: graph[u] = [(v, weight), ...]
    start_node : int
        Index of the source node.

    Returns
    -------
    lengths : List[float]
        Minimum distance from source to every node.
    paths : Dict[int, List[List[int]]]
        All shortest paths (lists of node indices) from 'source' to each other node.
    """
    g = nx.DiGraph()
    n = len(graph)
    g.add_nodes_from(range(n))

    for u, neighbors in enumerate(graph):
        for v, weight in neighbors:
            g.add_edge(u, v, weight=weight)

    lengths = [float("inf")] * n
    lengths[start_node] = 0
    sp_length = nx.single_source_dijkstra_path_length(g, start_node, weight="weight")
    for node, length in sp_length.items():
        lengths[node] = length

    paths: Dict[int, List[List[int]]] = dict()
    for target in range(n):
        if target == start_node:
            continue
        try:
            all_paths = list(
                nx.all_shortest_paths(g, start_node, target, weight="weight")
            )
            if all_paths:
                paths[target] = all_paths
        except nx.NetworkXNoPath:
            continue
    return lengths, paths


def compare_dijkstra_results(
    paths1: Dict[int, List[List[int]]],
    paths2: Dict[int, List[List[int]]],
    length1,
    length2,
) -> bool:
    """
    Compare two dictionaries of paths: validates that for each (common) key,
    there is at least one matching path, and that path lengths match.

    Parameters
    ----------
    paths1, paths2 : Dict[int, List[List[int]]]
        Each maps node index to a list of paths (list of lists of node indices).
    length1, length2 : List[float]
        The shortest-path distance arrays to be compared.

    Returns
    -------
    bool
        True if for every shared key, the sets of path tuples have non-empty intersection and all path lengths match.
    """
    if length1 != length2:
        # print(f"Invalid path length: {length1}")
        # print(f"Invalid path length: {length2}")
        return False
    common_keys = set(paths1.keys()) & set(paths2.keys())
    for key in common_keys:
        lists1 = paths1[key]
        lists2 = paths2[key]
        set1 = set(tuple(lst) for lst in lists1)
        set2 = set(tuple(lst) for lst in lists2)
        if not (set1 & set2):
            # print(f"Key {key} has no intersection: {lists1} vs {lists2}")
            return False
    return True


def is_dijkstra_valid(
    graph: List[List[List[int]]],
    start_node: int,
    lengths_result: List[float],
    previous_result: List[Any],
) -> bool:
    """
    Compare your Dijkstra result to networkx for both path lengths and all shortest paths.

    Parameters
    ----------
    graph : List[List[Tuple[int, int]]]
        Adjacency list.
    start_node : int
        Source node index.
    lengths_result : List[float]
        Output distances from your implementation.
    previous_result : List[Any]
        Output predecessor structure.

    Returns
    -------
    bool
        True if both path lengths and all shortest paths match those from networkx.
    """
    lengths_lib, paths_lib = dijkstra_lib(graph=graph, start_node=start_node)
    paths_result = reconstruct_paths_dict(
        previous=previous_result, start_node=start_node
    )
    valid = compare_dijkstra_results(
        paths1=paths_lib,
        paths2=paths_result,
        length1=lengths_lib,
        length2=lengths_result,
    )

    # if not valid:
    #     print(
    #         "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    #     )
    #     print("Mismatch found!")
    #     print("lengths_lib:", lengths_lib)
    #     print("lengths_result:", lengths_result)
    #     print("paths_lib:", paths_lib)
    #     print("paths_result", paths_result)
    #     print(
    #         "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    #     )
    return valid
