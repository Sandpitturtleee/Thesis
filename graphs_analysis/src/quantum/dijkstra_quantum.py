"""
Quantum Dijkstra Batch Runner
----------------------------

This module provides batch experiment utilities for benchmarking quantum-inspired variants of Dijkstra's shortest path algorithm
on multiple classes of input graphs. It systematically runs quantum Dijkstra variants with various options (resource/time limits,
repeatability, etc), and records comparative performance, mismatch, and validity data in JSON files.

Functions:
----------
- run_all_quantum: Run all quantum Dijkstra experiment variants and record results.
- run_all_dijkstra_quantum: Run Dijkstra on all main graph classes (sparse, dense, etc.) and save each variant.
- run_dijkstra_quantum: Run Dijkstra for a range of graph sizes, recording runtimes & correctness stats.
- dijkstra_quantum: Execute quantum-inspired Dijkstra's algorithm (min search via quantum minimum) on a single graph.

Types:
------
- AdjacencyList: type alias for List[List[Tuple[int, int]]] (each node's outgoing edges: [(neighbor_idx, weight), ...])
"""

from typing import Any, Dict, List, Tuple

from config import (DENSE, GRAPH_RUNS, HALF_EDGES,
                    QUANTUM_NO_TIME_LIMIT_FILENAMES,
                    QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_FILENAMES,
                    QUANTUM_SAME_GRAPH_TIME_LIMIT_FILENAMES,
                    QUANTUM_TIME_LIMIT_FILENAMES,
                    RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT, SPARSE, SPECIAL_CASE)
from graphs_analysis.src.dijkstra_validation import is_dijkstra_valid
from graphs_analysis.src.helpers import (create_frequency,
                                         load_graph_from_json,
                                         save_results_to_json_quantum)
from graphs_analysis.src.quantum.quantum_minimum import (
    find_min, pad_to_power_of_two_with_indices)

AdjacencyList = List[List[Tuple[int, int]]]


def run_all_quantum():
    """
    Runs all quantum Dijkstra experiment variants and saves each result.

    Four scenarios are executed: {time-limited, unlimited} × {same-graph, different-graph}.
    """
    run_all_dijkstra_quantum(
        time_limit=1,
        same_graph=0,
        result_directory=RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT,
        result_file_names=QUANTUM_TIME_LIMIT_FILENAMES,
    )
    run_all_dijkstra_quantum(
        time_limit=0,
        same_graph=0,
        result_directory=RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
        result_file_names=QUANTUM_NO_TIME_LIMIT_FILENAMES,
    )

    run_all_dijkstra_quantum(
        time_limit=1,
        same_graph=1,
        result_directory=RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT,
        result_file_names=QUANTUM_SAME_GRAPH_TIME_LIMIT_FILENAMES,
    )
    run_all_dijkstra_quantum(
        time_limit=0,
        same_graph=1,
        result_directory=RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT,
        result_file_names=QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_FILENAMES,
    )


def run_all_dijkstra_quantum(
    time_limit: int,
    same_graph: int,
    result_directory: str,
    result_file_names: List[str],
):
    """
    Run the quantum-based Dijkstra's algorithm for all configured graph types and save performance results.

    Parameters
    ----------
    time_limit : int
        If 1, applies time limit to quantum min search. If 0, unlimited (benchmark mode).
    same_graph : int
        If 1, all repetitions use the same graph instance; if 0, new graph per run.
    result_directory : str
        Directory for saving the results JSON.
    result_file_names : list of str
        Four JSON file names [SPARSE, HALF_EDGES, DENSE, SPECIAL_CASE].
    """
    times = GRAPH_RUNS
    print("Running Dijkstra's algorithm SPARSE")
    results = run_dijkstra_quantum(
        times=times, graph_type=SPARSE, time_limit=time_limit, same_graph=same_graph
    )
    save_results_to_json_quantum(
        directory=result_directory, name=result_file_names[0], results=results
    )
    print("Running Dijkstra's algorithm HALF_EDGES")
    results = run_dijkstra_quantum(
        times=times, graph_type=HALF_EDGES, time_limit=time_limit, same_graph=same_graph
    )
    save_results_to_json_quantum(
        directory=result_directory,
        name=result_file_names[1],
        results=results,
    )
    print("Running Dijkstra's algorithm DENSE")
    results = run_dijkstra_quantum(
        times=times, graph_type=DENSE, time_limit=time_limit, same_graph=same_graph
    )
    save_results_to_json_quantum(
        directory=result_directory, name=result_file_names[2], results=results
    )
    print("Running Dijkstra's algorithm SPECIAL_CASE")
    results = run_dijkstra_quantum(
        times=times,
        graph_type=SPECIAL_CASE,
        time_limit=time_limit,
        same_graph=same_graph,
    )
    save_results_to_json_quantum(
        directory=result_directory,
        name=result_file_names[3],
        results=results,
    )


def run_dijkstra_quantum(
    times: int, graph_type: str, time_limit: int, same_graph: int
) -> Dict[str, Any]:
    """
    Run the quantum-inspired Dijkstra's algorithm over all problem sizes and record results.

    Parameters
    ----------
    times : int
        Number of independently repeated runs per graph size.
    graph_type : str
        Type/tag of the graph family.
    time_limit : int
        1 to enforce time limit in quantum min, 0 otherwise.
    same_graph : int
        1 to reuse the same graph; 0 to use a new instance per repetition.

    Returns
    -------
    results : dict
        Contains per-size/run arrays:
            - 'vertices': list of graph sizes
            - 'cost': outer list = sizes, inner = [run values]
            - 'mismatch_counts': min-mismatch count [size][run]
            - 'invalid_counts': count of output invalid cases [size][run]
            - 'search_calls': quantum min search uses [size][run]
    """
    vertices = create_frequency()
    cost = []
    mismatch_counts = []
    invalid_counts = []
    search_calls = []

    start_node = 0
    for i in vertices:
        size_cost = []
        size_mismatches = []
        size_invalids = []
        size_search_calls = []
        for run in range(times):
            graph_number = 1 if same_graph == 1 else run + 1
            loaded_graph = load_graph_from_json(name=f"{i}{graph_type}_{graph_number}")
            lengths_naive, previous_naive, elapsed, mismatch_count, search_count = (
                dijkstra_quantum(
                    graph=loaded_graph, start_node=start_node, time_limit=time_limit
                )
            )
            valid = is_dijkstra_valid(
                graph=loaded_graph,
                start_node=start_node,
                lengths_result=lengths_naive,
                previous_result=previous_naive,
            )
            invalid = 0 if valid else 1
            size_cost.append(elapsed)
            size_mismatches.append(mismatch_count)
            size_invalids.append(invalid)
            size_search_calls.append(search_count)
        cost.append(size_cost)
        mismatch_counts.append(size_mismatches)
        invalid_counts.append(size_invalids)
        search_calls.append(size_search_calls)

    results = {
        "vertices": vertices,
        "cost": cost,
        "mismatch_counts": mismatch_counts,
        "invalid_counts": invalid_counts,
        "search_calls": search_calls,
    }
    return results


def dijkstra_quantum(
    graph: AdjacencyList, start_node: int, time_limit: int
) -> tuple[list[float], list[None], float, int, int]:
    """
    Quantum-inspired Dijkstra's algorithm (using quantum min search subroutine).

    Parameters
    ----------
    graph : List[List[Tuple[int, int]]]
        Adjacency list graph[u] = [(neighbor, weight), ...]
    start_node : int
        Node index to start the SSSP search from.
    time_limit : int
        If nonzero, use a time/resource-limited quantum minimum search.

    Returns
    -------
    distances : List[float]
        Distance estimates from start_node.
    previous : List[Optional[int]]
        Parent/pointer array for each node.
    operation_count : float
        Proxy for runtime cost (calls to quantum min).
    mismatch_count : int
        Number of times the quantum min search didn't match the true min.
    search_calls : int
        Number of quantum min search executions.
    """
    n = len(graph)
    distances = [float("inf")] * n
    previous = [None] * n
    in_heap = [True] * n
    operation_count = 0.0
    mismatch_count = 0
    search_calls = 0

    distances[start_node] = 0

    for _ in range(n):
        # Build active nodes/distances arrays
        active_indices = [i for i in range(n) if in_heap[i]]
        if not active_indices:
            break

        active_distances = [distances[i] for i in active_indices]

        # Skip if all are inf (nothing reachable)
        if all(x == float("inf") for x in active_distances):
            break

        padded_indices, padded_distances = pad_to_power_of_two_with_indices(
            active_indices, active_distances
        )
        if not padded_indices:
            break

        min_idx_active, min_dist, cost, limit = find_min(
            active_distances=padded_distances, time_limit=time_limit
        )
        true_idx = min(range(len(padded_distances)), key=lambda i: padded_distances[i])
        if padded_distances[min_idx_active] != padded_distances[true_idx]:
            mismatch_count += 1
        operation_count += cost  # Approximate runtime cost
        search_calls += 1

        u = padded_indices[min_idx_active]
        if distances[u] == float("inf"):
            break  # Remaining nodes are unreachable

        in_heap[u] = False

        for v, weight in graph[u]:
            if in_heap[v]:
                new_distance = distances[u] + weight
                if new_distance < distances[v]:
                    distances[v] = new_distance
                    previous[v] = u

    return distances, previous, operation_count, mismatch_count, search_calls
