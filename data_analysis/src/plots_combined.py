import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from config import (
    GRAPH_TYPES_MAPPING,
    STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_TIME_LIMIT,
    STATS_DIRECTORY_STANDARD_HEAP,
    STATS_DIRECTORY_STANDARD_NAIVE,
)
from data_analysis.src.helpers import (
    extract_methods_and_labels,
    merge_stats_dicts,
    read_results_from_json,
)


def plot_standard_quantum_combined():
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


def plot_standard_combined():
    exclude = []
    naive_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_NAIVE)
    heap_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_HEAP)
    merged = [naive_stats, heap_stats]
    merged_stats = merge_stats_dicts(dicts=merged)
    plots_types_by_stat(data=merged_stats, stat_key="mean", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="median", exclude_files=exclude)
    plots_types_by_stat(data=merged_stats, stat_key="std", exclude_files=exclude)


def plot_quantum_combined():
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


def plots_types_by_stat(data, stat_key, exclude_files=None):
    """
    Plot the chosen stat for 4 types of graphs: sparse, half_edges, dense, worstcase.
    Each type gets its own subplot. Legend uses display names, not raw keys.
    """
    if exclude_files is None:
        exclude_files = []

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs = axs.flatten()

    for idx, (display_name, keyword, cmap) in enumerate(GRAPH_TYPES_MAPPING):
        files = [
            f
            for f in data
            if keyword in f and "cost" in data[f] and f not in exclude_files
        ]
        if not files:
            axs[idx].set_title(f"{display_name} (No Data)")
            continue

        # Prepare one color for each file (shades)
        shades = [
            cmap(0.5 + 0.5 * i / max(len(files) - 1, 1)) for i in range(len(files))
        ]
        handles_dict = {}  # for custom legend

        for i, filename in enumerate(files):
            records = data[filename]["cost"]
            x = sorted(int(size) for size in records.keys() if size.isdigit())
            y = [records[str(size)][stat_key] for size in x]
            file_label = filename.replace(".json", "")
            label_nice = file_label.replace("_", " ")
            (handle,) = axs[idx].plot(
                x, y, marker="o", label=label_nice, color=shades[i]
            )
            handles_dict[label_nice] = handle

        # Sorted legend by desired label order (not raw file order)
        legend_labels = sorted(handles_dict.keys())
        axs[idx].legend([handles_dict[k] for k in legend_labels], legend_labels)

        axs[idx].set_title(display_name)
        axs[idx].set_xlabel("Vertices")
        axs[idx].set_ylabel(stat_key.capitalize())
        axs[idx].grid(True)

    plt.suptitle(f"{stat_key.capitalize()} for 4 types of graphs")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
