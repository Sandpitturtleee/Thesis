from config import GRAPH_RUNS
from graphs_analysis.src.standard.dijkstra_heap import run_all_dijkstra_heap
from graphs_analysis.src.standard.dijkstra_naive import run_all_dijkstra_naive

if __name__ == "__main__":
    print()
    run_all_dijkstra_heap(times=GRAPH_RUNS)
    run_all_dijkstra_naive(times=GRAPH_RUNS)
