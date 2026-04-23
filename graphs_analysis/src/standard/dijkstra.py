import heapq

import matplotlib.pyplot as plt
from fibheap import *

from config import RANDOM, WORST_CASE
from graphs_analysis.src.helpers import (
    create_frequency,
    load_graph_from_json_dict,
    timing_decorator,
)


@timing_decorator
def dijkstra_binary_heap(graph, start_node):
    # Inicjalizacja odległości i zbioru odwiedzonych
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start_node] = 0
    queue = [(0, start_node)]
    while queue:
        dist_u, u = heapq.heappop(queue)
        # Jeśli znaleźliśmy już krótszą drogę - pomijamy
        if dist_u > distances[u]:
            continue
        for v, weight in graph[u]:
            new_distance = distances[u] + weight
            if new_distance < distances[v]:
                distances[v] = new_distance
                previous[v] = u
                heapq.heappush(queue, (new_distance, v))

    return distances, previous


def run_dijkstra_binary_heap(graph, start_node, times):
    elapsed_sum = 0
    for i in range(times):
        (results, elapsed) = dijkstra_binary_heap(graph=graph, start_node=start_node)
        elapsed_sum += elapsed
    mean = elapsed_sum / times
    return mean


@timing_decorator
def dijkstra_fibheap(graph, start):
    # Zainicjuj odległości i poprzedników
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    # Stwórz kopiec
    heap = Fheap()
    heap_nodes = {}

    # Dodaj wszystkie wierzchołki do kopca (z odległościami)
    for node in graph:
        nd = Node(distances[node])
        heap.insert(nd)
        heap_nodes[node] = nd

    while heap.min is not None:
        # Pobierz wierzchołek o minimalnej odległości
        min_node = heap.extract_min()
        # Musimy znaleźć który to klucz (w grafie)
        # (możliwa jest sytuacja kilku wierzchołków o tej samej wartości)
        u = None
        for k, n in heap_nodes.items():
            if n is min_node:
                u = k
                break
        if u is None:
            continue  # nie powinno się zdarzyć

        for v, weight in graph[u]:
            alt = distances[u] + weight
            if alt < distances[v]:
                distances[v] = alt
                previous[v] = u
                heap.decrease_key(heap_nodes[v], alt)

    return distances, previous


def run_for_multiple_json(times):
    frequency = create_frequency()
    print(frequency)
    times_random = []
    times_worst = []
    for i in frequency:
        loaded_graph_random = load_graph_from_json_dict(name=f"{i}{RANDOM}")
        loaded_graph_worst_case = load_graph_from_json_dict(name=f"{i}{WORST_CASE}")
        result1 = run_dijkstra_binary_heap(
            graph=loaded_graph_random, start_node="V0", times=times
        )
        result2 = run_dijkstra_binary_heap(
            graph=loaded_graph_worst_case, start_node="V0", times=times
        )
        times_random.append(result1)
        times_worst.append(result2)
    plt.figure(figsize=(8, 6))
    plt.plot(frequency, times_random, marker="o", label="Random graphs")
    plt.plot(frequency, times_worst, marker="s", label="Worst-case graphs")
    plt.xlabel("Graph Size")
    plt.ylabel("Elapsed Time [s]")
    plt.title("Dijkstra Algorithm Performance")
    plt.legend()
    plt.grid(True)
    plt.show()
