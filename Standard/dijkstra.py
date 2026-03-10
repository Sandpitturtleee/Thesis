import heapq

def dijkstra_binheap(graph, start):
    # Inicjalizacja odległości i zbioru odwiedzonych
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    queue = [(0, start)]

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

from fibheap import *

def dijkstra_fibheap(graph, start):
    # Zainicjuj odległości i poprzedników
    distances = {node: float('inf') for node in graph}
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