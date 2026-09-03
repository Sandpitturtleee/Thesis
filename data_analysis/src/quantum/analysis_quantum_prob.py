"""
Quantum Probability Stats Analysis Utilities
-------------------------------------------

This module provides utility functions for analyzing quantum experiment results:
reading results, computing various per-vertex success probabilities, merging stats,
and saving the merged statistics to JSON files.

Functions:
----------
- prob_stats_quantum_analysis: Run all-prob analysis over new data and save as JSON to stats/quantum_prob/...
- compute_and_merge_all_probs: Merge a number of probability calculations for each quantum experiment file and vertex
- compute_dijkstra_success_prob: Compute Dijkstra's algorithm success probability per vertex and file
- compute_find_min_success_prob: Compute 'find min' operation success probability per vertex and file
- compute_mismatch_without_invalid_prob: Compute probability that mismatch did *not* result in invalid result
- compute_invalid_when_mismatch_prob: Compute probability that mismatch did result in invalid Dijkstra result
- save_merged_prob_stats_by_file: Save merged per-file/vertex stats dict to separate JSON files

Types:
------
- ResultsDict: type alias for `dict[str, dict[str, any]]`
- StatsDict: type alias for `dict[str, dict[str, dict[str, float|int]]]`
"""

import json
from pathlib import Path
from typing import Any, Dict

from config import (DATA_DIRECTORY, RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_NO_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_TIME_LIMIT)
from data_analysis.src.helpers import read_results_from_json

ResultsDict = Dict[str, Dict[str, Any]]
StatsDict = Dict[str, Dict[str, Dict[str, float | int]]]


def prob_stats_quantum_analysis() -> None:
    """
    Generate and save success probability statistics for all quantum result sets.

    Reads result files from configured directories, computes various success probabilities,
    merges stats by file/vertex, and saves as individual JSON summary files into the appropriate
    stats directories.
    """
    time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT
    )
    time_limit_merged = compute_and_merge_all_probs(results=time_limit_results)
    save_merged_prob_stats_by_file(
        merged=time_limit_merged, directory=STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT
    )

    no_time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT
    )
    no_time_limit_merged = compute_and_merge_all_probs(results=no_time_limit_results)
    save_merged_prob_stats_by_file(
        merged=no_time_limit_merged,
        directory=STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT,
    )

    same_graph_time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT
    )
    same_graph_time_limit_stats = compute_and_merge_all_probs(
        results=same_graph_time_limit_results
    )
    save_merged_prob_stats_by_file(
        merged=same_graph_time_limit_stats,
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_TIME_LIMIT,
    )

    no_time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT
    )
    no_time_limit_stats = compute_and_merge_all_probs(results=no_time_limit_results)
    save_merged_prob_stats_by_file(
        merged=no_time_limit_stats,
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_NO_TIME_LIMIT,
    )


def compute_and_merge_all_probs(results: ResultsDict) -> StatsDict:
    """
    Merge several quantum probability/statistics calculations per file and vertex.

    Parameters
    ----------
    results : ResultsDict
        Dictionary of quantum experiment results (output of read_results_from_json).

    Returns
    -------
    StatsDict
        Nested dictionary of merged statistics:
        {file_name: {vertex: {stat_name: value, ...}, ...}, ...}
    """
    dijkstra_dict = compute_dijkstra_success_prob(results)
    find_min_dict = compute_find_min_success_prob(results)
    mismatch_wo_invalid_dict = compute_mismatch_without_invalid_prob(results)
    invalid_when_mismatch_dict = compute_invalid_when_mismatch_prob(results)

    merged_results = {}

    for filename in results:
        if not filename.startswith("quantum"):
            continue
        vertices = results[filename]["vertices"]
        merged_results[filename] = {}
        for v in vertices:
            merged_entry = {}
            if filename in dijkstra_dict and v in dijkstra_dict[filename]:
                merged_entry.update(dijkstra_dict[filename][v])
            if filename in find_min_dict and v in find_min_dict[filename]:
                merged_entry.update(find_min_dict[filename][v])
            if (
                filename in mismatch_wo_invalid_dict
                and v in mismatch_wo_invalid_dict[filename]
            ):
                merged_entry.update(mismatch_wo_invalid_dict[filename][v])
            if (
                filename in invalid_when_mismatch_dict
                and v in invalid_when_mismatch_dict[filename]
            ):
                merged_entry.update(invalid_when_mismatch_dict[filename][v])
            merged_results[filename][v] = merged_entry

    return merged_results


def compute_dijkstra_success_prob(all_data: ResultsDict) -> StatsDict:
    """
    Compute, for each file, the success probability of Dijkstra for each vertex.

    Success = (calls - invalid) / calls

    Parameters
    ----------
    all_data : ResultsDict
        Dictionary mapping file names to per-file results.

    Returns
    -------
    StatsDict
        {filename: {vertex: {dijkstra_success_prob, invalid_total, calls_total}}}
    """
    results = {}
    for filename, file_data in all_data.items():
        if not filename.startswith("quantum"):
            continue
        file_result = {}
        vertices = file_data["vertices"]
        invalid_counts = file_data["invalid_counts"]
        length = len(invalid_counts[0])
        for i, v in enumerate(vertices):
            invalid_total = sum(invalid_counts[i])
            success_prob = 1 - (invalid_total / length) if length > 0 else 0
            file_result[v] = {
                "dijkstra_success_prob": success_prob,
                "invalid_total": invalid_total,
                "calls_total": length,
            }
        results[filename] = file_result
    return results


def compute_find_min_success_prob(all_data: ResultsDict) -> StatsDict:
    """
    For each file, compute 'find min' success probability per vertex, relative to total search calls.

    Success = (search_total - mismatch_total) / search_total

    Parameters
    ----------
    all_data : ResultsDict

    Returns
    -------
    StatsDict
        {filename: {vertex: {find_min_success_prob, mismatch_total, search_total}}}
    """
    results = {}
    for filename, file_data in all_data.items():
        if not filename.startswith("quantum"):
            continue
        file_result = {}
        vertices = file_data["vertices"]
        mismatch_counts = file_data["mismatch_counts"]
        search_calls = file_data["search_calls"]
        for i, v in enumerate(vertices):
            mismatch_total = sum(mismatch_counts[i])
            search_total = int(sum(search_calls[i]))
            success_prob = (
                1 - (mismatch_total / search_total) if search_total > 0 else 0
            )
            file_result[v] = {
                "find_min_success_prob": success_prob,
                "mismatch_total": mismatch_total,
                "search_total": search_total,
            }
        results[filename] = file_result
    return results


def compute_mismatch_without_invalid_prob(all_data: ResultsDict) -> StatsDict:
    """
    For each file, compute the probability that for each vertex, a mismatch did NOT result in invalid outcome.

    Probability = 1 - (# times mismatch AND invalid) / (# times mismatch occurred)

    Parameters
    ----------
    all_data : ResultsDict

    Returns
    -------
    StatsDict
        {filename: {vertex: {mismatch_without_invalid_prob, mismatch_and_invalid, mismatch_total}}}
    """
    results = {}
    for filename, file_data in all_data.items():
        if not filename.startswith("quantum"):
            continue
        file_result = {}
        vertices = file_data["vertices"]
        mismatch_counts = file_data["mismatch_counts"]
        invalid_counts = file_data["invalid_counts"]
        for i, v in enumerate(vertices):
            mismatch_total = 0
            mismatch_and_invalid = 0
            for mismatch, invalid in zip(mismatch_counts[i], invalid_counts[i]):
                if mismatch > 0:
                    mismatch_total += 1
                    if invalid > 0:
                        mismatch_and_invalid += 1
            prob = (
                1 - (mismatch_and_invalid / mismatch_total) if mismatch_total > 0 else 0
            )
            file_result[v] = {
                "mismatch_without_invalid_prob": prob,
                "mismatch_and_invalid": mismatch_and_invalid,
                "mismatch_total": mismatch_total,
            }
        results[filename] = file_result
    return results


def compute_invalid_when_mismatch_prob(all_data: ResultsDict) -> StatsDict:
    """
    For each file, compute probability that, for each vertex, a mismatch resulted in invalid Dijkstra result.

    Probability = (# times mismatch AND invalid) / (# times mismatch occurred)

    Parameters
    ----------
    all_data : ResultsDict

    Returns
    -------
    StatsDict
        {filename: {vertex: {invalid_when_mismatch_prob, mismatch_and_invalid, mismatch_total}}}
    """
    results = {}
    for filename, file_data in all_data.items():
        if not filename.startswith("quantum"):
            continue
        file_result = {}
        vertices = file_data["vertices"]
        mismatch_counts = file_data["mismatch_counts"]
        invalid_counts = file_data["invalid_counts"]
        for i, v in enumerate(vertices):
            mismatch_total = 0
            mismatch_and_invalid = 0
            for mismatch, invalid in zip(mismatch_counts[i], invalid_counts[i]):
                if mismatch > 0:
                    mismatch_total += 1
                    if invalid > 0:
                        mismatch_and_invalid += 1
            prob = (mismatch_and_invalid / mismatch_total) if mismatch_total > 0 else 0
            file_result[v] = {
                "invalid_when_mismath_prob": prob,
                "mismatch_and_invalid": mismatch_and_invalid,
                "mismatch_total": mismatch_total,
            }
        results[filename] = file_result
    return results


def save_merged_prob_stats_by_file(merged: StatsDict, directory: str) -> None:
    """
    Save merged per-file/vertex stats dict to separate JSON files by file.

    Each JSON file will contain all stats for every vertex in its corresponding experiment.

    Parameters
    ----------
    merged : StatsDict
        Merged per-file and per-vertex statistics dictionary.
    directory : str
        Relative directory name for output within the data directory.
    """
    project_root = Path(__file__).parent.parent.parent.parent
    output_dir = project_root / DATA_DIRECTORY / directory
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_name, vertex_stats in merged.items():
        file_name_out = Path(file_name).stem + ".json"
        out_path = output_dir / file_name_out
        with open(out_path, "w") as f:
            json.dump(vertex_stats, f, indent=4)
    print(f"Quantum prob stats saved to {output_dir}")
