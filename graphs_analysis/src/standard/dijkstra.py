from config import (
    RANDOM,
    RESULTS_DIRECTORY,
    STANDARD_RANDOM_FILENAME,
    STANDARD_WORSTCASE_FILENAME,
    WORSTCASE,
)
from graphs_analysis.src.helpers import (
    create_frequency,
    load_graph_from_json_list,
    save_results_to_json,
)
from graphs_analysis.src.standard.heap import MinHeap


def run_all(times):
    vertices, count = run_dijkstra_heap(times=times, graph_type=RANDOM)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_RANDOM_FILENAME,
        vertices=vertices,
        count=count,
    )
    vertices, count = run_dijkstra_heap(times=times, graph_type=WORST_CASE)
    save_results_to_json(
        directory=RESULTS_DIRECTORY,
        name=STANDARD_WORSTCASE_FILENAME,
        vertices=vertices,
        count=count,
    )


def dijkstra_heap(graph, start_node):
    n = len(graph)
    distances = [float("inf")] * n
    previous = [None] * n
    in_heap = [True] * n

    heap = MinHeap()
    for node in range(n):
        heap.push(float("inf"), node)
    heap.decrease_key(start_node, 0)
    distances[start_node] = 0

    while not heap.is_empty():
        dist_u, u = heap.pop()
        in_heap[u] = False

        for v, weight in graph[u]:
            if in_heap[v]:
                new_distance = distances[u] + weight
                if new_distance < distances[v]:
                    distances[v] = new_distance
                    previous[v] = u
                    heap.decrease_key(v, new_distance)
    return distances, previous, heap.total()


def run_dijkstra_heap(times, graph_type):
    vertices = create_frequency()
    count = []

    for i in vertices:
        loaded_graph = load_graph_from_json_list(name=f"{i}{graph_type}")
        elapsed_sum = 0
        for _ in range(times):
            _, _, elapsed = dijkstra_heap(graph=loaded_graph, start_node=0)
            elapsed_sum += elapsed
        mean = elapsed_sum / times
        count.append(mean)

    return vertices, count
