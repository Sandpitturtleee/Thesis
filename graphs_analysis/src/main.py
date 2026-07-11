from config import GRAPH_RUNS
from graphs_analysis.src.quantum.dijkstra_quantum import run_all_dijkstra_quantum

if __name__ == "__main__":
    print()
    # run_all_dijkstra_heap(times=GRAPH_RUNS)
    # run_all_dijkstra_naive(times=GRAPH_RUNS)
    run_all_dijkstra_quantum(times=GRAPH_RUNS)
