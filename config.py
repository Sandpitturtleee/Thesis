# config.py

MAX_GRAPH_SIZE = 100
GRAPH_RUNS = 2
SPARSE = "_sparse"
HALF_EDGES = "_half_edges"
DENSE = "_dense"
SPECIAL_CASE = "_special_case"

DATA_DIRECTORY = "data"
GENERATED_GRAPHS_DIRECTORY = "generated_graphs"

RESULTS_DIRECTORY_STANDARD_HEAP = "dijkstra_results/standard/heap"
RESULTS_DIRECTORY_STANDARD_NAIVE = "dijkstra_results/standard/naive"
RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT = "dijkstra_results/quantum/time_limit"
RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT = "dijkstra_results/quantum/no_time_limit"

STATS_DIRECTORY_STANDARD_HEAP = "dijkstra_stats/standard/heap"
STATS_DIRECTORY_STANDARD_NAIVE = "dijkstra_stats/standard/naive"
STATS_DIRECTORY_QUANTUM_TIME_LIMIT = "dijkstra_stats/quantum/time_limit"
STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT = "dijkstra_stats/quantum/no_time_limit"
STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT = "dijkstra_stats/quantum_prob/time_limit"
STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT = "dijkstra_stats/quantum_prob/no_time_limit"


STANDARD_HEAP_SPARSE_FILENAME = "standard_heap_sparse"
STANDARD_HEAP_HALF_EDGES_FILENAME = "standard_heap_half_edges"
STANDARD_HEAP_DENSE_FILENAME = "standard_heap_dense"
STANDARD_HEAP_SPECIAL_CASE_FILENAME = "standard_heap_special_case"
STANDARD_NAIVE_SPARSE_FILENAME = "standard_naive_sparse"
STANDARD_NAIVE_HALF_EDGES_FILENAME = "standard_naive_half_edges"
STANDARD_NAIVE_DENSE_FILENAME = "standard_naive_dense"
STANDARD_NAIVE_SPECIAL_CASE_FILENAME = "standard_naive_special_case"

QUANTUM_TIME_LIMIT_SPARSE_FILENAME = "quantum_time_limit_sparse"
QUANTUM_TIME_LIMIT_HALF_EDGES_FILENAME = "quantum_time_limit_half_edges"
QUANTUM_TIME_LIMIT_DENSE_FILENAME = "quantum_time_limit_dense"
QUANTUM_TIME_LIMIT_SPECIAL_CASE_FILENAME = "quantum_time_limit_special_case"
QUANTUM_NO_TIME_LIMIT_SPARSE_FILENAME = "quantum_no_time_limit_sparse"
QUANTUM_NO_TIME_LIMIT_HALF_EDGES_FILENAME = "quantum_no_time_limit_half_edges"
QUANTUM_NO_TIME_LIMIT_DENSE_FILENAME = "quantum_time_no_limit_dense"
QUANTUM_NO_TIME_LIMIT_SPECIAL_CASE_FILENAME = "quantum_no_time_limit_special_case"
