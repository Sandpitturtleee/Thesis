"""
Quantum Statistics Plotting Utilities
-------------------------------------

This module provides functions for visualizing statistical results for quantum algorithms
on graph datasets, including mean, median, standard deviation, mismatch and invalid counts,
and search call statistics, under different time-limit and problem-type scenarios. It supports:

Functions:
----------
- plot_all_quantum_time_limit:         Plot all quantum stats with a time limit across all types.
- plot_all_quantum_no_time_limit:      Plot all quantum stats without a time limit across all types.
- plot_all_quantum_same_graph_time_limit:     Plot all quantum stats with a time limit on the same graphs.
- plot_all_quantum_same_graph_no_time_limit:  Plot all quantum stats without a time limit on the same graphs.
- plot_quantum_time_limit_vs_no_time_limit_all:   Plot comparisons of quantum statistics with/without time limit.
- plot_quantum_same_graph_time_limit_vs_no_time_limit_all: Plot comparisons for same-graph with/without time limit.
- plot_quantum_stat_time_limit_vs_no_time_limit:            Plot a single quantum statistic split by time limit.
- plot_quantum_stat_same_graph_time_limit_vs_no_time_limit: Plot a single quantum statistic for same-graph comparison.
- plot_quantum_stat_subplot:                  Plot a quantum statistic on a matplotlib Axes.
- plots_mean_quantum:                         Plot quantum mean results as a function of graph size.
- plots_median_quantum:                       Plot quantum median results as a function of graph size.
- plots_std_quantum:                          Plot quantum std-deviation results as a function of graph size.
- plots_mismatch_quantum:                     Plot quantum mismatch counts as a function of graph size.
- plots_invalid_quantum:                      Plot quantum invalid counts as a function of graph size.
- plots_search_calls_quantum:                 Plot quantum search call stats as a function of graph size.

Types:
------
- QuantumStatsDict: type alias for Dict[str, dict] (filename -> stat dictionary)
- Axes:    Matplotlib Axes object for custom plotting.
"""

from typing import Any, Dict

import matplotlib.pyplot as plt

from config import (COLOR_MAP, PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT,
                    PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT,
                    PLOT_TITLE_TYPE_NO_TIME_LIMIT, PLOT_TITLE_TYPE_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT)
from data_analysis.src.helpers import (add_custom_legend,
                                       get_type_from_filename,
                                       quantum_stat_from_dict,
                                       read_results_from_json)

QuantumStatsDict = Dict[str, Any]


def plot_all_quantum_time_limit() -> None:
    """
    Plot all quantum statistics with a time limit for all graph types/configurations.
    """
    time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_QUANTUM_TIME_LIMIT
    )
    plots_mean_quantum(data=time_limit_stats, title_type=PLOT_TITLE_TYPE_TIME_LIMIT)
    plots_median_quantum(data=time_limit_stats, title_type=PLOT_TITLE_TYPE_TIME_LIMIT)
    plots_std_quantum(data=time_limit_stats, title_type=PLOT_TITLE_TYPE_TIME_LIMIT)
    plots_mismatch_quantum(data=time_limit_stats, title_type=PLOT_TITLE_TYPE_TIME_LIMIT)
    plots_invalid_quantum(data=time_limit_stats, title_type=PLOT_TITLE_TYPE_TIME_LIMIT)
    plots_search_calls_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_TYPE_TIME_LIMIT
    )


def plot_all_quantum_no_time_limit() -> None:
    """
    Plot all quantum statistics without a time limit for all graph types/configurations.
    """
    no_time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT
    )
    plots_mean_quantum(
        data=no_time_limit_stats, title_type=PLOT_TITLE_TYPE_NO_TIME_LIMIT
    )
    plots_median_quantum(
        data=no_time_limit_stats, title_type=PLOT_TITLE_TYPE_NO_TIME_LIMIT
    )
    plots_std_quantum(
        data=no_time_limit_stats, title_type=PLOT_TITLE_TYPE_NO_TIME_LIMIT
    )
    plots_mismatch_quantum(
        data=no_time_limit_stats, title_type=PLOT_TITLE_TYPE_NO_TIME_LIMIT
    )
    plots_invalid_quantum(
        data=no_time_limit_stats, title_type=PLOT_TITLE_TYPE_NO_TIME_LIMIT
    )
    plots_search_calls_quantum(
        data=no_time_limit_stats, title_type=PLOT_TITLE_TYPE_NO_TIME_LIMIT
    )


def plot_all_quantum_same_graph_time_limit() -> None:
    """
    Plot all quantum statistics with a time limit using the same graph instance for each configuration.
    """
    time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT
    )
    plots_mean_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT
    )
    plots_median_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT
    )
    plots_std_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT
    )
    plots_mismatch_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT
    )
    plots_invalid_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT
    )
    plots_search_calls_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT
    )


def plot_all_quantum_same_graph_no_time_limit() -> None:
    """
    Plot all quantum statistics without a time limit using the same graph instance for each configuration.
    """
    time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT
    )
    plots_mean_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT
    )
    plots_median_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT
    )
    plots_std_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT
    )
    plots_mismatch_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT
    )
    plots_invalid_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT
    )
    plots_search_calls_quantum(
        data=time_limit_stats, title_type=PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT
    )


def plot_quantum_time_limit_vs_no_time_limit_all() -> None:
    """
    Plot and compare all main statistics for quantum runs with and without time limits.
    """
    plot_quantum_stat_time_limit_vs_no_time_limit("cost", "mean", "mean")
    plot_quantum_stat_time_limit_vs_no_time_limit("cost", "median", "median")
    plot_quantum_stat_time_limit_vs_no_time_limit("cost", "std", "std")
    plot_quantum_stat_time_limit_vs_no_time_limit(
        "mismatch_counts", "mean", "mean mismatch count"
    )
    plot_quantum_stat_time_limit_vs_no_time_limit(
        "invalid_counts", "mean", "mean invalid count"
    )
    plot_quantum_stat_time_limit_vs_no_time_limit(
        "search_calls", "mean", "mean min search calls"
    )


def plot_quantum_same_graph_time_limit_vs_no_time_limit_all() -> None:
    """
    Plot and compare all main statistics for same-graph quantum runs with and without time limits.
    """
    plot_quantum_stat_same_graph_time_limit_vs_no_time_limit("cost", "mean", "mean")
    plot_quantum_stat_same_graph_time_limit_vs_no_time_limit("cost", "median", "median")
    plot_quantum_stat_same_graph_time_limit_vs_no_time_limit("cost", "std", "std")
    plot_quantum_stat_same_graph_time_limit_vs_no_time_limit(
        "mismatch_counts", "mean", "mean mismatch count"
    )
    plot_quantum_stat_same_graph_time_limit_vs_no_time_limit(
        "invalid_counts", "mean", "mean invalid count"
    )
    plot_quantum_stat_same_graph_time_limit_vs_no_time_limit(
        "search_calls", "mean", "mean min search calls"
    )


def plot_quantum_stat_time_limit_vs_no_time_limit(
    stat_type: str, stat_key: str, stat_label: str
) -> None:
    """
    Plot a single quantum stat (e.g. mean cost) for time-limited and no-time-limit cases side by side.

    Parameters
    ----------
    stat_type : str
        Statistic type: 'cost', 'mismatch_counts', 'invalid_counts', 'search_calls', etc.
    stat_key : str
        Key of statistic to plot, e.g., 'mean', 'median', 'std'.
    stat_label : str
        Text label for use in the plot title.
    """
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    # Time limit
    stats_time = read_results_from_json(STATS_DIRECTORY_QUANTUM_TIME_LIMIT)
    plot_quantum_stat_subplot(
        stats_time,
        stat_type,
        stat_key,
        axs[0],
        f"Quantum {PLOT_TITLE_TYPE_TIME_LIMIT} - {stat_label}",
    )

    # No time limit
    stats_no = read_results_from_json(STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT)
    plot_quantum_stat_subplot(
        stats_no,
        stat_type,
        stat_key,
        axs[1],
        f"Quantum {PLOT_TITLE_TYPE_NO_TIME_LIMIT} - {stat_label}",
    )

    fig.tight_layout()
    plt.show()


def plot_quantum_stat_same_graph_time_limit_vs_no_time_limit(
    stat_type: str, stat_key: str, stat_label: str
) -> None:
    """
    Plot a single quantum stat for same-graph time-limited vs. no-time-limit cases side-by-side.

    Parameters
    ----------
    stat_type : str
        Statistic type: 'cost', 'mismatch_counts', etc.
    stat_key : str
        Key of statistic to plot.
    stat_label : str
        Text label for plot title.
    """
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    # Same graph, time limit
    stats_time = read_results_from_json(STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT)
    plot_quantum_stat_subplot(
        stats_time,
        stat_type,
        stat_key,
        axs[0],
        f"Quantum {PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT} - {stat_label}",
    )

    # Same graph, no time limit
    stats_no = read_results_from_json(STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT)
    plot_quantum_stat_subplot(
        stats_no,
        stat_type,
        stat_key,
        axs[1],
        f"Quantum {PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT} - {stat_label}",
    )

    fig.tight_layout()
    plt.show()


def plot_quantum_stat_subplot(
    data: QuantumStatsDict,
    stat_type: str,
    stat_key: str,
    ax: plt.Axes,
    title: str,
) -> None:
    """
    Plot a statistic (mean, median, etc.) for all types on a Matplotlib Axes.

    Parameters
    ----------
    data : QuantumStatsDict
        Raw statistics dictionary loaded from JSON.
    stat_type : str
        Statistic type: 'cost', 'mismatch_counts', etc.
    stat_key : str
        Key for secondary statistic (e.g., 'mean', 'median', 'std').
    ax : matplotlib.axes.Axes
        Matplotlib Axes object on which to plot.
    title : str
        Title for this subplot.
    """
    handles_dict = {}
    for filename, dct in data.items():
        if "quantum" not in filename or stat_type not in dct:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        x, y = quantum_stat_from_dict(dct[stat_type], stat_key)
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line
    add_custom_legend(ax, handles_dict)
    ax.set_title(title)
    ax.set_xlabel("Vertices")
    ax.grid(True)
    if stat_type == "cost":
        ylabel = stat_key.capitalize()
    elif stat_type in ("mismatch_counts", "invalid_counts"):
        ylabel = "Mean " + stat_type.replace("_", " ")
    elif stat_type == "search_calls":
        ylabel = "Mean min search calls"
    else:
        ylabel = stat_type
    ax.set_ylabel(ylabel)


def plots_mean_quantum(data: QuantumStatsDict, title_type: str) -> None:
    """
    Plot the mean quantum cost as a function of graph size for all types/configurations.

    Parameters
    ----------
    data : QuantumStatsDict
        Input statistics dictionary.
    title_type : str
        Title string describing the type of quantum experiment/run.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}
    for filename, dct in data.items():
        if "quantum" not in filename or "cost" not in dct:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        x, y = quantum_stat_from_dict(dct["cost"], key="mean")
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line
    add_custom_legend(ax, handles_dict)
    ax.set_title(f"Quantum {title_type} - mean")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Mean")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_median_quantum(data: QuantumStatsDict, title_type: str) -> None:
    """
    Plot the median quantum cost as a function of graph size.

    Parameters
    ----------
    data : QuantumStatsDict
        Dictionary mapping filenames to their quantum cost/statistics dictionaries.
    title_type : str
        String to be used in the plot title to indicate type/category.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}
    for filename, dct in data.items():
        if "quantum" not in filename or "cost" not in dct:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        x, y = quantum_stat_from_dict(dct["cost"], "median")
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line
    add_custom_legend(ax, handles_dict)
    ax.set_title(f"Quantum {title_type} - median")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Median")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_std_quantum(data: QuantumStatsDict, title_type: str) -> None:
    """
    Plot the standard deviation of quantum cost as a function of graph size.

    Parameters
    ----------
    data : QuantumStatsDict
        Dictionary mapping filenames to their quantum cost/statistics dictionaries.
    title_type : str
        String to be used in the plot title to indicate type/category.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}
    for filename, dct in data.items():
        if "quantum" not in filename or "cost" not in dct:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        x, y = quantum_stat_from_dict(dct["cost"], "std")
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line
    add_custom_legend(ax, handles_dict)
    ax.set_title(f"Quantum {title_type} - std")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Std")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_mismatch_quantum(data: QuantumStatsDict, title_type: str) -> None:
    """
    Plot the mean mismatch count as a function of graph size.

    Parameters
    ----------
    data : QuantumStatsDict
        Dictionary mapping filenames to their quantum cost/statistics dictionaries.
    title_type : str
        String to be used in the plot title to indicate type/category.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}
    for filename, dct in data.items():
        if "quantum" not in filename or "mismatch_counts" not in dct:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        x, y = quantum_stat_from_dict(dct["mismatch_counts"], "mean")
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line
    add_custom_legend(ax, handles_dict)
    ax.set_title(f"Quantum {title_type} - mean mismatch count")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Mean mismatch")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_invalid_quantum(data: QuantumStatsDict, title_type: str) -> None:
    """
    Plot the mean invalid count as a function of graph size.

    Parameters
    ----------
    data : QuantumStatsDict
        Dictionary mapping filenames to their quantum cost/statistics dictionaries.
    title_type : str
        String to be used in the plot title to indicate type/category.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}
    for filename, dct in data.items():
        if "quantum" not in filename or "invalid_counts" not in dct:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        x, y = quantum_stat_from_dict(dct["invalid_counts"], "mean")
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line
    add_custom_legend(ax, handles_dict)
    ax.set_title(f"Quantum {title_type} - mean invalid count")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Mean invalid")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plots_search_calls_quantum(data: QuantumStatsDict, title_type: str) -> None:
    """
    Plot the mean minimum number of search calls as a function of graph size.

    Parameters
    ----------
    data : QuantumStatsDict
        Dictionary mapping filenames to their quantum cost/statistics dictionaries.
    title_type : str
        String to be used in the plot title to indicate type/category.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    handles_dict = {}
    for filename, dct in data.items():
        if "quantum" not in filename or "search_calls" not in dct:
            continue
        type_key = get_type_from_filename(filename)
        color = COLOR_MAP.get(type_key, "gray")
        label = type_key if type_key in COLOR_MAP else filename.replace(".json", "")
        x, y = quantum_stat_from_dict(dct["search_calls"], "mean")
        (line,) = ax.plot(x, y, marker="o", color=color, label=label)
        handles_dict[type_key] = line
    add_custom_legend(ax, handles_dict)
    ax.set_title(f"Quantum {title_type} - mean min search calls")
    ax.set_xlabel("Vertices")
    ax.set_ylabel("Mean min search calls")
    ax.grid(True)
    fig.tight_layout()
    plt.show()
