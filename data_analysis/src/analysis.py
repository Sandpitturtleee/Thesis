"""
Dijkstra Operation Count Plotting Utility
----------------------------------------

This module provides a utility function for plotting the operation counts of Dijkstra's algorithm
for multiple graph types, assuming results are loaded from JSONs of a specific structure.

Functions
---------
- plot_dijkstra_counts: Plot Dijkstra's operation counts for different graph types loaded from result files
"""

import numpy as np
import pandas as pd

from config import DIJKSTRA_RESULTS_DIRECTORY, DIJKSTRA_STATS_DIRECTORY
from data_analysis.src.helpers import (
    read_results_from_json,
    save_stats_by_file,
    save_stats_by_file_quantum,
)


def stats_analysis():
    dijkstra_results = read_results_from_json(directory=DIJKSTRA_RESULTS_DIRECTORY)
    standard_stats = statistics_by_file_standard(dijkstra_results)
    save_stats_by_file(standard_stats)
    quantum_stats = statistics_by_file_quantum(dijkstra_results)
    save_stats_by_file_quantum(
        stats_by_file=quantum_stats, directory=DIJKSTRA_STATS_DIRECTORY
    )


def per_count_row_statistics(counts, vertices=None):
    """
    Compute statistics per row for a 2D list of counts.
    If vertices are provided, use them as the DataFrame index.
    """
    df = pd.DataFrame(counts)
    if vertices is not None:
        df.index = vertices  # Set index for better labeling
    df_stats = pd.DataFrame(
        {
            "mean": df.mean(axis=1),
            "std": df.std(axis=1),
            "median": df.median(axis=1),
            "min": df.min(axis=1),
            "max": df.max(axis=1),
        },
        index=df.index,
    )
    return df_stats


def statistics_by_file_standard(results_dict):
    """
    For 'standard' files, calculate statistics for 'count' field only.
    Returns: {fname: stats_df}
    """
    all_stats = {}
    for file_name, data in results_dict.items():
        if file_name.startswith("standard"):
            stats_df = per_count_row_statistics(
                data["count"], vertices=data["vertices"]
            )
            all_stats[file_name] = stats_df
    return all_stats


def statistics_by_file_quantum(results_dict):
    """
    For 'quantum' files, calculate statistics for all 2D-list fields except 'vertices'.
    Returns: {fname: {key: stats_df}}
    """
    all_stats = {}
    for file_name, data in results_dict.items():
        if file_name.startswith("quantum"):
            stats_by_field = {}
            vertices = data.get("vertices", None)
            for key, value in data.items():
                if (
                    key != "vertices"
                    and isinstance(value, list)
                    and value
                    and isinstance(value[0], list)
                ):
                    stats_by_field[key] = per_count_row_statistics(
                        value, vertices=vertices
                    )
            all_stats[file_name] = stats_by_field
    return all_stats
