from config import DIJKSTRA_RESULTS_DIRECTORY
from data_analysis.src.analysis import stats_analysis
from data_analysis.src.analysis_prob import prob_stats_analysis
from data_analysis.src.helpers import read_results_from_json
from data_analysis.src.plots_combined import plot_all_combined
from data_analysis.src.plots_other import plot_all_other
from data_analysis.src.plots_quantum import plot_all_quantum
from data_analysis.src.plots_quantum_prob import plot_all_quantum_prob
from data_analysis.src.plots_standard import plot_all_standard

if __name__ == "__main__":
    print()
    # stats_analysis()
    # prob_stats_analysis()
    #
    # plot_all_standard()
    # plot_all_quantum()
    # plot_all_combined()
    # plot_all_other()

    plot_all_quantum_prob()
