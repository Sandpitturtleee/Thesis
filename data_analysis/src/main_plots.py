from data_analysis.src.plots_combined import (plot_quantum_combined,
                                              plot_quantum_same_graph_combined,
                                              plot_standard_combined,
                                              plot_standard_quantum_combined)
from data_analysis.src.plots_other import plot_all_other
from data_analysis.src.quantum.plots_quantum import (
    plot_all_quantum_no_time_limit, plot_all_quantum_same_graph_no_time_limit,
    plot_all_quantum_same_graph_time_limit, plot_all_quantum_time_limit,
    plot_quantum_same_graph_time_limit_vs_no_time_limit_all,
    plot_quantum_time_limit_vs_no_time_limit_all, plot_quantum_time_limit_cost_comparison_all)
from data_analysis.src.quantum.plots_quantum_prob import (
    plot_all_quantum_prob_no_time_limit,
    plot_all_quantum_prob_same_graph_no_time_limit,
    plot_all_quantum_prob_same_graph_time_limit,
    plot_all_quantum_prob_time_limit)
from data_analysis.src.standard.plots_standard import (plot_all_heap,
                                                       plot_all_naive,
                                                       plot_naive_vs_heap_all)

if __name__ == "__main__":
    print()
    #
    # plot_all_naive()
    # plot_all_heap()
    # plot_naive_vs_heap_all()
    # plot_standard_combined()
    #
    plot_quantum_time_limit_cost_comparison_all()
    # plot_all_quantum_time_limit() #!
    # plot_all_quantum_no_time_limit() #!
    # plot_quantum_time_limit_vs_no_time_limit_all() #!
    #
    # plot_quantum_combined()
    #
    # plot_standard_quantum_combined()

    # plot_all_other()
    #
    # plot_all_quantum_prob_time_limit()
    # plot_all_quantum_prob_no_time_limit()

    # plot_all_quantum_same_graph_time_limit()
    # plot_all_quantum_same_graph_no_time_limit()
    # plot_quantum_same_graph_combined()
    # plot_quantum_same_graph_time_limit_vs_no_time_limit_all()
    # plot_all_quantum_prob_same_graph_time_limit()
    # plot_all_quantum_prob_same_graph_no_time_limit()
