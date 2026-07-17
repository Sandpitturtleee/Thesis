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
    RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT,
    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT,
    RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_TIME_LIMIT,
    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT,
    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT,
)
from data_analysis.src.helpers import per_count_row_statistics, read_results_from_json


def stats_analysis_quantum():
    time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT
    )
    time_limit_stats = stats_by_file_quantum(results=time_limit_results)
    save_stats_by_file_quantum(
        stats=time_limit_stats, directory=STATS_DIRECTORY_QUANTUM_TIME_LIMIT
    )

    no_time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT
    )
    no_time_limit_stats = stats_by_file_quantum(results=no_time_limit_results)
    save_stats_by_file_quantum(
        stats=no_time_limit_stats, directory=STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT
    )

    same_graph_time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT
    )
    same_graph_time_limit_stats = stats_by_file_quantum(
        results=same_graph_time_limit_results
    )
    save_stats_by_file_quantum(
        stats=same_graph_time_limit_stats,
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT,
    )

    no_time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT
    )
    no_time_limit_stats = stats_by_file_quantum(results=no_time_limit_results)
    save_stats_by_file_quantum(
        stats=no_time_limit_stats,
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT,
    )


def stats_by_file_quantum(results):
    """
    For 'quantum' files, calculate statistics for all 2D-list fields except 'vertices'.
    Returns: {fname: {key: stats_df}}
    """
    all_stats = {}
    for file_name, data in results.items():
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


def save_stats_by_file_quantum(stats, directory):
    """
    Save quantum stats for each file.
    stats_by_file = {file_name: {key: DataFrame, ...}, ...}
    """
    project_root = Path(__file__).parent.parent.parent.parent
    output_dir = project_root / DATA_DIRECTORY / directory
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_name, field_stats in stats.items():
        file_name_out = Path(file_name).stem + ".json"
        out_path = output_dir / file_name_out

        output_dict = {}
        for key, df in field_stats.items():
            output_dict[key] = df.to_dict(orient="index")

        with open(out_path, "w") as f:
            json.dump(output_dict, f, indent=4)
    print(f"Quantum stats saved to {output_dir}")
