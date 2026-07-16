import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from config import (
    DIJKSTRA_STATS_DIRECTORY,
    STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_TIME_LIMIT,
)
from data_analysis.src.helpers import quantum_stat_from_dict, read_results_from_json


def plot_all_quantum_time_limit():
    time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_QUANTUM_TIME_LIMIT
    )
    plots_mean_quantum(data=time_limit_stats)
    plots_median_quantum(data=time_limit_stats)
    plots_std_quantum(data=time_limit_stats)
    plots_mismatch_quantum(data=time_limit_stats)
    plots_invalid_quantum(data=time_limit_stats)
    plots_search_calls_quantum(data=time_limit_stats)


def plot_all_quantum_no_time_limit():
    no_time_limit_stats = read_results_from_json(
        directory=STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT
    )
    plots_mean_quantum(data=no_time_limit_stats)
    plots_median_quantum(data=no_time_limit_stats)
    plots_std_quantum(data=no_time_limit_stats)
    plots_mismatch_quantum(data=no_time_limit_stats)
    plots_invalid_quantum(data=no_time_limit_stats)
    plots_search_calls_quantum(data=no_time_limit_stats)


def plots_mean_quantum(data):
    plt.figure(figsize=(10, 6))
    count = 0
    for filename, dct in data.items():
        if "quantum" in filename and "cost" in dct:
            vertices, y = quantum_stat_from_dict(dct["cost"], key="mean")
            plt.plot(vertices, y, marker="o", label=filename.replace(".json", ""))
            count += 1
    plt.title("Quantum - mean")
    plt.xlabel("Vertices")
    plt.ylabel("Mean")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_median_quantum(data):
    plt.figure(figsize=(10, 6))
    for filename, dct in data.items():
        if "quantum" not in filename or "cost" not in dct:
            continue
        x, y = quantum_stat_from_dict(dct["cost"], "median")
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Quantum - median")
    plt.xlabel("Vertices")
    plt.ylabel("Median")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_std_quantum(data):
    plt.figure(figsize=(10, 6))
    for filename, dct in data.items():
        if "quantum" not in filename or "cost" not in dct:
            continue
        x, y = quantum_stat_from_dict(dct["cost"], "std")
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Quantum - std")
    plt.xlabel("Vertices")
    plt.ylabel("Std")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_mismatch_quantum(data):
    plt.figure(figsize=(10, 6))
    for filename, dct in data.items():
        if "quantum" not in filename or "mismatch_counts" not in dct:
            continue
        x, y = quantum_stat_from_dict(dct["mismatch_counts"], "mean")
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Quantum - mean mismatch count")
    plt.xlabel("Vertices")
    plt.ylabel("Mean mismatch")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_invalid_quantum(data):
    plt.figure(figsize=(10, 6))
    for filename, dct in data.items():
        if "quantum" not in filename or "invalid_counts" not in dct:
            continue
        x, y = quantum_stat_from_dict(dct["invalid_counts"], "mean")
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Quantum - mean invalid count")
    plt.xlabel("Vertices")
    plt.ylabel("Mean invalid")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plots_search_calls_quantum(data):
    plt.figure(figsize=(10, 6))
    for filename, dct in data.items():
        if "quantum" not in filename or "search_calls" not in dct:
            continue
        x, y = quantum_stat_from_dict(dct["search_calls"], "mean")
        plt.plot(x, y, marker="o", label=filename.replace(".json", ""))
    plt.title("Quantum - mean search_calls")
    plt.xlabel("Vertices")
    plt.ylabel("Mean search_calls")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
