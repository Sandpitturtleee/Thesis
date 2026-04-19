import random
from typing import Dict, List, Tuple

from config import RANDOM, WORST_CASE
from Data.src.helpers import create_frequency, save_graph_to_json_dict

GraphDict = Dict[str, List[Tuple[str, int]]]


def generate_random_graph_dict(num_vertices: int, min_weight: int = 1) -> GraphDict:
    max_weight = num_vertices
    nodes = [f"V{i}" for i in range(num_vertices)]
    graph = {node: [] for node in nodes}

    for i, node in enumerate(nodes):
        num_edges = random.randint(1, num_vertices - 1)
        neighbors = set()
        while len(neighbors) < num_edges:
            neighbor = random.choice(nodes)
            if neighbor != node:
                neighbors.add(neighbor)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            if (neighbor, weight) not in graph[node]:
                graph[node].append((neighbor, weight))
            if (node, weight) not in graph[neighbor]:
                graph[neighbor].append((node, weight))

    return graph


def generate_random_graph_worst_case_dict(
    num_vertices: int, min_weight: int = 1, max_weight: int = 10
) -> GraphDict:
    nodes = [f"V{i}" for i in range(num_vertices)]
    graph = {node: [] for node in nodes}

    for i, node in enumerate(nodes):
        num_edges = num_vertices
        neighbors = set()
        while len(neighbors) < num_edges:
            neighbor = random.choice(nodes)
            if neighbor != node:
                neighbors.add(neighbor)
        for neighbor in neighbors:
            weight = random.randint(min_weight, max_weight)
            if (neighbor, weight) not in graph[node]:
                graph[node].append((neighbor, weight))
            if (node, weight) not in graph[neighbor]:
                graph[neighbor].append((node, weight))

    return graph


def generate_graphs_dict() -> None:
    frequency = create_frequency()
    for i in frequency:
        random_graph = generate_random_graph_dict(num_vertices=i)
        worst_case_graph = generate_random_graph_dict(num_vertices=i)
        save_graph_to_json_dict(graph=random_graph, name=f"{i}{RANDOM}")
        save_graph_to_json_dict(graph=worst_case_graph, name=f"{i}{WORST_CASE}")
