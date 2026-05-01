"""
Dijkstra Operation Count Plotting Utility
----------------------------------------

This module provides a utility function for plotting the operation counts of Dijkstra's algorithm
for multiple graph types, assuming results are loaded from JSONs of a specific structure.

Functions
---------
- plot_dijkstra_counts: Plot Dijkstra's operation counts for different graph types loaded from result files
"""

import matplotlib.pyplot as plt


def plot_dijkstra_counts(results_dict):
    """
    Plot Dijkstra's algorithm operation counts for different graph types.

    Parameters
    ----------
    results_dict : dict
        Dictionary loaded from your JSON results.
        Keys are filenames (e.g., 'standard_grid.json'), and values are dicts containing:
            - 'vertices': list of number of vertices in the graph
            - 'count': list of operation counts for each graph size
    Returns
    -------
    None

    Displays
    -------
    A matplotlib line plot comparing the operation counts.
    """
    plt.figure(figsize=(10, 7))

    for key, data in results_dict.items():
        label = key.replace("standard_", "").replace(".json", "").capitalize()
        plt.plot(data["vertices"], data["count"], marker="o", label=label)

    plt.xlabel("Graph Size (vertices)")
    plt.ylabel("Operation Count")
    plt.title("Dijkstra's Algorithm Operation Count on Different Graph Types")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
