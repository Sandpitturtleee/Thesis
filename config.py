# config.py

MAX_GRAPH_SIZE = 100
GRAPH_RUNS = 100
SPARSE = "_sparse"
HALF_EDGES = "_half_edges"
DENSE = "_dense"
WORSTCASE = "_worstcase"

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
STANDARD_HEAP_WORSTCASE_FILENAME = "standard_heap_worstcase"

STANDARD_NAIVE_SPARSE_FILENAME = "standard_naive_sparse"
STANDARD_NAIVE_HALF_EDGES_FILENAME = "standard_naive_half_edges"
STANDARD_NAIVE_DENSE_FILENAME = "standard_naive_dense"
STANDARD_NAIVE_WORSTCASE_FILENAME = "standard_naive_worstcase"

QUANTUM_SPARSE_FILENAME = "quantum_sparse"
QUANTUM_HALF_EDGES_FILENAME = "quantum_half_edges"
QUANTUM_DENSE_FILENAME = "quantum_dense"
QUANTUM_WORSTCASE_FILENAME = "quantum_worstcase"


DIJKSTRA_STATS_DIRECTORY = "dijkstra_stats"
DIJKSTRA_STATS_NO_LIMIT_DIRECTORY = "dijkstra_stats_no_limit"
DIJKSTRA_PROB_STATS_DIRECTORY = "dijkstra_prob_stats"
DIJKSTRA_PROB_STATS_NO_LIMIT_DIRECTORY = "dijkstra_prob_stats_no_limit"


RESULTS_DIRECTORY_NO_LIMIT = "dijkstra_results_no_limit"
