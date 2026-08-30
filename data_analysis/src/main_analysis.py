from pprint import pprint

from config import RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT, STATS_DIRECTORY_QUANTUM_TIME_LIMIT, \
    STATS_DIRECTORY_QUANTUM_TIME_LIMIT_COST_COMPARISON
from data_analysis.src.helpers import read_results_from_json
from data_analysis.src.quantum.analysis_quantum import stats_analysis_quantum,\
    save_stats_by_file_quantum_time_limit
from data_analysis.src.quantum.analysis_quantum_prob import prob_stats_quantum_analysis
from data_analysis.src.standard.analysis import stats_analysis_standard


if __name__ == "__main__":
    print()
    #stats_analysis_standard()
    stats_analysis_quantum()
    # prob_stats_quantum_analysis()

