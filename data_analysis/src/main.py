from data_analysis.src.plots_combined import (
    plot_quantum_combined,
    plot_standard_combined,
    plot_standard_quantum_combined,
)
from data_analysis.src.plots_other import plot_all_other
from data_analysis.src.quantum.analysis import stats_analysis_quantum
from data_analysis.src.quantum.analysis_prob import prob_stats_quantum_analysis
from data_analysis.src.quantum.plots_quantum import (
    plot_all_quantum_no_time_limit,
    plot_all_quantum_time_limit,
)
from data_analysis.src.quantum.plots_quantum_prob import (
    plot_all_quantum_prob_no_time_limit,
    plot_all_quantum_prob_time_limit,
)
from data_analysis.src.standard.analysis import stats_analysis_standard
from data_analysis.src.standard.plots_standard import plot_all_heap, plot_all_naive

if __name__ == "__main__":
    print()
    # stats_analysis_standard()
    stats_analysis_quantum()
    prob_stats_quantum_analysis()
    #
    # plot_all_naive()
    # plot_all_heap()
    # plot_standard_combined()
    #
    # plot_all_quantum_time_limit()
    # plot_all_quantum_no_time_limit()
    # plot_quantum_combined()

    # plot_standard_quantum_combined()

    # plot_all_other()
    #
    # plot_all_quantum_prob_time_limit()
    # plot_all_quantum_prob_no_time_limit()
