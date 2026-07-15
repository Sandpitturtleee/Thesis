from data_analysis.src.quantum.analysis import stats_analysis_quantum
from data_analysis.src.quantum.analysis_prob import prob_stats_quantum_analysis
from data_analysis.src.standard.analysis import stats_analysis_standard

if __name__ == "__main__":
    print()
    stats_analysis_standard()
    stats_analysis_quantum()

    prob_stats_quantum_analysis()
    # #
    # # #plot_all_standard()
    # plot_all_quantum(directory=DIJKSTRA_STATS_DIRECTORY)
    # # plot_all_combined()
    # # # plot_all_other()
    # # #
    # # plot_all_quantum_prob(directory=DIJKSTRA_PROB_STATS_DIRECTORY)
    # # dijkstra_results = read_results_from_json(directory=RESULTS_DIRECTORY_NO_LIMIT)
    # # quantum_stats = statistics_by_file_quantum(dijkstra_results)
    # # print(quantum_stats)
    # # save_stats_by_file_quantum(stats_by_file=quantum_stats,directory=DIJKSTRA_STATS_NO_LIMIT_DIRECTORY)
    # # prob_stats_analysis(input_directory=RESULTS_DIRECTORY_NO_LIMIT,output_directory=DIJKSTRA_PROB_STATS_NO_LIMIT_DIRECTORY)
    # # plot_all_quantum_prob(directory=DIJKSTRA_PROB_STATS_NO_LIMIT_DIRECTORY)
    # # #
    # plot_all_quantum(directory=DIJKSTRA_STATS_NO_LIMIT_DIRECTORY)
