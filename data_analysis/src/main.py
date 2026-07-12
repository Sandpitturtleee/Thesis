from data_analysis.src.analysis import stats_analysis
from data_analysis.src.plots_combined import plot_all_combined
from data_analysis.src.plots_other import plot_all_other
from data_analysis.src.plots_quantum import plot_all_quantum
from data_analysis.src.plots_standard import plot_all_standard

if __name__ == "__main__":
    print()
    stats_analysis()

    plot_all_standard()
    plot_all_quantum()
    plot_all_combined()
    plot_all_other()
