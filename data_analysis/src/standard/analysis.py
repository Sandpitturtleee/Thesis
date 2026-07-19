"""
Dijkstra Operation Count Analysis and Plotting Utilities
-------------------------------------------------------

This module provides utility functions for analyzing and saving operation count statistics
from Dijkstra's algorithm experiments, particularly for "standard" graph types (naive and heap variants).
It assumes all results are loaded from JSON files with a specific structure and provides
batch statistical analysis and bulk JSON saving of summarized data.

Functions
---------
- stats_analysis_standard: Batch compute and save statistics for both heap and naive graph types.
- stats_by_file_standard: Calculate per-file statistics (mean, std, min, max) for Dijkstra operation counts.
- save_stats_by_file: Save batch statistics as pretty-printed JSON files.

Types:
-----
- StatsDict: type alias for Dict[str, Any]
- ResultsDict: type alias for Dict[str, Dict[str, Any]]
"""

import json
from pathlib import Path
from typing import Any, Dict

from config import (DATA_DIRECTORY, RESULTS_DIRECTORY_STANDARD_HEAP,
                    RESULTS_DIRECTORY_STANDARD_NAIVE,
                    STATS_DIRECTORY_STANDARD_HEAP,
                    STATS_DIRECTORY_STANDARD_NAIVE)
from data_analysis.src.helpers import (per_count_row_statistics,
                                       read_results_from_json)

StatsDict = Dict[str, Any]
ResultsDict = Dict[str, Dict[str, Any]]


def stats_analysis_standard() -> None:
    """
    Compute and save operation count statistics from standard Dijkstra experiments (heap and naive).

    Loads JSON result files, computes statistics for each, then saves them to
    their respective summary output directories as pretty-printed JSON files.
    """
    heap_results = read_results_from_json(directory=RESULTS_DIRECTORY_STANDARD_HEAP)
    heap_stats = stats_by_file_standard(results=heap_results)
    save_stats_by_file(stats=heap_stats, directory=STATS_DIRECTORY_STANDARD_HEAP)

    naive_results = read_results_from_json(directory=RESULTS_DIRECTORY_STANDARD_NAIVE)
    naive_stats = stats_by_file_standard(results=naive_results)
    save_stats_by_file(stats=naive_stats, directory=STATS_DIRECTORY_STANDARD_NAIVE)


def stats_by_file_standard(results: ResultsDict) -> StatsDict:
    """
    For each file with a key starting with 'standard', calculate summary statistics for only the 'count' field.

    Parameters
    ----------
    results : ResultsDict
        Mapping of file names to loaded experiment data dicts. Each data dict
        must contain "count" (sequence of operation counts) and "vertices" fields.

    Returns
    -------
    StatsDict
        Dictionary mapping file name to a DataFrame of per-row statistics
        (such as mean, std, min, max) indexed by graph size.
    """
    all_stats = {}
    for file_name, data in results.items():
        if file_name.startswith("standard"):
            stats_df = per_count_row_statistics(
                data["count"], vertices=data["vertices"]
            )
            all_stats[file_name] = stats_df
    return all_stats


def save_stats_by_file(stats: StatsDict, directory: str) -> None:
    """
    Save calculated statistics for standard Dijkstra result files as prettified JSON.
    Statistics for each file are wrapped under a top-level 'cost' key
    for convenience during later loading.

    Parameters
    ----------
    stats : StatsDict
        Mapping of file names to DataFrames with statistics.
    directory : str
        Target directory (subfolder of DATA_DIRECTORY) for output JSONs.

    Returns
    -------
    None
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
