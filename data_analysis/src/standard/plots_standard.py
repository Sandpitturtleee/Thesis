import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from config import (
    COLOR_MAP,
    STATS_DIRECTORY_STANDARD_HEAP,
    STATS_DIRECTORY_STANDARD_NAIVE,
)
from data_analysis.src.helpers import (
    add_custom_legend,
    extract_methods_and_labels,
    get_type_from_filename,
    merge_dicts_standard,
    merge_stats_dicts,
    read_results_from_json,
)


def plot_all_naive():
    naive_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_NAIVE)
    plots_mean_naive(data=naive_stats)
    plots_median_naive(data=naive_stats)
    plots_std_naive(data=naive_stats)


def plot_all_heap():
    heap_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_HEAP)
    plots_mean_heap(data=heap_stats)
    plots_median_heap(data=heap_stats)
    plots_std_heap(data=heap_stats)


def plot_naive_vs_heap_all():
    plot_naive_vs_heap(stat_key="mean", stat_label="mean", fig_size=(16, 6))
    plot_naive_vs_heap(stat_key="median", stat_label="median", fig_size=(16, 6))
    plot_naive_vs_heap(stat_key="std", stat_label="std", fig_size=(16, 6))


def plot_naive_vs_heap(stat_key, stat_label, fig_size=(16, 6)):
    fig, axs = plt.subplots(1, 2, figsize=fig_size)
    naive_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_NAIVE)
    heap_stats = read_results_from_json(directory=STATS_DIRECTORY_STANDARD_HEAP)
    merged = merge_stats_dicts(dicts=[naive_stats, heap_stats])
    plot_stat_subplot(merged, "naive", stat_key, axs[0], f"Naive - {stat_label}")
    plot_stat_subplot(merged, "heap", stat_key, axs[1], f"Heap - {stat_label}")
    fig.tight_layout()
    plt.show()


def plots_mean_heap(data):
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


def plots_mean_naive(data):
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


def plots_median_heap(data):
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


def plots_median_naive(data):
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


def plots_std_heap(data):
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


def plots_std_naive(data):
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


def plot_stat_subplot(data, method_keyword, stat_key, ax, title):
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
