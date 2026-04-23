"""
Graph Handling Utilities
------------------------

This module provides utility functions for loading graphs (in dictionary or adjacency list format) from JSON files,
managing file paths, and constructing useful sizes for batch graph generation.

Functions:
----------
- create_file_path: Create and return a JSON file path for persisting graph data.
- create_frequency: Build standard batch sizes/frequencies up to MAX_FREQUENCY.
- load_graph_from_json_dict: Load GraphDict-style graphs from JSON file.
- load_graph_from_json_list: Load GraphList-style graphs from JSON file.
- timing_decorator Decorator for timing any function, returns (result, elapsed_time).

Types:
------
- GraphDict: type alias for Dict[str, List[Tuple[str, int]]]
- GraphList: type alias for List[List[Tuple[int, int]]]
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

from config import (
    DATA_DIRECTORY,
    JSON_DICT_DIRECTORY,
    JSON_LIST_DIRECTORY,
    MAX_FREQUENCY,
)

GraphDict = Dict[str, List[Tuple[str, int]]]
GraphList = List[List[Tuple[int, int]]]


def create_file_path(directory: str, name: str) -> Path:
    """
    Create the appropriate file path for saving or loading a graph's JSON file by name.

    The file will be placed in ../data/directory/ relative to this file.

    Parameters
    ----------
    directory : str
        The base name of a parent directory
    name : str
        The base name (without extension) for the JSON file.

    Returns
    -------
    Path
        The full path to the target JSON file.
    """
    project_root = Path(__file__).parent.parent.parent
    base_path = project_root / DATA_DIRECTORY / directory
    base_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.json"
    file_path = base_path / file_name
    return file_path


def create_frequency() -> List[int]:
    """
    Generate a list of sizes for use in batch graph generation, up to MAX_FREQUENCY.

    Returns
    -------
    List[int]
        List of sizes (int), excluding 0 and not exceeding MAX_FREQUENCY.
    """
    intervals = [
        (10, 100, 10),
        (200, 1000, 100),
        (2000, 10000, 1000),
        (20000, 100000, 10000),
        (200000, float("inf"), 100000),
    ]

    frequency = []
    for start, stop, step in intervals:
        actual_stop = min(stop, MAX_FREQUENCY)
        if start > MAX_FREQUENCY:
            continue
        vals = list(range(start, actual_stop + 1, step))
        frequency.extend(vals)
    return sorted(set(filter(lambda x: x <= MAX_FREQUENCY, frequency)))


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
    file_path = create_file_path(directory=JSON_DICT_DIRECTORY, name=name)
    with open(file_path, "r") as f:
        data = json.load(f)
    graph_dict = {node: [list(edge) for edge in edges] for node, edges in data.items()}
    return graph_dict


def load_graph_from_json_list(name: str) -> list:
    """
    Load a graph from a JSON file already in adjacency-list list format.

    Parameters
    ----------
    name : str
        The base file name (without extension).

    Returns
    -------
    list
        The graph as a list of adjacency lists, as in [[neighbor, weight], ...] per node.
    """
    file_path = create_file_path(directory=JSON_LIST_DIRECTORY, name=name)
    with open(file_path, "r") as f:
        graph_list = json.load(f)
    return graph_list


def save_results_to_json(directory, name, vertices, count):
    results = {"vertices": vertices, "count": count}
    file_path = create_file_path(directory=directory, name=name)
    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)
