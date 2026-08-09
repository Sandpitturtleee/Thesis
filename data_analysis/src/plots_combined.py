"""
Graph Experiment Plotting Utilities
===================================

This module provides utilities for reading statistical results of graph experiments,
combining and merging them, and plotting their mean, median, and standard deviation
for various graph types and experiment methods.

It integrates with existing configuration files and relies on data extraction helpers.
Plotting functions are provided for combinations of quantum and classical approaches.

Dependencies:
-------------
- numpy
- matplotlib
- networkx
- config (with experiment directory constants)
- data_analysis.src.helpers (for data extraction and merging)
- Data is assumed in JSON format within dedicated directories

Functions:
----------
- plot_standard_quantum_combined()
- plot_standard_combined()
- plot_quantum_combined()
- plot_quantum_same_graph_combined()
- plots_types_by_stat()

Types:
------
- DataStats: Dict[str, Any]
"""

from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt

from config import (GRAPH_TYPES_MAPPING, STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT,
                    STATS_DIRECTORY_STANDARD_HEAP,
                    STATS_DIRECTORY_STANDARD_NAIVE, VERTICES_X_PLOT_LABEL, GRAPH_LABELS_MAP, STAT_NAME_MAP)
from data_analysis.src.helpers import merge_stats_dicts, read_results_from_json

DataStats = Dict[str, Any]


def plot_standard_quantum_combined() -> None:
    """
    Plot comparison of all standard and quantum algorithms with and without time limits.

    Creates subplots for mean, median, and std statistics. Combines results from
    standard (naive, heap) and quantum (with/without time limit) experiment directories.
    """
    exclude = []
    naive_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_NAIVE)
    heap_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_HEAP)
    time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_QUANTUM_TIME_LIMIT
    )
    no_time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT
    )
    merged = [naive_stats, heap_stats, time_limit_stats, no_time_limit_stats]
    merged_stats = merge_stats_dicts(dicts=merged)
    plots_types_by_stat(data=merged_stats, stat_key="mean", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="median", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="std", exclude_files=exclude)


def plot_standard_combined() -> None:
    """
    Plot comparison of standard algorithms (naive and heap).

    Creates subplots for mean, median, and std statistics.
    """
    exclude = []
    naive_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_NAIVE)
    heap_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_HEAP)
    merged = [naive_stats, heap_stats]
    merged_stats = merge_stats_dicts(dicts=merged)
    plots_types_by_stat(data=merged_stats, stat_key="mean", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="median", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="std", exclude_files=exclude)


def plot_quantum_combined() -> None:
    """
    Plot comparison of quantum algorithms (with and without time limit).

    Creates subplots for mean, median, and std statistics.
    """
    exclude = []
    time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_QUANTUM_TIME_LIMIT
    )
    no_time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT
    )
    merged = [time_limit_stats, no_time_limit_stats]
    merged_stats = merge_stats_dicts(dicts=merged)
    plots_types_by_stat(data=merged_stats, stat_key="mean", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="median", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="std", exclude_files=exclude)


def plot_quantum_same_graph_combined() -> None:
    """
    Plot comparison of quantum algorithms (same-graph, with and without time limit).

    Creates subplots for mean, median, and std statistics.
    """
    exclude = []
    time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT
    )
    no_time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT
    )
    merged = [time_limit_stats, no_time_limit_stats]
    merged_stats = merge_stats_dicts(dicts=merged)
    plots_types_by_stat(data=merged_stats, stat_key="mean", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="median", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="std", exclude_files=exclude)


def plots_types_by_stat(
    data: DataStats, stat_key: str, exclude_files: Optional[List[str]] = None
) -> None:
    """
    Plot one statistic (mean/median/std) for each graph type over all available files.

    Each of four graph types (sparse, half_edges, dense, worstcase) gets a subplot.
    One line per algorithm/file. Provides custom legend, labeling each method.

    Parameters
    ----------
    data : DataStats
        The combined and merged results from all input experiment directories.
    stat_key : str
        Which statistic to plot ("mean", "median", "std").
    exclude_files : Optional[List[str]], default=None
        List of file names to exclude from plots.

    Returns
    -------
    None
    """
    if exclude_files is None:
        exclude_files = []

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs = axs.flatten()
    y_label = ""

    for idx, (display_name, keyword, cmap) in enumerate(GRAPH_TYPES_MAPPING):
        files = [
            f
            for f in data
            if keyword in f and "cost" in data[f] and f not in exclude_files
        ]
        if not files:
            axs[idx].set_title(f"{display_name} (No Data)")
            continue

        shades = [
            cmap(0.5 + 0.5 * i / max(len(files) - 1, 1)) for i in range(len(files))
        ]
        handles_dict = {}

        for i, filename in enumerate(files):
            records = data[filename]["cost"]
            x = sorted(int(size) for size in records.keys() if size.isdigit())
            y = [records[str(size)][stat_key] for size in x]
            file_label = filename.replace(".json", "")
            label_nice = GRAPH_LABELS_MAP.get(file_label, file_label)
            (handle,) = axs[idx].plot(
                x, y, marker="o", color=shades[i]
            )
            handles_dict[label_nice] = handle

        y_label = STAT_NAME_MAP.get(stat_key, stat_key.capitalize())
        legend_labels = sorted(handles_dict.keys())
        axs[idx].legend([handles_dict[k] for k in legend_labels], legend_labels)

        axs[idx].set_title(display_name)
        axs[idx].set_xlabel(VERTICES_X_PLOT_LABEL)
        axs[idx].set_ylabel(y_label)
        axs[idx].grid(True)

    plt.suptitle(f"{y_label} dla czterech typów grafów")
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))
    plt.show()
