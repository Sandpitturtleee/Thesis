from config import (
    DIJKSTRA_PROB_STATS_DIRECTORY,
    DIJKSTRA_PROB_STATS_NO_LIMIT_DIRECTORY,
    DIJKSTRA_RESULTS_DIRECTORY,
    DIJKSTRA_STATS_DIRECTORY,
    DIJKSTRA_STATS_NO_LIMIT_DIRECTORY,
    RESULTS_DIRECTORY_NO_LIMIT,
)
from data_analysis.src.analysis import statistics_by_file_quantum, stats_analysis
from data_analysis.src.analysis_prob import prob_stats_analysis
from data_analysis.src.helpers import read_results_from_json, save_stats_by_file_quantum
from data_analysis.src.plots_combined import plot_all_combined
from data_analysis.src.plots_other import plot_all_other
from data_analysis.src.plots_quantum import plot_all_quantum
from data_analysis.src.plots_quantum_prob import plot_all_quantum_prob
from data_analysis.src.plots_standard import plot_all_standard

if __name__ == "__main__":
    print()
    # stats_analysis()
    # prob_stats_analysis(input_directory=DIJKSTRA_RESULTS_DIRECTORY,output_directory=DIJKSTRA_PROB_STATS_DIRECTORY)
    #
    # #plot_all_standard()
    plot_all_quantum(directory=DIJKSTRA_STATS_DIRECTORY)
    # plot_all_combined()
    # # plot_all_other()
    # #
    # plot_all_quantum_prob(directory=DIJKSTRA_PROB_STATS_DIRECTORY)
    # dijkstra_results = read_results_from_json(directory=RESULTS_DIRECTORY_NO_LIMIT)
    # quantum_stats = statistics_by_file_quantum(dijkstra_results)
    # print(quantum_stats)
    # save_stats_by_file_quantum(stats_by_file=quantum_stats,directory=DIJKSTRA_STATS_NO_LIMIT_DIRECTORY)
    # prob_stats_analysis(input_directory=RESULTS_DIRECTORY_NO_LIMIT,output_directory=DIJKSTRA_PROB_STATS_NO_LIMIT_DIRECTORY)
    # plot_all_quantum_prob(directory=DIJKSTRA_PROB_STATS_NO_LIMIT_DIRECTORY)
    # #
    plot_all_quantum(directory=DIJKSTRA_STATS_NO_LIMIT_DIRECTORY)
