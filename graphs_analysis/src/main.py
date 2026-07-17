from config import (
    QUANTUM_SAME_GRAPH_TIME_LIMIT_FILENAMES,
    RESULTS_DIRECTORY_QUANTUM_SAME_GRAPH_NO_TIME_LIMIT,
)
from graphs_analysis.src.quantum.dijkstra_quantum import run_all_quantum
from graphs_analysis.src.standard.dijkstra_heap import run_all_dijkstra_heap
from graphs_analysis.src.standard.dijkstra_naive import run_all_dijkstra_naive

if __name__ == "__main__":
    print()
    run_all_dijkstra_heap()
    run_all_dijkstra_naive()

    run_all_quantum()
