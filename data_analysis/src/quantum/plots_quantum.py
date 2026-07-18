import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from config import (
    COLOR_MAP,
    PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT,
    PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT,
    PLOT_TITLE_TYPE_NO_TIME_LIMIT,
    PLOT_TITLE_TYPE_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_TIME_LIMIT,
    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT,
    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT,
)
from data_analysis.src.helpers import (
    add_custom_legend,
    get_type_from_filename,
    quantum_stat_from_dict,
    read_results_from_json,
)


def plot_all_quantum_time_limit():
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


def plot_all_quantum_no_time_limit():
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


def plot_all_quantum_same_graph_time_limit():
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


def plot_all_quantum_same_graph_no_time_limit():
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


def plots_mean_quantum(data, title_type):
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


def plots_median_quantum(data, title_type):
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


def plots_std_quantum(data, title_type):
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


def plots_mismatch_quantum(data, title_type):
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


def plots_invalid_quantum(data, title_type):
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


def plots_search_calls_quantum(data, title_type):
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
