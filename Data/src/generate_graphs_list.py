import random
from Data.src.helpers import save_graph_to_json_list, create_frequency
from config import RANDOM, WORST_CASE


def generate_random_graph_list(num_vertices, min_weight=1, max_weight=10):
    max_weight = num_vertices
    # adjacency list: vertices 0,1,2,...
    graph = [[] for _ in range(num_vertices)]

    for i in range(num_vertices):
        # Choose a random number of edges for vertex i
        num_edges = random.randint(1, num_vertices - 1)
        neighbors = set()
        while len(neighbors) < num_edges:
            neighbor = random.randint(0, num_vertices - 1)
            if neighbor != i:
                neighbors.add(neighbor)
        for neighbor in neighbors:
            # Assign a random weight
            weight = random.randint(min_weight, max_weight)
            # Only add edge if not already connected (ignore weight for check)
            if neighbor not in [v for v, w in graph[i]]:
                graph[i].append((neighbor, weight))
            if i not in [v for v, w in graph[neighbor]]:
                graph[neighbor].append((i, weight))
    return graph


def generate_random_graph_worst_case_list(num_vertices, min_weight=1, max_weight=10):
    # adjacency list: vertices 0,1,2,...
    graph = [[] for _ in range(num_vertices)]
    for i in range(num_vertices):
        # Connect to all other vertices
        neighbors = set(j for j in range(num_vertices) if j != i)
        for neighbor in neighbors:
            # Assign a random weight
            weight = random.randint(min_weight, max_weight)
            # Only add edge if not already connected (ignore weight for check)
            if neighbor not in [v for v, w in graph[i]]:
                graph[i].append((neighbor, weight))
            if i not in [v for v, w in graph[neighbor]]:
                graph[neighbor].append((i, weight))
    return graph


def generate_graphs_list():
    frequency = create_frequency()
    for i in frequency:
        random_graph = generate_random_graph_list(num_vertices=i)
        worst_case_graph = generate_random_graph_worst_case_list(num_vertices=i)
        save_graph_to_json_list(graph=random_graph, name=f"{i}{RANDOM}")
        save_graph_to_json_list(graph=worst_case_graph, name=f"{i}{WORST_CASE}")