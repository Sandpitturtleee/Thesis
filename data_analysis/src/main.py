from config import DIJKSTRA_RESULTS_DIRECTORY, DIJKSTRA_STATS_DIRECTORY
from data_analysis.src.analysis import  statistics_by_file, stats_analysis
from data_analysis.src.helpers import read_results_from_json, save_stats_by_file, read_results_by_vertex
import matplotlib.pyplot as plt

from data_analysis.src.plots import stats_plots_mean, stats_plots_std, stats_plots_mean_combined, \
    stats_plots_std_combined, plot_vertex_counts, stats_plots_median_combined, stats_plots_median, plot_vertices_counts

if __name__ == "__main__":
    print()
    stats_analysis()

    stats_plots_mean()
    #stats_plots_mean_combined()

    # stats_plots_median()
    # stats_plots_median_combined()
    #
    # stats_plots_std()
    # stats_plots_std_combined()

    #plot_vertex_counts(file_name='standard_naive_sparse.json',vertex_number=400)
    # plot_vertices_counts(file_name='standard_naive_sparse.json',vertices_number=[300,400,500])
