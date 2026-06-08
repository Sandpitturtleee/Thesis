"""
Naive-based Dijkstra Benchmarking Utilities
==========================================

This module provides high-level orchestration for benchmarking the naive-based Dijkstra's algorithm on different classes
of generated graphs. It automates the loading of graph data, running performance experiments, and saving results for further analysis.

Overview
--------

The main purposes of this module:
    - Run tests for all supported graph types (random, worst-case, sparse) for a range of sizes
    - Execute and instrument Dijkstra's shortest path algorithm (naive O(N^2) implementation here
    - Repeat the experiments multiple times for statistical robustness
    - Save benchmark statistics as JSON files for later plotting or analysis

Functions
---------

- run_all_dijkstra_naive(times):
    Orchestrates benchmarking Dijkstra’s algorithm for various graph types and dumps results as JSON.

- dijkstra_naive(graph, start_node):
    Runs Dijkstra’s algorithm WITHOUT a heap (naive O(N^2)), returning distances, predecessors and operation count.

- run_dijkstra_naive(times, graph_type):
    Runs Dijkstra’s algorithm (naive) over a set of problem sizes for the specified type, returns statistics.

Types
-----

- GraphList: List[List[Tuple[int, int]]]
    Adjacency list format: each node index gives a list of (neighbor_index, weight) tuples.

- vertices: List[int]
    List of graph sizes (=number of nodes) used for the experiments.

- count: List[float]
    For each problem size, an averaged operation count (or timing).
"""

from config import (
    RESULTS_DIRECTORY,
    SPARSE,
    STANDARD_NAIVE_SPARSE_FILENAME,
    STANDARD_NAIVE_WORSTCASE_FILENAME,
    WORSTCASE, HALF_EDGES, STANDARD_NAIVE_HALF_EDGES_FILENAME, DENSE, STANDARD_NAIVE_DENSE_FILENAME,
)
from graphs_analysis.src.dijkstra_validation import is_dijkstra_valid
from graphs_analysis.src.helpers import (
    create_frequency,
    load_graph_from_json,
    save_results_to_json,
)


def run_all_dijkstra_naive(times):
    """
    Run the heap-based Dijkstra's algorithm for all configured graph types and save performance results.

    Parameters
    ----------
    times : int
        Number of times to repeat each benchmark for averaging.
    """
    vertices, count = run_dijkstra_naive(times=times, graph_type=SPARSE)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_NAIVE_SPARSE_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_naive(times=times, graph_type=HALF_EDGES)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_NAIVE_HALF_EDGES_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_naive(times=times, graph_type=DENSE)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_NAIVE_DENSE_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_naive(times=times, graph_type=WORSTCASE)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_NAIVE_WORSTCASE_FILENAME,
        vertices=vertices,
        count=count,
    )



def dijkstra_naive(graph, start_node):
    """
    Run Dijkstra's shortest paths algorithm using a naive O(n^2) version (no heap).

    Parameters
    ----------
    graph : List[List[Tuple[int, float]]]
        Adjacency list representation of the graph.
    start_node : int
        Index of source node.

    Returns
    -------
    (distances, previous, operation_count)
        distances : List[float] - Minimum distance from start_node to all nodes.
        previous : List[Optional[int]] - Parent predecessors in the shortest paths.
        operation_count : int - Total number of key comparisons for picking the next node.
    """
    n = len(graph)
    distances = [float("inf")] * n
    previous = [None] * n
    in_heap = [True] * n
    operation_count = 0

    distances[start_node] = 0

    for _ in range(n):
        u = None
        min_dist = float("inf")
        for v in range(n):
            if in_heap[v] and distances[v] < min_dist:
                min_dist = distances[v]
                u = v
            operation_count += 1

        if u is None:
            break
        in_heap[u] = False

        for v, weight in graph[u]:
            if in_heap[v]:
                new_distance = distances[u] + weight
                if new_distance < distances[v]:
                    distances[v] = new_distance
                    previous[v] = u

    return distances, previous, operation_count


def run_dijkstra_naive(times, graph_type):
    """
    Run the naive Dijkstra's algorithm on all available sizes for the given graph type, multiple times.

    Parameters
    ----------
    times : int
        Number of repetitions for the whole set of graph sizes.
    graph_type : str
        Identifies which graph set to load.

    Returns
    -------
    vertices : List[int]
        The graph sizes (number of nodes) used.
    all_results : List[List[float]]
        Nested list with all timing per size, per full run (len = size x times).
    """
    vertices = create_frequency()
    all_results = []

    start_node = 0
    for i in vertices:
        size_results = []
        for run in range(times):
            loaded_graph = load_graph_from_json(name=f"{i}{graph_type}_{run + 1}")
            lengths_naive, previous_naive, elapsed = dijkstra_naive(graph=loaded_graph, start_node=start_node)
            #is_dijkstra_valid(graph=loaded_graph, start_node=start_node, lengths_result=lengths_naive, previous_result=previous_naive)
            size_results.append(elapsed)
        all_results.append(size_results)

    return vertices, all_results
