import random
from Data.src.helpers import save_graph_to_json_dict, create_frequency
from config import RANDOM, WORST_CASE


def generate_random_graph_dict(num_vertices, min_weight=1, max_weight=10):
    max_weight = num_vertices
    nodes = [f"V{i}" for i in range(num_vertices)]
    graph = {node: [] for node in nodes}

    for i, node in enumerate(nodes):
        # Losuj liczbę połączeń (1 <= x <= liczba wierzchołków - 1)
        num_edges = random.randint(1, num_vertices - 1)
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


def generate_random_graph_worst_case_dict(num_vertices, min_weight=1, max_weight=10):
    nodes = [f"V{i}" for i in range(num_vertices)]
    graph = {node: [] for node in nodes}

    for i, node in enumerate(nodes):
        # Losuj połączen tyle co liczba wierzchołków
        num_edges = num_vertices
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


def generate_graphs_dict():
    frequency = create_frequency()
    for i in frequency:
        random_graph = generate_random_graph_dict(num_vertices=i)
        worst_case_graph = generate_random_graph_dict(num_vertices=i)
        save_graph_to_json_dict(graph=random_graph, name=f"{i}{RANDOM}")
        save_graph_to_json_dict(graph=worst_case_graph, name=f"{i}{WORST_CASE}")
