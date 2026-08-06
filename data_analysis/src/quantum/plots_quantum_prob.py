"""
Quantum Probability Statistics Plotting Utilities
------------------------------------------------

This module provides utility functions for visualizing various probability statistics
from quantum algorithm experiments on different types of graphs. The statistics are
presumed precomputed and saved as JSON files, organized by specific experiment scenarios
(e.g., time limit, no time limit, same graph structure).

The main functions automate the loading, processing, and plotting of key quantum-related
probabilities for sets of experimental graph data using matplotlib.

Functions:
----------
- plot_all_quantum_prob_time_limit:    Plot all probability statistics with quantum time limits.
- plot_all_quantum_prob_no_time_limit: Plot all probability statistics with no quantum time limits.
- plot_all_quantum_prob_same_graph_time_limit:    Plot all on same graph with time limits.
- plot_all_quantum_prob_same_graph_no_time_limit: Plot all on same graph with no time limits.
- plot_bars_with_percent: Plot a bar chart with attached percentage labels.
- plot_dijkstra_success_prob: Plot P(Dijkstra Success) by graph family/type.
- plot_find_min_success_prob: Plot P(Find Min Success) by graph family/type.
- plot_mismatch_without_invalid_prob: Plot mismatch prob (sans invalid) by graph family/type.
- plot_invalid_when_mismatch_prob:    Plot P(Invalid | Mismatch) by graph family/type.
- plot_grouped_dijkstra_and_find_min_success_prob: Plot Dijkstra and Find-Min grouped comparison.

Types:
------
- StatDict: Dict[str, Dict[str, float]]
- AllStatsDict: Dict[str, StatDict]
- TitlesList: List[str]
- FilenamesList: List[str]
"""

from typing import Dict, List

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from config import (STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT,
                    STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_NO_TIME_LIMIT,
                    STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_TIME_LIMIT)
from data_analysis.src.helpers import order_filenames, read_results_from_json

StatDict = Dict[str, Dict[str, float]]
AllStatsDict = Dict[str, StatDict]
TitlesList = List[str]
FilenamesList = List[str]


def plot_all_quantum_prob_time_limit() -> None:
    """
    Plot all quantum probability statistics for the scenario with quantum time limits.
    Loads data from the corresponding directory and generates all bar plots.
    """
    data = read_results_from_json(directory=STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT)
    titles = ["Sparse", "Half edges", "Dense", "Special case"]
    ordered_filenames = order_filenames(all_stats=data)

    plot_dijkstra_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_find_min_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_mismatch_without_invalid_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_invalid_when_mismatch_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_grouped_dijkstra_and_find_min_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )


def plot_all_quantum_prob_no_time_limit() -> None:
    """
    Plot all quantum probability statistics for the scenario with no quantum time limit.
    Loads data from the corresponding directory and generates all bar plots.
    """
    data = read_results_from_json(directory=STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT)
    titles = ["Sparse", "Half edges", "Dense", "Special case"]
    ordered_filenames = order_filenames(all_stats=data)

    plot_dijkstra_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_find_min_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_mismatch_without_invalid_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_invalid_when_mismatch_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_grouped_dijkstra_and_find_min_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )


def plot_all_quantum_prob_same_graph_time_limit() -> None:
    """
    Plot all quantum probability statistics for the *same* graph experiment with time limit.
    Loads data from the corresponding directory and generates all bar plots.
    """
    data = read_results_from_json(
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_TIME_LIMIT
    )
    titles = ["Sparse", "Half edges", "Dense", "Special case"]
    ordered_filenames = order_filenames(all_stats=data)

    plot_dijkstra_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_find_min_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_mismatch_without_invalid_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_invalid_when_mismatch_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_grouped_dijkstra_and_find_min_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )


def plot_all_quantum_prob_same_graph_no_time_limit() -> None:
    """
    Plot all quantum probability statistics for the *same* graph experiment with no time limit.
    Loads data from the corresponding directory and generates all bar plots.
    """
    data = read_results_from_json(
        directory=STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_NO_TIME_LIMIT
    )
    titles = ["Sparse", "Half edges", "Dense", "Special case"]
    ordered_filenames = order_filenames(all_stats=data)

    plot_dijkstra_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_find_min_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_mismatch_without_invalid_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_invalid_when_mismatch_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )
    plot_grouped_dijkstra_and_find_min_success_prob(
        all_stats=data, titles=titles, ordered_filenames=ordered_filenames
    )


def plot_bars_with_percent(
    ax: plt.Axes,
    xs: List[int],
    ys: List[float],
    y_label: str,
    title: str,
    x_label: str,
) -> None:
    """
    Utility function to plot a bar chart and annotate each bar with its value as a percentage.

    Parameters
    ----------
    ax : plt.Axes
        Matplotlib axes to plot on.
    xs : List[int]
        X-values (e.g., sizes of the graphs).
    ys : List[float]
        Y-values (probabilities, must be in [0,1]).
    y_label : str
        Label for the Y-axis.
    title : str
        Title for the subplot.
    x_label : str
        Label for the X-axis.
    """
    bars = ax.bar(xs, ys, width=2)
    for bar, y in zip(bars, ys):
        ax.annotate(
            f"{y*100:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, y),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title, pad=20)
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xticks(xs)
    ax.set_xticklabels([str(x) for x in xs], fontsize=10)


def plot_dijkstra_success_prob(
    all_stats: AllStatsDict, titles: TitlesList, ordered_filenames: FilenamesList
) -> None:
    """
    Plot the probability of Dijkstra's algorithm returning the correct result
    for each graph variant.

    Parameters
    ----------
    all_stats : AllStatsDict
        Nested dictionary with statistics data for each filename/graph type.
    titles : TitlesList
        List of plot titles per graph type.
    ordered_filenames : FilenamesList
        List of filenames in order to match subplot and title.
    """
    i = 0
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    for i, filename in enumerate(ordered_filenames[:4]):
        stat_dict = all_stats[filename]
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["dijkstra_success_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            y_label="Probability (%)",
            title=titles[i],
            x_label="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Dijkstra Success Probability")
    plt.tight_layout(rect=(0, 0.03, 1, 0.97))
    plt.show()


def plot_find_min_success_prob(
    all_stats: AllStatsDict, titles: TitlesList, ordered_filenames: FilenamesList
) -> None:
    """
    Plot the probability of successfully finding the minimum value in the graph statistics.

    Parameters
    ----------
    all_stats : AllStatsDict
        Nested dictionary with statistics data for each filename/graph type.
    titles : TitlesList
        List of plot titles per graph type.
    ordered_filenames : FilenamesList
        List of filenames in order to match subplot and title.
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    i = 0
    for i, filename in enumerate(ordered_filenames[:4]):
        stat_dict = all_stats[filename]
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["find_min_success_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            y_label="Probability (%)",
            title=titles[i],
            x_label="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Find Min Success Probability")
    plt.tight_layout(rect=(0, 0.03, 1, 0.97))
    plt.show()


def plot_mismatch_without_invalid_prob(
    all_stats: AllStatsDict, titles: TitlesList, ordered_filenames: FilenamesList
) -> None:
    """
    Plot the probability of mismatch excluding invalid cases (e.g., mismatches where the output is not simply invalid).

    Parameters
    ----------
    all_stats : AllStatsDict
        Nested dictionary with statistics data for each filename/graph type.
    titles : TitlesList
        List of plot titles per graph type.
    ordered_filenames : FilenamesList
        List of filenames in order to match subplot and title.
    """
    i = 0
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    for i, filename in enumerate(ordered_filenames[:4]):
        stat_dict = all_stats[filename]
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["mismatch_without_invalid_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            y_label="Probability (%)",
            title=titles[i],
            x_label="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Mismatch Without Invalid Probability")
    plt.tight_layout(rect=(0, 0.03, 1, 0.97))
    plt.show()


def plot_invalid_when_mismatch_prob(
    all_stats: AllStatsDict, titles: TitlesList, ordered_filenames: FilenamesList
) -> None:
    """
    Plot the probability of an invalid result given a mismatch condition.

    Parameters
    ----------
    all_stats : AllStatsDict
        Nested dictionary with statistics data for each filename/graph type.
    titles : TitlesList
        List of plot titles per graph type.
    ordered_filenames : FilenamesList
        List of filenames in order to match subplot and title.
    """
    i = 0
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    for i, filename in enumerate(ordered_filenames[:4]):
        stat_dict = all_stats[filename]
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["invalid_when_mismath_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            y_label="Probability (%)",
            title=titles[i],
            x_label="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Invalid When Mismatch Probability")
    plt.tight_layout(rect=(0, 0.03, 1, 0.97))
    plt.show()


def plot_grouped_dijkstra_and_find_min_success_prob(
    all_stats: AllStatsDict, titles: TitlesList, ordered_filenames: FilenamesList
) -> None:
    """
    Plot grouped bar charts for Dijkstra and Find-Min success probabilities for comparison.

    Parameters
    ----------
    all_stats : AllStatsDict
        Nested dictionary with statistics data for each filename/graph type.
    titles : TitlesList
        List of plot titles per graph type.
    ordered_filenames : FilenamesList
        List of filenames in order to match subplot and title.
    """
    i = 0
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    cmap = plt.get_cmap("Blues", 8)
    axs = axs.flatten()
    width = 2
    sep = 1
    for i, filename in enumerate(ordered_filenames[:4]):
        stat_dict = all_stats[filename]
        xs = np.array(sorted(int(k) for k in stat_dict))
        ys1 = [stat_dict[str(x)]["dijkstra_success_prob"] for x in xs]
        ys2 = [stat_dict[str(x)]["find_min_success_prob"] for x in xs]
        x1 = xs - width / 2 - sep / 2
        x2 = xs + width / 2 + sep / 2

        axs[i].bar(x1, ys1, width=width, color=cmap(3), label="Dijkstra Success Prob")
        axs[i].bar(x2, ys2, width=width, color=cmap(5), label="Find Min Success Prob")
        axs[i].set_ylabel("Probability (%)")
        axs[i].set_xlabel("Vertices")
        axs[i].set_title(titles[i], pad=20)
        axs[i].set_ylim(0, 1)
        axs[i].yaxis.set_major_formatter(ticker.PercentFormatter(1.0, decimals=0))
        axs[i].set_xticks(xs)
        axs[i].set_xticklabels([str(x) for x in xs], fontsize=10)
        axs[i].legend()
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Dijkstra vs Find Min Success Probability")
    plt.tight_layout(rect=(0, 0.03, 1, 0.97))
    plt.show()
