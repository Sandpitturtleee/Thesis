"""
Graph Handling Utilities
------------------------

This module provides utility functions for saving graphs (in dictionary or adjacency list format) as JSON files,
managing file paths, and constructing useful sizes for batch graph generation.

Functions:
----------
- create_file_path: Create and return a JSON file path for persisting graph data.
- create_frequency: Generate a list of sizes for graph generation batches.
- save_graph_to_json_dict: Save a dictionary-format graph as a compact JSON file.
- save_graph_to_json_list: Save a list-format (adjacency list) graph as a pretty-printed JSON array.

Types:
------
- GraphDict: type alias for Dict[str, List[Tuple[str, int]]]
- GraphList: type alias for List[List[Tuple[int, int]]]
"""

import json
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
    file_path = create_file_path(directory=JSON_DICT_DIRECTORY, name=name)
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
    file_path = create_file_path(directory=JSON_LIST_DIRECTORY, name=name)
    with open(file_path, "w") as f:
        f.write("[\n")
        for idx, neighbors in enumerate(graph):
            line = "  " + json.dumps(neighbors)
            if idx != len(graph) - 1:
                line += ","
            f.write(line + "\n")
        f.write("]")
