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

import heapq
import math

from config import (
    DENSE,
    GRAPH_RUNS,
    HALF_EDGES,
    RESULTS_DIRECTORY_STANDARD_HEAP,
    RESULTS_DIRECTORY_STANDARD_NAIVE,
    SPARSE,
    SPECIAL_CASE,
    STANDARD_HEAP_DENSE_FILENAME,
    STANDARD_HEAP_HALF_EDGES_FILENAME,
    STANDARD_HEAP_SPARSE_FILENAME,
    STANDARD_HEAP_SPECIAL_CASE_FILENAME,
)
from graphs_analysis.src.helpers import (
    create_frequency,
    load_graph_from_json,
    save_results_to_json,
)
from graphs_analysis.src.standard.heap import CountingHeap


def run_all_dijkstra_heap():
    """
    Run the heap-based Dijkstra's algorithm for all configured graph types and save performance results.
    """
    times = GRAPH_RUNS
    directory = RESULTS_DIRECTORY_STANDARD_HEAP
    vertices, count = run_dijkstra_heap(times=times, graph_type=SPARSE)
    save_results_to_json(
        directory=directory,
        name=STANDARD_HEAP_SPARSE_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_heap(times=times, graph_type=HALF_EDGES)
    save_results_to_json(
        directory=directory,
        name=STANDARD_HEAP_HALF_EDGES_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_heap(times=times, graph_type=DENSE)
    save_results_to_json(
        directory=directory,
        name=STANDARD_HEAP_DENSE_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_heap(times=times, graph_type=SPECIAL_CASE)
    save_results_to_json(
        directory=directory,
        name=STANDARD_HEAP_SPECIAL_CASE_FILENAME,
        vertices=vertices,
        count=count,
    )


def dijkstra_log(graph, start_node):
    n = len(graph)
    distances = [float("inf")] * n
    previous = [None] * n
    in_heap = [True] * n

    Q = []
    total_log_work = 0

    # O(V)
    for node in range(n):
        dist = 0 if node == start_node else float("inf")
        heapq.heappush(Q, (dist, node))
        total_log_work += 1  # Log work for push
        distances[node] = dist

    while Q:
        # O(logV)
        heap_size = len(Q)
        dist_u, u = heapq.heappop(Q)
        total_log_work += math.log2(heap_size)  # Log work for pop

        # Outdated entry check (lazy deletion)
        if dist_u > distances[u]:
            continue
        in_heap[u] = False
        for v, weight in graph[u]:
            if in_heap[v]:
                alt = distances[u] + weight
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
                    # O(logV): push new possible distance
                    heapq.heappush(Q, (alt, v))
                    total_log_work += math.log2(len(Q))  # Log work for push

    return distances, previous, total_log_work


def dijkstra_heap(graph, start_node):
    n = len(graph)
    distances = [float("inf")] * n
    previous = [None] * n
    in_heap = [True] * n

    heap = CountingHeap()

    for node in range(n):
        dist = 0 if node == start_node else float("inf")
        heap.push((dist, node))
        distances[node] = dist

    while heap.data:
        result = heap.pop()
        if result is None:
            break
        dist_u, u = result

        if dist_u > distances[u]:
            continue
        in_heap[u] = False
        for v, weight in graph[u]:
            if in_heap[v]:
                alt = distances[u] + weight
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
                    heap.push((alt, v))

    return distances, previous, heap.total_work()


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

    start_node = 0
    for i in vertices:
        size_results = []
        for run in range(times):
            loaded_graph = load_graph_from_json(name=f"{i}{graph_type}_{run + 1}")
            lengths_heap, previous_heap, elapsed = dijkstra_heap(
                graph=loaded_graph, start_node=start_node
            )
            # is_dijkstra_valid(graph=loaded_graph, start_node=start_node, lengths_result=lengths_heap, previous_result=previous_heap)
            size_results.append(elapsed)
        all_results.append(size_results)

    return vertices, all_results
