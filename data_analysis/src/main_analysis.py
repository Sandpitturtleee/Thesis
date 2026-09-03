from data_analysis.src.quantum.analysis_quantum import stats_analysis_quantum
from data_analysis.src.quantum.analysis_quantum_prob import \
    prob_stats_quantum_analysis
from data_analysis.src.standard.analysis import stats_analysis_standard

if __name__ == "__main__":
    print()
    stats_analysis_standard()
    stats_analysis_quantum()
    prob_stats_quantum_analysis()
