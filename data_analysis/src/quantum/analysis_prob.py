import json
import os
from pathlib import Path

import pandas as pd

from config import (
    DATA_DIRECTORY,
    RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT,
    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT,
    RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT,
    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT,
    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_NO_TIME_LIMIT,
    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_TIME_LIMIT,
    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT,
)
from data_analysis.src.helpers import read_results_from_json


def prob_stats_quantum_analysis():
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


def compute_and_merge_all_probs(results):
    dijkstra_dict = compute_dijkstra_success_prob(results)
    find_min_dict = compute_find_min_success_prob(results)
    mismatch_wo_invalid_dict = compute_mismatch_without_invalid_prob(results)
    invalid_when_mismatch_dict = compute_invalid_when_mismatch_prob(results)

    merged_results = {}

    for filename in results:
        if not filename.startswith("quantum"):
            continue
        # Keep this order!
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


def compute_dijkstra_success_prob(all_data):
    """
    For each file, computes success probability if dijkstra per vertex.
    Returns: { filename: {vertex: {...}} }
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


def compute_find_min_success_prob(all_data):
    """
    For each file, computes success probability against mismatch counts per vertex.
    Returns: { filename: {vertex: {...}} }
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


def compute_mismatch_without_invalid_prob(all_data):
    """
    Computes (per file!) for each vertex, the probability that a mismatch did NOT result in invalid.
    Returns: { filename: {vertex: {...}} }
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


def compute_invalid_when_mismatch_prob(all_data):
    """
    Computes (per file!) for each vertex, the probability that when a mismatch happened it resulted in invalid dijkstra result
    Returns: { filename: {vertex: {...}} }
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


def save_merged_prob_stats_by_file(merged, directory):
    """
    Save merged per-file/vertex stats dict to separate JSON files.
    merged_stats_dict: {file_name: {vertex: {...stats...}, ...}, ...}
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
