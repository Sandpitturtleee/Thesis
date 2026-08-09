# config.py

import matplotlib.pyplot as plt

MAX_GRAPH_SIZE = 100
GRAPH_RUNS = 100
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
RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_TIME_LIMIT = (
    "dijkstra_results/quantum/same_graph_time_limit"
)
RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT = (
    "dijkstra_results/quantum/same_graph_no_time_limit"
)

STATS_DIRECTORY_STANDARD_HEAP = "dijkstra_stats/standard/heap"
STATS_DIRECTORY_STANDARD_NAIVE = "dijkstra_stats/standard/naive"

STATS_DIRECTORY_QUANTUM_TIME_LIMIT = "dijkstra_stats/quantum/time_limit"
STATS_DIRECTORY_QUANTUM_NO_TIME_LIMIT = "dijkstra_stats/quantum/no_time_limit"
STATS_DIRECTORY_QUANTUM_PROB_TIME_LIMIT = "dijkstra_stats/quantum_prob/time_limit"
STATS_DIRECTORY_QUANTUM_PROB_NO_TIME_LIMIT = "dijkstra_stats/quantum_prob/no_time_limit"
STATS_DIRECTORY_SAME_GRAPH_QUANTUM_TIME_LIMIT = (
    "dijkstra_stats/quantum/same_graph_time_limit"
)
STATS_DIRECTORY_SAME_GRAPH_QUANTUM_NO_TIME_LIMIT = (
    "dijkstra_stats/quantum/same_graph_no_time_limit"
)
STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_TIME_LIMIT = (
    "dijkstra_stats/quantum_prob/same_graph_time_limit"
)
STATS_DIRECTORY_SAME_GRAPH_QUANTUM_PROB_NO_TIME_LIMIT = (
    "dijkstra_stats/quantum_prob/same_graph_no_time_limit"
)


STANDARD_HEAP_SPARSE_FILENAME = "standard_heap_sparse"
STANDARD_HEAP_HALF_EDGES_FILENAME = "standard_heap_half_edges"
STANDARD_HEAP_DENSE_FILENAME = "standard_heap_dense"
STANDARD_HEAP_SPECIAL_CASE_FILENAME = "standard_heap_special_case"
STANDARD_HEAP_FILENAMES = [
    STANDARD_HEAP_SPARSE_FILENAME,
    STANDARD_HEAP_HALF_EDGES_FILENAME,
    STANDARD_HEAP_DENSE_FILENAME,
    STANDARD_HEAP_SPECIAL_CASE_FILENAME,
]

STANDARD_NAIVE_SPARSE_FILENAME = "standard_naive_sparse"
STANDARD_NAIVE_HALF_EDGES_FILENAME = "standard_naive_half_edges"
STANDARD_NAIVE_DENSE_FILENAME = "standard_naive_dense"
STANDARD_NAIVE_SPECIAL_CASE_FILENAME = "standard_naive_special_case"
STANDARD_NAIVE_FILENAMES = [
    STANDARD_NAIVE_SPARSE_FILENAME,
    STANDARD_NAIVE_HALF_EDGES_FILENAME,
    STANDARD_NAIVE_DENSE_FILENAME,
    STANDARD_NAIVE_SPECIAL_CASE_FILENAME,
]

QUANTUM_TIME_LIMIT_SPARSE_FILENAME = "quantum_time_limit_sparse"
QUANTUM_TIME_LIMIT_HALF_EDGES_FILENAME = "quantum_time_limit_half_edges"
QUANTUM_TIME_LIMIT_DENSE_FILENAME = "quantum_time_limit_dense"
QUANTUM_TIME_LIMIT_SPECIAL_CASE_FILENAME = "quantum_time_limit_special_case"
QUANTUM_TIME_LIMIT_FILENAMES = [
    QUANTUM_TIME_LIMIT_SPARSE_FILENAME,
    QUANTUM_TIME_LIMIT_HALF_EDGES_FILENAME,
    QUANTUM_TIME_LIMIT_DENSE_FILENAME,
    QUANTUM_TIME_LIMIT_SPECIAL_CASE_FILENAME,
]

QUANTUM_NO_TIME_LIMIT_SPARSE_FILENAME = "quantum_no_time_limit_sparse"
QUANTUM_NO_TIME_LIMIT_HALF_EDGES_FILENAME = "quantum_no_time_limit_half_edges"
QUANTUM_NO_TIME_LIMIT_DENSE_FILENAME = "quantum_no_time_limit_dense"
QUANTUM_NO_TIME_LIMIT_SPECIAL_CASE_FILENAME = "quantum_no_time_limit_special_case"
QUANTUM_NO_TIME_LIMIT_FILENAMES = [
    QUANTUM_NO_TIME_LIMIT_SPARSE_FILENAME,
    QUANTUM_NO_TIME_LIMIT_HALF_EDGES_FILENAME,
    QUANTUM_NO_TIME_LIMIT_DENSE_FILENAME,
    QUANTUM_NO_TIME_LIMIT_SPECIAL_CASE_FILENAME,
]

QUANTUM_SAME_GRAPH_TIME_LIMIT_SPARSE_FILENAME = "quantum_same_graph_time_limit_sparse"
QUANTUM_SAME_GRAPH_TIME_LIMIT_HALF_EDGES_FILENAME = (
    "quantum_same_graph_time_limit_half_edges"
)
QUANTUM_SAME_GRAPH_TIME_LIMIT_DENSE_FILENAME = "quantum_same_graph_time_limit_dense"
QUANTUM_SAME_GRAPH_TIME_LIMIT_SPECIAL_CASE_FILENAME = (
    "quantum_same_graph_time_limit_special_case"
)
QUANTUM_SAME_GRAPH_TIME_LIMIT_FILENAMES = [
    QUANTUM_SAME_GRAPH_TIME_LIMIT_SPARSE_FILENAME,
    QUANTUM_SAME_GRAPH_TIME_LIMIT_HALF_EDGES_FILENAME,
    QUANTUM_SAME_GRAPH_TIME_LIMIT_DENSE_FILENAME,
    QUANTUM_SAME_GRAPH_TIME_LIMIT_SPECIAL_CASE_FILENAME,
]

QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_SPARSE_FILENAME = (
    "quantum_same_graph_no_time_limit_sparse"
)
QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_HALF_EDGES_FILENAME = (
    "quantum_same_graph_no_time_limit_half_edges"
)
QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_DENSE_FILENAME = (
    "quantum_same_graph_time_no_limit_dense"
)
QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_SPECIAL_CASE_FILENAME = (
    "quantum_same_graph_no_time_limit_special_case"
)
QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_FILENAMES = [
    QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_SPARSE_FILENAME,
    QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_HALF_EDGES_FILENAME,
    QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_DENSE_FILENAME,
    QUANTUM_SAME_GRAPH_NO_TIME_LIMIT_SPECIAL_CASE_FILENAME,
]

cmap = plt.get_cmap("Blues", 8)
COLOR_MAP = {
    "sparse": cmap(3),
    "half_edges": cmap(5),
    "dense": cmap(7),
    "special_case": "red",
}
GRAPH_LABELS_MAP = {
    "sparse": "Graf rzadki",
    "half_edges": "Graf średnio gęsty",
    "dense": "Graf gęsty",
    "special_case": "Przypadek szczególny",

    "standard_naive_sparse": "Wersja naiwna",
    "standard_heap_sparse": "Wersja z kopcem binarnym",

    "standard_naive_half_edges": "Wersja naiwna",
    "standard_heap_half_edges": "Wersja z kopcem binarnym",

    "standard_naive_dense": "Wersja naiwna",
    "standard_heap_dense": "Wersja z kopcem binarnym",

    "standard_naive_special_case": "Wersja naiwna",
    "standard_heap_special_case": "Wersja z kopcem binarnym",

    "quantum_no_time_limit_sparse": "Wersja kwantowa z limitem",
    "quantum_time_limit_sparse": "Wersja kwantowa bez limitu",

    "quantum_no_time_limit_half_edges": "Wersja kwantowa z limitem",
    "quantum_time_limit_half_edges": "Wersja kwantowa bez limitu",

    "quantum_no_time_limit_dense": "Wersja kwantowa z limitem",
    "quantum_time_limit_dense": "Wersja kwantowa bez limitu",

    "quantum_no_time_limit_special_case": "Wersja kwantowa z limitem",
    "quantum_time_limit_special_case": "Wersja kwantowa bez limitu",
}

STAT_NAME_MAP = {
    "mean": "Średnia",
    "median": "Mediana",
    "std": "Odchylenie standardowe",
}

VERTICES_X_PLOT_LABEL = "Liczba wierzchołków"
LEGEND_ORDER = ["sparse", "half_edges", "dense", "special_case"]


PLOT_TITLE_TYPE_TIME_LIMIT = "z limitem czasowym"
PLOT_TITLE_TYPE_NO_TIME_LIMIT = "bez limitu czasowego"
PLOT_TITLE_SAME_GRAPH_TYPE_TIME_LIMIT = "ten sam graf z limitem czasowym"
PLOT_TITLE_SAME_GRAPH_TYPE_NO_TIME_LIMIT = "ten sam bez limitu czasowego"

GRAPH_TYPES_MAPPING = [
    ("Graf rzadki", "sparse", plt.get_cmap("Blues")),
    ("Graf średnio gęsty", "half_edges", plt.get_cmap("Blues")),
    ("Graf gęsty", "dense", plt.get_cmap("Blues")),
    ("Przypadek szczególny", "special_case", plt.get_cmap("Reds")),
]
