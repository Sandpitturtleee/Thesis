from config import (
    GRAPH_RUNS,
    RESULTS_DIRECTORY_NO_LIMIT,
    RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
    RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT,
    RESULTS_DIRECTORY_STANDARD_HEAP,
    RESULTS_DIRECTORY_STANDARD_NAIVE,
)
from graphs_analysis.src.quantum.dijkstra_quantum import run_all_dijkstra_quantum
from graphs_analysis.src.standard.dijkstra_heap import run_all_dijkstra_heap
from graphs_analysis.src.standard.dijkstra_naive import run_all_dijkstra_naive

if __name__ == "__main__":
    print()
    # run_all_dijkstra_heap(times=GRAPH_RUNS,directory=RESULTS_DIRECTORY_STANDARD_HEAP)
    # run_all_dijkstra_naive(times=GRAPH_RUNS,directory=RESULTS_DIRECTORY_STANDARD_NAIVE)

    run_all_dijkstra_quantum(
        times=GRAPH_RUNS, directory=RESULTS_DIRECTORY_QUANTUM_TIME_LIMIT, time_limit=1
    )  # With time limit
    run_all_dijkstra_quantum(
        times=GRAPH_RUNS,
        directory=RESULTS_DIRECTORY_QUANTUM_NO_TIME_LIMIT,
        time_limit=0,
    )  # No time limit
