"""
Dijkstra Operation Count Plotting Utility
----------------------------------------

This module provides a utility function for plotting the operation counts of Dijkstra's algorithm
for multiple graph types, assuming results are loaded from JSONs of a specific structure.

Functions
---------
- plot_dijkstra_counts: Plot Dijkstra's operation counts for different graph types loaded from result files
"""

import pandas as pd

from config import DIJKSTRA_RESULTS_DIRECTORY
from data_analysis.src.helpers import read_results_from_json, save_stats_by_file


def stats_analysis():
    dijkstra_results = read_results_from_json(directory=DIJKSTRA_RESULTS_DIRECTORY)
    stats_by_file = statistics_by_file(dijkstra_results)
    save_stats_by_file(stats_by_file)


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


def statistics_by_file(results_dict):
    """
    For each result file, calculate statistics per input size (row) for 'count'.
    Returns: {fname: stats_df}
    """
    all_stats = {}
    for file_name, data in results_dict.items():
        stats_df = per_count_row_statistics(data["count"], vertices=data["vertices"])
        all_stats[file_name] = stats_df
    return all_stats
