import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from config import DIJKSTRA_STATS_DIRECTORY
from data_analysis.src.helpers import (
    extract_methods_and_labels,
    read_results_by_vertex,
    read_results_by_vertices,
    read_results_from_json,
)


def plot_all_standard():
    data = read_results_from_json(directory=DIJKSTRA_STATS_DIRECTORY)
    plots_mean_heap(data=data)
    plots_mean_naive(data=data)
    plots_median_heap(data=data)
    plots_median_naive(data=data)
    plots_std_heap(data=data)
    plots_std_naive(data=data)


def plots_mean_heap(data):
    plt.figure(figsize=(10, 6))
    for filename, methods in data.items():
        if "heap" not in filename or "cost" not in methods:
            continue
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["mean"] for size in x]
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    # Add n^2*logn curve
    xs = []
    for filename, methods in data.items():
        if "heap" not in filename or "cost" not in methods:
            continue
        xs += [int(size) for size in methods["cost"].keys() if size.isdigit()]
    x_all = sorted(set(xs))
    y_lognn = [2.55 * n * n * np.log2(n) for n in x_all]
    plt.plot(x_all, y_lognn, label=r"$n^2 \log n$", linestyle="--", color="black")
    plt.title("Heap - mean")
    plt.xlabel("Vertices")
    plt.ylabel("Mean")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_mean_naive(data):
    plt.figure(figsize=(10, 6))
    for filename, methods in data.items():
        if "naive" not in filename or "cost" not in methods:
            continue
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["mean"] for size in x]
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    # Add n^2 curve
    xs = []
    for filename, methods in data.items():
        if "naive" not in filename or "cost" not in methods:
            continue
        xs += [int(size) for size in methods["cost"].keys() if size.isdigit()]
    x_all_naive = sorted(set(xs))
    y_n2 = [n * n for n in x_all_naive]
    plt.plot(x_all_naive, y_n2, label=r"$n^2$", linestyle="--", color="black")
    plt.title("Naive - mean")
    plt.xlabel("Vertices")
    plt.ylabel("Mean")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_median_heap(data):
    plt.figure(figsize=(10, 6))
    for filename, methods in data.items():
        if "heap" not in filename or "cost" not in methods:
            continue
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["median"] for size in x]
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Heap - median")
    plt.xlabel("Vertices")
    plt.ylabel("Median")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_median_naive(data):
    plt.figure(figsize=(10, 6))
    for filename, methods in data.items():
        if "naive" not in filename or "cost" not in methods:
            continue
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["median"] for size in x]
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Naive - median")
    plt.xlabel("Vertices")
    plt.ylabel("Median")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_std_heap(data):
    plt.figure(figsize=(8, 5))
    for filename, methods in data.items():
        if "heap" not in filename or "cost" not in methods:
            continue
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["std"] for size in x]
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Heap - std")
    plt.xlabel("Vertices")
    plt.ylabel("Std")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_std_naive(data):
    plt.figure(figsize=(8, 5))
    for filename, methods in data.items():
        if "naive" not in filename or "cost" not in methods:
            continue
        records = methods["cost"]
        x = sorted(int(size) for size in records.keys() if size.isdigit())
        y = [records[str(size)]["std"] for size in x]
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Naive - std")
    plt.xlabel("Vertices")
    plt.ylabel("Std")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
