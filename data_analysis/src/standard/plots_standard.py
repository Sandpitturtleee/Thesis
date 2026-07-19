"""
Plotting Utilities for Experiment Results
----------------------------------------

This module provides utility functions for plotting the results of graph algorithm experiments.
It supports plotting mean, median, and standard deviation for both "naive" and "heap" methods,
as well as comparative subplots. All relevant functions handle JSON data structures produced
by the experiment scripts.

Functions:
----------
- plot_all_naive:         Plots mean, median, and std for all naive method results.
- plot_all_heap:          Plots mean, median, and std for all heap method results.
- plot_naive_vs_heap_all: Plots naive vs heap comparisons for mean, median, and std.
- plot_naive_vs_heap:     Plots a side-by-side comparison for a specific statistical key.
- plots_mean_heap:        Plots mean for heap method for each data type.
- plots_mean_naive:       Plots mean for naive method for each data type.
- plots_median_heap:      Plots median for heap method for each data type.
- plots_median_naive:     Plots median for naive method for each data type.
- plots_std_heap:         Plots std for heap method for each data type.
- plots_std_naive:        Plots std for naive method for each data type.
- plot_stat_subplot:      Helper for plotting a statistical result on a subplot.

Types:
------
- StatsDict:      Dict[str, dict]
- StatKey:        Literal["mean", "median", "std"]
"""

from typing import Any, Dict, Tuple

import matplotlib.pyplot as plt

from config import (COLOR_MAP, STATS_DIRECTORY_STANDARD_HEAP,
                    STATS_DIRECTORY_STANDARD_NAIVE)
from data_analysis.src.helpers import (add_custom_legend,
                                       get_type_from_filename,
                                       merge_stats_dicts,
                                       read_results_from_json)

StatsDict = Dict[str, Any]
StatKey = str  # "mean", "median", or "std"


def plot_all_naive() -> None:
    """
    Plot mean, median, and std plots for all naive method experiment results.
    """
    naive_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_NAIVE)
    plots_mean_naive(data=naive_stats)
    plots_median_naive(data=naive_stats)
    plots_std_naive(data=naive_stats)


def plot_all_heap() -> None:
    """
    Plot mean, median, and std plots for all heap method experiment results.
    """
    heap_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_HEAP)
    plots_mean_heap(data=heap_stats)
    plots_median_heap(data=heap_stats)
    plots_std_heap(data=heap_stats)


def plot_naive_vs_heap_all() -> None:
    """
    Plot comparisons (side-by-side) for mean, median, and std between naive and heap approaches.
    """
    plot_naive_vs_heap(stat_key="mean", stat_label="mean", fig_size=(16, 6))
    plot_naive_vs_heap(stat_key="median", stat_label="median", fig_size=(16, 6))
    plot_naive_vs_heap(stat_key="std", stat_label="std", fig_size=(16, 6))


def plot_naive_vs_heap(
    stat_key: StatKey,
    stat_label: str,
    fig_size: Tuple[int, int] = (16, 6),
) -> None:
    """
    Plot a side-by-side comparison for the given statistical key (mean, median, or std)
    between naive and heap methods.

    Parameters
    ----------
    stat_key : str
        Key to extract from result dicts ("mean", "median", or "std").
    stat_label : str
        Label used for plot titles.
    fig_size : tuple of int, optional
        Size of the matplotlib figure (width, height).
    """
    fig, axs = plt.subplots(1, 2, figsize=fig_size)
    naive_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_NAIVE)
    heap_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_HEAP)
    merged = merge_stats_dicts(dicts=[naive_stats, heap_stats])
    plot_stat_subplot(merged, "naive", stat_key, axs[0], f"Naive - {stat_label}")
    plot_stat_subplot(merged, "heap", stat_key, axs[1], f"Heap - {stat_label}")
    fig.tight_layout()
    plt.show()


def plots_mean_heap(data: StatsDict) -> None:
    """
    Plot mean results for all heap variant graphs.

    Parameters
    ----------
    data : StatsDict
        Nested dict containing result statistics read from JSON files.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}

    for filename, methods in data.items():
        if "heap" not in filename or "cost" not in methods:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["mean"] for size in x]
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line

    # Add n^2*logn curve
    xs = [
        int(size)
        for filename, methods in data.items()
        if "heap" in filename and "cost" in methods
        for size in methods["cost"].keys()
        if size.isdigit()
    ]
    x_all = sorted(set(xs))
    # y_lognn = [2.55 * n * n * np.log2(n) for n in x_all]
    # extra_curve, = ax.plot(x_all, y_lognn, label=r"$n^2 \log n$", linestyle="--", color="black")

    add_custom_legend(ax, handles_dict)
    # add_custom_legend(ax, handles_dict, [extra_curve], [r"$n^2 \log n$"])
    ax.set_title("Heap - mean")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Mean")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_mean_naive(data: StatsDict) -> None:
    """
    Plot mean results for all naive variant graphs.

    Parameters
    ----------
    data : StatsDict
        Nested dict containing result statistics read from JSON files.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}

    for filename, methods in data.items():
        if "naive" not in filename or "cost" not in methods:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["mean"] for size in x]
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line

    xs = [
        int(size)
        for filename, methods in data.items()
        if "naive" in filename and "cost" in methods
        for size in methods["cost"].keys()
        if size.isdigit()
    ]
    x_all_naive = sorted(set(xs))
    # y_n2 = [n * n for n in x_all_naive]
    # extra_curve, = ax.plot(x_all_naive, y_n2, label=r"$n^2$", linestyle="--", color="black")

    add_custom_legend(ax, handles_dict)
    # add_custom_legend(ax, handles_dict, [extra_curve], [r"$n^2$"])
    ax.set_title("Naive - mean")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Mean")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_median_heap(data: StatsDict) -> None:
    """
    Plot median results for all heap variant graphs.

    Parameters
    ----------
    data : StatsDict
        Nested dict containing result statistics read from JSON files.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}

    for filename, methods in data.items():
        if "heap" not in filename or "cost" not in methods:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["median"] for size in x]
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line

    add_custom_legend(ax, handles_dict)
    ax.set_title("Heap - median")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Median")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_median_naive(data: StatsDict) -> None:
    """
    Plot median results for all naive variant graphs.

    Parameters
    ----------
    data : StatsDict
        Nested dict containing result statistics read from JSON files.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}

    for filename, methods in data.items():
        if "naive" not in filename or "cost" not in methods:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["median"] for size in x]
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line

    add_custom_legend(ax, handles_dict)
    ax.set_title("Naive - median")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Median")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_std_heap(data: StatsDict) -> None:
    """
    Plot standard deviation for all heap variant graphs.

    Parameters
    ----------
    data : StatsDict
        Nested dict containing result statistics read from JSON files.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    handles_dict = {}

    for filename, methods in data.items():
        if "heap" not in filename or "cost" not in methods:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["std"] for size in x]
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line

    add_custom_legend(ax, handles_dict)
    ax.set_title("Heap - std")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Std")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_std_naive(data: StatsDict) -> None:
    """
    Plot standard deviation for all naive variant graphs.

    Parameters
    ----------
    data : StatsDict
        Nested dict containing result statistics read from JSON files.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    handles_dict = {}

    for filename, methods in data.items():
        if "naive" not in filename or "cost" not in methods:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["std"] for size in x]
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line

    add_custom_legend(ax, handles_dict)
    ax.set_title("Naive - std")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Std")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plot_stat_subplot(
    data: StatsDict,
    method_keyword: str,
    stat_key: StatKey,
    ax: plt.Axes,
    title: str,
) -> None:
    """
    Plot a single subplot for a chosen statistic for a method.

    Parameters
    ----------
    data : StatsDict
        Nested dict with all experiment results.
    method_keyword : str
        "naive" or "heap"; used to select relevant files.
    stat_key : str
        Statistical key to plot ("mean", "median", or "std").
    ax : plt.Axes
        Matplotlib Axes to draw into.
    title : str
        Title string for the subplot.
    """
    handles_dict = {}
    for filename, methods in data.items():
        if method_keyword not in filename or "cost" not in methods:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)][stat_key] for size in x]
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line
    add_custom_legend(ax, handles_dict)
    ax.set_title(title)
    ax.set_xlabel("Vertices")
    ax.set_ylabel(stat_key.capitalize())
    ax.grid(True)
