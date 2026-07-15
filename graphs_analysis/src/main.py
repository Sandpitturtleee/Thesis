from config import GRAPH_RUNS, RESULTS_DIRECTORY, RESULTS_DIRECTORY_NO_LIMIT
from graphs_analysis.src.quantum.dijkstra_quantum import run_all_dijkstra_quantum

if __name__ == "__main__":
    print()
    # run_all_dijkstra_heap(times=GRAPH_RUNS)
    # run_all_dijkstra_naive(times=GRAPH_RUNS)
    run_all_dijkstra_quantum(times=GRAPH_RUNS,directory=RESULTS_DIRECTORY,time_limit=1) #With time limit
    # run_all_dijkstra_quantum(
    #     times=GRAPH_RUNS, directory=RESULTS_DIRECTORY_NO_LIMIT, time_limit=0
    # )  # No time limit
