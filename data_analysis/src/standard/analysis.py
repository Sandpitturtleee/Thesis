"""
Dijkstra Operation Count Plotting Utility
----------------------------------------

This module provides a utility function for plotting the operation counts of Dijkstra's algorithm
for multiple graph types, assuming results are loaded from JSONs of a specific structure.

Functions
---------
- plot_dijkstra_counts: Plot Dijkstra's operation counts for different graph types loaded from result files
"""

import json
from pathlib import Path

from config import (
    DATA_DIRECTORY,
    RESULTS_DIRECTORY_STANDARD_HEAP,
    RESULTS_DIRECTORY_STANDARD_NAIVE,
    STATS_DIRECTORY_STANDARD_HEAP,
    STATS_DIRECTORY_STANDARD_NAIVE,
)
from data_analysis.src.helpers import per_count_row_statistics, read_results_from_json


def stats_analysis_standard():
    heap_results = read_results_from_json(directory=RESULTS_DIRECTORY_STANDARD_HEAP)
    heap_stats = stats_by_file_standard(results=heap_results)
    save_stats_by_file(stats=heap_stats, directory=STATS_DIRECTORY_STANDARD_HEAP)

    naive_results = read_results_from_json(directory=RESULTS_DIRECTORY_STANDARD_NAIVE)
    naive_stats = stats_by_file_standard(results=naive_results)
    save_stats_by_file(stats=naive_stats, directory=STATS_DIRECTORY_STANDARD_NAIVE)


def stats_by_file_standard(results):
    """
    For 'standard' files, calculate statistics for 'count' field only.
    Returns: {fname: stats_df}
    """
    all_stats = {}
    for file_name, data in results.items():
        if file_name.startswith("standard"):
            stats_df = per_count_row_statistics(
                data["count"], vertices=data["vertices"]
            )
            all_stats[file_name] = stats_df
    return all_stats


def save_stats_by_file(stats, directory):
    """
    Save stats for classic/standard files.
    Each is wrapped in a top-level 'cost' key.
    """
    project_root = Path(__file__).parent.parent.parent.parent
    output_dir = project_root / DATA_DIRECTORY / directory
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_name, stats in stats.items():
        file_name_out = Path(file_name).stem + ".json"
        out_path = output_dir / file_name_out
        wrapped = {"cost": stats.to_dict(orient="index")}

        with open(out_path, "w") as f:
            json.dump(wrapped, f, indent=4)
    print(f"Stats saved to {output_dir}")
