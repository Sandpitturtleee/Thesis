import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

from config import DIJKSTRA_PROB_STATS_DIRECTORY
from data_analysis.src.helpers import read_results_from_json


def plot_all_quantum_prob():
    data = read_results_from_json(directory=DIJKSTRA_PROB_STATS_DIRECTORY)
    plot_grouped_dijkstra_and_find_min_success_prob(all_stats=data)
    # plot_dijkstra_success_prob(all_stats=data)
    # plot_find_min_success_prob(all_stats=data)
    # plot_mismatch_without_invalid_prob(all_stats=data)
    # plot_invalid_when_mismatch_prob(all_stats=data)


def plot_bars_with_percent(ax, xs, ys, ylabel, title, xlabel):
    bars = ax.bar(xs, ys, width=2)
    for bar, y in zip(bars, ys):
        ax.annotate(
            f"{y*100:.1f}%",  # Multiply by 100 for percent annotation
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
    # Use percent format for y-ticks
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=0))
    ax.set_xticks(xs)
    ax.set_xticklabels([str(x) for x in xs], fontsize=10)


def plot_dijkstra_success_prob(all_stats):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    for i, (filename, stat_dict) in enumerate(list(all_stats.items())[:4]):
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["dijkstra_success_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            ylabel="Probability (%)",
            title=filename.replace(".json", ""),
            xlabel="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Dijkstra Success Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


# Repeat similar logic for the other plots:
def plot_find_min_success_prob(all_stats):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    for i, (filename, stat_dict) in enumerate(list(all_stats.items())[:4]):
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["find_min_success_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            ylabel="Probability (%)",
            title=filename.replace(".json", ""),
            xlabel="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Find Min Success Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


def plot_mismatch_without_invalid_prob(all_stats):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    for i, (filename, stat_dict) in enumerate(list(all_stats.items())[:4]):
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["mismatch_without_invalid_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            ylabel="Probability (%)",
            title=filename.replace(".json", ""),
            xlabel="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Mismatch Without Invalid Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


def plot_invalid_when_mismatch_prob(all_stats):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    for i, (filename, stat_dict) in enumerate(list(all_stats.items())[:4]):
        xs = sorted(int(k) for k in stat_dict)
        ys = [stat_dict[str(x)]["invalid_when_mismath_prob"] for x in xs]
        plot_bars_with_percent(
            axs[i],
            xs,
            ys,
            ylabel="Probability (%)",
            title=filename.replace(".json", ""),
            xlabel="Vertices",
        )
    for j in range(i + 1, 4):
        axs[j].axis("off")
    fig.suptitle("Invalid When Mismatch Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()


def plot_grouped_dijkstra_and_find_min_success_prob(all_stats):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    width = 2  # Narrower bars
    sep = 1  # Separation between bars in a group

    for i, (filename, stat_dict) in enumerate(list(all_stats.items())[:4]):
        xs = np.array(sorted(int(k) for k in stat_dict))
        ys1 = [stat_dict[str(x)]["dijkstra_success_prob"] for x in xs]
        ys2 = [stat_dict[str(x)]["find_min_success_prob"] for x in xs]

        # Shift positions for each group
        x1 = xs - width / 2 - sep / 2
        x2 = xs + width / 2 + sep / 2

        bars1 = axs[i].bar(
            x1, ys1, width=width, color="green", label="Dijkstra Success Prob"
        )
        bars2 = axs[i].bar(
            x2, ys2, width=width, color="blue", label="Find Min Success Prob"
        )

        # Annotate with slight horizontal offsets to avoid overlap
        # for bar, y in zip(bars1, ys1):
        #     axs[i].annotate(
        #         f'{y * 100:.1f}%',
        #         xy=(bar.get_x() + bar.get_width() / 2 - sep / 3, y),
        #         xytext=(0, 5),
        #         textcoords="offset points",
        #         ha='center', va='bottom', fontsize=10, color='green'
        #     )
        # for bar, y in zip(bars2, ys2):
        #     axs[i].annotate(
        #         f'{y * 100:.1f}%',
        #         xy=(bar.get_x() + bar.get_width() / 2 + sep / 3, y),
        #         xytext=(0, 5),
        #         textcoords="offset points",
        #         ha='center', va='bottom', fontsize=10, color='blue'
        #     )

        axs[i].set_ylabel("Probability (%)")
        axs[i].set_xlabel("Vertices")
        axs[i].set_title(filename.replace(".json", ""), pad=20)
        axs[i].set_ylim(0, 1)
        axs[i].yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=0))
        axs[i].set_xticks(xs)
        axs[i].set_xticklabels([str(x) for x in xs], fontsize=10)

        axs[i].legend()

    # Turn off extra subplots if less than 4 files
    for j in range(i + 1, 4):
        axs[j].axis("off")

    fig.suptitle("Dijkstra vs Find Min Success Probability")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()
