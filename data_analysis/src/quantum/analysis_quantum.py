"""
Dijkstra Operation Count Plotting Utility
----------------------------------------

This module provides utilities for statistical analysis and plotting of Dijkstra's operation counts from experiment result files,
with focus on quantum variations. The statistics are computed per result file and for each "2D-list" field except 'vertices',
and are saved back as JSON.

Functions
---------
- stats_analysis_quantum: Compute summary statistics from several sources of quantum results, saving per-file stats.
- stats_by_file_quantum: Given loaded results, compute stats-per-field for each file, skipping the 'vertices' key.
- save_stats_by_file_quantum: Serialize and save statistics for all result files into built directory.

Types
-----
- The result files must be a dictionary mapping file name -> underlying field dict keyed by metrics (except 'vertices'),
  where each is a 2D list (list of lists of numbers).
"""

import json
from pathlib import Path
from pprint import pprint
from typing import Any, Dict

import pandas as pd

from config import (DATA_DIRECTORY, RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT,
                    RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_TIME_LIMIT_COST_COMPARISON,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT)
from data_analysis.src.helpers import (per_count_row_statistics,
                                       read_results_from_json)


def stats_analysis_quantum() -> None:
    """
    Calculate and save relevant statistics for all quantum result directories defined in config.

    For each relevant result directory (with or without time limits, and variants using the same graph),
    statistics are calculated and saved to stats directories, one file per input file.
    """
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

    time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT
    )
    time_limit_stats = stats_by_file_quantum_time_limit_cost(results=time_limit_results)
    save_stats_by_file_quantum_time_limit(
        stats=time_limit_stats,
        directory=STATS_DIRECTORY_QUANTUM_TIME_LIMIT_COST_COMPARISON,
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

    same_graph_no_time_limit_results = read_results_from_json(
        directory=RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT
    )
    same_graph_no_time_limit_stats = stats_by_file_quantum(
        results=same_graph_no_time_limit_results
    )
    save_stats_by_file_quantum(
        stats=same_graph_no_time_limit_stats,
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT,
    )


def stats_by_file_quantum(
    results: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """
    For 'quantum' result files, calculate statistics for all 2D-list fields except 'vertices'.

    Parameters
    ----------
    results : dict
        Mapping from result file name to loaded data ({key: value} per file).

    Returns
    -------
    dict
        Nested dict: {file_name: {field_name: statistics_df, ...}, ...}
        Each statistics_df is a DataFrame computed per field.
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


def save_stats_by_file_quantum(
    stats: Dict[str, Dict[str, Any]],
    directory: str,
) -> None:
    """
    Save quantum stats for each file in the provided directory.

    Parameters
    ----------
    stats : dict
        Output from stats_by_file_quantum, a nested dict by file and field, mapping onto pandas DataFrames

    directory : str
        Subdirectory (under DATA_DIRECTORY/) to save the stats files.
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


def stats_by_file_quantum_time_limit_cost(
    results: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """
    For 'quantum' time limit cost result files, calculate statistics.

    Parameters
    ----------
    results : dict
        Mapping from result file name to loaded data ({key: value} per file).

    Returns
    -------
    dict
        Nested dict: {file_name: {field_name: statistics_df, ...}, ...}
        Each statistics_df is a DataFrame computed per field.
    """
    all_stats = {}

    for file_name, data in results.items():
        vertices = data["vertices"]
        costs = data["cost"]
        mismatch_counts = data["mismatch_counts"]

        file_stats = {}

        for i, vertex_count in enumerate(vertices):

            if len(costs[i]) != len(mismatch_counts[i]):
                raise ValueError(
                    f"Inconsistent number of runs in {file_name}, "
                    f"vertices={vertex_count}"
                )

            rows = []

            for run_idx, cost in enumerate(costs[i]):
                rows.append(
                    {
                        "cost": cost,
                        "mismatch_count": mismatch_counts[i][run_idx],
                    }
                )

            df = pd.DataFrame(rows)

            by_mismatch = (
                df.groupby("mismatch_count")["cost"]
                .agg(
                    count="count",
                    mean="mean",
                    std="std",
                    median="median",
                    min="min",
                    max="max",
                )
                .fillna(0)
            )

            file_stats[str(vertex_count)] = {
                "by_mismatch": by_mismatch.to_dict(orient="index")
            }

        all_stats[file_name] = file_stats

    return all_stats


def save_stats_by_file_quantum_time_limit(
    stats: Dict[str, Dict[str, Any]],
    directory: str,
) -> None:
    """
    Save quantum time limit stats for each file in the provided directory.

    Parameters
    ----------
    stats : dict
        Output from stats_by_file_quantum, a nested dict by file and field, mapping onto pandas DataFrames

    directory : str
        Subdirectory (under DATA_DIRECTORY/) to save the stats files.
    """
    project_root = Path(__file__).parent.parent.parent.parent
    output_dir = project_root / DATA_DIRECTORY / directory
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_name, file_stats in stats.items():
        input_path = Path(file_name)

        output_file_name = f"{input_path.stem}_stats.json"
        output_path = output_dir / output_file_name

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(
                file_stats,
                file,
                indent=4,
                ensure_ascii=False,
            )

    print(f"Quantum time-limit stats saved to: {output_dir}")
