"""
Graph Handling Utilities
------------------------

This module provides utility functions for saving/loading graphs (in dictionary or adjacency list format) as JSON files,
managing file paths, measuring function execution time, and constructing useful sizes for batch graph generation.

Functions:
----------
- create_file_path: Create and return a JSON file path for persisting graph data.
- save_graph_to_json_dict: Save a dictionary-format graph as a compact JSON file.
- save_graph_to_json_list: Save a list-format (adjacency list) graph as a pretty-printed JSON array.
- load_graph_from_json_dict: Load and convert a dictionary-format graph from a JSON file.
- timing_decorator: Decorator for measuring the execution time of any function.
- create_frequency: Generate a list of sizes for graph generation batches.

Types:
------
- GraphDict: type alias for Dict[str, List[Tuple[str, int]]]
- GraphList: type alias for List[List[Tuple[int, int]]]
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

GraphDict = Dict[str, List[Tuple[str, int]]]
GraphList = List[List[Tuple[int, int]]]


# TODO load_graph_from_json_LIST with test
def create_file_path(name: str) -> Path:
    """
    Create the appropriate file path for saving or loading a graph's JSON file by name.

    The file will be placed in ../data/json/ relative to this file.

    Parameters
    ----------
    name : str
        The base name (without extension) for the JSON file.

    Returns
    -------
    Path
        The full path to the target JSON file.
    """
    base_path = Path(__file__).parent.parent / "json"
    base_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.json"
    file_path = base_path / file_name
    return file_path


def save_graph_to_json_dict(graph: GraphDict, name: str) -> None:
    """
    Save a graph (in dictionary adjacency format) as a compact JSON file.

    Parameters
    ----------
    graph : GraphDict
        The graph to be saved, mapping node str -> list of (neighbor str, weight int).
    name : str
        The base file name (without extension).

    Returns
    -------
    None
    """
    graph = {node: [list(edge) for edge in edges] for node, edges in graph.items()}
    file_path = create_file_path(name=name)
    with open(file_path, "w") as f:
        json.dump(graph, f, separators=(",", ":"))


def save_graph_to_json_list(graph: GraphList, name: str) -> None:
    """
    Save a graph (in list adjacency format) as a pretty-printed JSON array.

    Parameters
    ----------
    graph : GraphList
        Adjacency list: list of lists of (neighbor idx, weight int) tuples.
    name : str
        The base file name (without extension).

    Returns
    -------
    None
    """
    file_path = create_file_path(name=name)
    print(file_path)
    with open(file_path, "w") as f:
        f.write("[\n")
        for idx, neighbors in enumerate(graph):
            line = "  " + json.dumps(neighbors)
            if idx != len(graph) - 1:
                line += ","
            f.write(line + "\n")
        f.write("]")


def load_graph_from_json_dict(name: str) -> dict:
    """
    Load a graph (dictionary adjacency format) from a JSON file, returning all edges as lists (not tuples).

    Parameters
    ----------
    name : str
        The base file name (without extension).

    Returns
    -------
    dict
        The graph as a dict mapping node str to list of [neighbor str, weight int] lists.
    """
    file_path = create_file_path(name=name)
    with open(file_path, "r") as f:
        data = json.load(f)
    graph = {node: [list(edge) for edge in edges] for node, edges in data.items()}
    return graph


def timing_decorator(func):
    """
    Decorator to measure the execution time of a function.

    The decorator returns a tuple (result, elapsed_time).

    Parameters
    ----------
    func : callable
        The function to be timed.

    Returns
    -------
    callable
        A wrapped version of `func` that returns (result, elapsed_time).
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        # print(f"{func.__name__} executed in {elapsed:.6f} seconds")
        return result, elapsed

    return wrapper


def create_frequency() -> List[int]:
    """
    Generate a list of sizes for use in batch graph generation.

    Returns
    -------
    List[int]
        List of sizes (int), excluding 0.
    """
    frequency = []
    frequency += list(range(0, 101, 10))
    # frequency += list(range(200, 1001, 100))
    # frequency += list(range(2000, 10001, 1000))
    # frequency += list(range(20000, 100001, 10000))
    frequency.pop(0)
    return frequency
