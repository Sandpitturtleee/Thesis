import random
from typing import List, Tuple

from config import RANDOM, WORST_CASE
from Data.src.helpers import create_frequency, save_graph_to_json_list

GraphList = List[List[Tuple[int, int]]]


def generate_random_graph_list(num_vertices: int, min_weight: int = 1) -> GraphList:
    max_weight = num_vertices
    graph = [[] for _ in range(num_vertices)]

    for i in range(num_vertices):
        num_edges = random.randint(1, num_vertices - 1)
        neighbors = set()
        while len(neighbors) < num_edges:
            neighbor = random.randint(0, num_vertices - 1)
            if neighbor != i:
                neighbors.add(neighbor)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            if neighbor not in [v for v, w in graph[i]]:
                graph[i].append((neighbor, weight))
            if i not in [v for v, w in graph[neighbor]]:
                graph[neighbor].append((i, weight))
    return graph


def generate_random_graph_worst_case_list(
    num_vertices: int, min_weight: int = 1, max_weight: int = 10
) -> GraphList:
    graph = [[] for _ in range(num_vertices)]
    for i in range(num_vertices):
        neighbors = set(j for j in range(num_vertices) if j != i)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            if neighbor not in [v for v, w in graph[i]]:
                graph[i].append((neighbor, weight))
            if i not in [v for v, w in graph[neighbor]]:
                graph[neighbor].append((i, weight))
    return graph


def generate_graphs_list() -> None:
    frequency = create_frequency()
    for i in frequency:
        random_graph = generate_random_graph_list(num_vertices=i)
        worst_case_graph = generate_random_graph_worst_case_list(num_vertices=i)
        save_graph_to_json_list(graph=random_graph, name=f"{i}{RANDOM}")
        save_graph_to_json_list(graph=worst_case_graph, name=f"{i}{WORST_CASE}")
