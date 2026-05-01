from data_analysis.src.analysis import plot_dijkstra_counts
from data_analysis.src.helpers import read_results_from_json

if __name__ == "__main__":
    print()
    results = read_results_from_json()
    plot_dijkstra_counts(results)
