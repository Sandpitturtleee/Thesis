import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

from config import (
    STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT,
    STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT,
)
from data_analysis.src.helpers import (
    order_filenames,
    quantum_stat_from_dict,
    read_results_from_json,
)


def plot_all_quantum_prob_time_limit():
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


def plot_all_quantum_prob_no_time_limit():
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


def plot_bars_with_percent(ax, xs, ys, ylabel, title, xlabel):
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
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title, pad=20)
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=0))
    ax.set_xticks(xs)
    ax.set_xticklabels([str(x) for x in xs], fontsize=10)


def plot_dijkstra_success_prob(all_stats, titles, ordered_filenames):
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
            ylabel="Probability (%)",
            title=titles[i],
            xlabel="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Dijkstra Success Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


def plot_find_min_success_prob(all_stats, titles, ordered_filenames):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    for i, filename in enumerate(ordered_filenames[:4]):
        stat_dict = all_stats[filename]
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["find_min_success_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            ylabel="Probability (%)",
            title=titles[i],
            xlabel="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Find Min Success Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


def plot_mismatch_without_invalid_prob(all_stats, titles, ordered_filenames):
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
            ylabel="Probability (%)",
            title=titles[i],
            xlabel="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Mismatch Without Invalid Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


def plot_invalid_when_mismatch_prob(all_stats, titles, ordered_filenames):
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
            ylabel="Probability (%)",
            title=titles[i],
            xlabel="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Invalid When Mismatch Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


def plot_grouped_dijkstra_and_find_min_success_prob(
    all_stats, titles, ordered_filenames
):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    cmap = cm.get_cmap("Blues", 8)
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
        axs[i].yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=0))
        axs[i].set_xticks(xs)
        axs[i].set_xticklabels([str(x) for x in xs], fontsize=10)
        axs[i].legend()
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Dijkstra vs Find Min Success Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()
