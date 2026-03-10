import random

from Data.helpers import save_graph_to_json


def create_frequency():
    frequency = []
    frequency += list(range(0, 101, 10))
    frequency += list(range(200, 1001, 100))
    frequency += list(range(2000, 10001, 1000))
    frequency.pop(0)
    return frequency


def generate_random_graph(num_vertices, min_edges=2, max_edges=5, min_weight=1, max_weight=10):
    nodes = [f"V{i}" for i in range(num_vertices)]
    graph = {node: [] for node in nodes}

    for i, node in enumerate(nodes):
        # Losuj liczbę połączeń (nie więcej niż liczba wierzchołków - 1)
        num_edges = random.randint(min_edges, min(max_edges, num_vertices - 1))
        neighbors = set()
        while len(neighbors) < num_edges:
            neighbor = random.choice(nodes)
            if neighbor != node:
                neighbors.add(neighbor)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            # Dodaj krawędź (nieskierowaną!)
            if (neighbor, weight) not in graph[node]:
                graph[node].append((neighbor, weight))
            if (node, weight) not in graph[neighbor]:
                graph[neighbor].append((node, weight))

    return graph


def generate_graphs():
    frequency = create_frequency()
    for n in frequency:
        graph = generate_random_graph(num_vertices=n)
        save_graph_to_json(graph=graph, name=n)
