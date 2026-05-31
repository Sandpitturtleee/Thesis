"""
Heap-based Dijkstra Benchmarking Utilities
==========================================

This module provides high-level orchestration for benchmarking the heap-based Dijkstra's algorithm
on various classes of generated graphs. It automates loading graph data, running timed/performance
experiments, and saving results for later analysis.

Overview
--------

This module comprises the following main parts:

    - Running experiments for all major graph types (random, worst-case, sparse)
    - Executing and instrumenting Dijkstra's shortest path algorithm using a MinHeap
    - Automating repeated runs for statistical averaging per graph size
    - Saving resulting benchmark statistics to disk for later analysis

Functions
---------

- run_all_dijkstra_heap(times):
    Orchestrates benchmarking Dijkstra’s algorithm for various graph types and saves results as JSON.
- dijkstra_heap(graph, start_node):
    Runs Dijkstra’s algorithm with a MinHeap and returns distances, predecessor info, and heap operation count.
- run_dijkstra_heap(times, graph_type):
    Runs the heap-based Dijkstra’s algorithm for a variety of graph sizes of a given type; averages performance metrics.

Types
-----

- GraphList: List[List[Tuple[int, int]]]
    Adjacency list representation; each node maps to list of (neighbor_index, weight) pairs.
- vertices: List[int]
    List of graph sizes (node counts) under test.
- count: List[float]
    Per-graph size list of averaged operation counts or timings.
"""

from config import (
    RANDOM,
    RESULTS_DIRECTORY,
    SPARSE,
    STANDARD_HEAP_RANDOM_FILENAME,
    STANDARD_HEAP_SPARSE_FILENAME,
    STANDARD_HEAP_WORSTCASE_FILENAME,
    WORSTCASE,
)
from graphs_analysis.src.helpers import (
    create_frequency,
    load_graph_from_json,
    save_results_to_json,
)
from graphs_analysis.src.standard.heap import MinHeap


def run_all_dijkstra_heap(times):
    """
    Run the heap-based Dijkstra's algorithm for all configured graph types and save performance results.

    Parameters
    ----------
    times : int
        Number of times to repeat each benchmark for averaging.
    """
    vertices, count = run_dijkstra_heap(times=times, graph_type=RANDOM)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_HEAP_RANDOM_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_heap(times=times, graph_type=WORSTCASE)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_HEAP_WORSTCASE_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_heap(times=times, graph_type=SPARSE)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_HEAP_SPARSE_FILENAME,
        vertices=vertices,
        count=count,
    )


def dijkstra_heap(graph, start_node):
    """
    Run Dijkstra's shortest paths algorithm using a MinHeap, instrumented for performance.

    Parameters
    ----------
    graph : GraphList
        Adjacency list representation of the graph.
    start_node : int
        Index of source node.

    Returns
    -------
    (distances, previous, operation_count)
        distances : List[float] - Minimum distance from start_node to all nodes.
        previous : List[Optional[int]] - Parent predecessors in the shortest paths.
        operation_count : int - Total number of heap operations (e.g., comparisons), depending on heap implementation.
    """
    n = len(graph)
    distances = [float("inf")] * n
    previous = [None] * n
    in_heap = [True] * n

    heap = MinHeap()
    for node in range(n):
        heap.push(float("inf"), node)
    heap.decrease_key(start_node, 0)
    distances[start_node] = 0

    while not heap.is_empty():
        dist_u, u = heap.pop()
        in_heap[u] = False

        for v, weight in graph[u]:
            if in_heap[v]:
                new_distance = distances[u] + weight
                if new_distance < distances[v]:
                    distances[v] = new_distance
                    previous[v] = u
                    heap.decrease_key(v, new_distance)
    return distances, previous, heap.total()


def run_dijkstra_heap(times, graph_type):
    """
    Run heap-based Dijkstra's algorithm on all available sizes for the given graph type, multiple times.

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

    for i in vertices:
        size_results = []
        for run in range(times):
            loaded_graph = load_graph_from_json(name=f"{i}{graph_type}_{run + 1}")
            _, _, elapsed = dijkstra_heap(graph=loaded_graph, start_node=0)
            size_results.append(elapsed)
        all_results.append(size_results)

    return vertices, all_results
