"""
Dijkstra Results Loader
-----------------------

This module provides a utility function to load all JSON result files for Dijkstra algorithm runs
from a specified results directory.

Functions:
----------
- read_results_from_json: Loads all JSON files from `../data/dijkstra_results/`
  and returns their contents in a dictionary.
"""

import json
import os
from pathlib import Path

import pandas as pd

from config import (
    DATA_DIRECTORY,
    DIJKSTRA_PROB_STATS_DIRECTORY,
    DIJKSTRA_STATS_DIRECTORY,
)


def read_results_from_json(directory) -> dict:
    """
    Reads all JSON result files for Dijkstra algorithm runs from the results directory.

    For each `.json` file found in the `../data/dijkstra_results/` directory (relative to this file),
    the function loads its contents and adds it to a dictionary using the filename as the key.

    Returns
    -------
    dict
        A dictionary where keys are JSON file names and values are the parsed JSON data for each file.
    """
    project_root = Path(__file__).parent.parent.parent
    path = project_root / DATA_DIRECTORY / directory
    path.mkdir(parents=True, exist_ok=True)
    data = {}
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r") as file:
                file_data = json.load(file)
                data[filename] = file_data
    return data


# def read_results_by_vertex(file_name: str, vertex_number: int):
#     """
#     Reads a specific JSON result file for Dijkstra algorithm runs and returns data for a selected vertex number.
#
#     Parameters
#     ----------
#     file_name : str
#         Name of the .json result file to read (e.g., "some_results.json")
#     vertex_number : int
#         Number of vertices to look for in the file.
#
#     Returns
#     -------
#     dict
#         A dictionary with the matching 'vertices' value and corresponding 'count' list, or None if not found.
#     """
#     project_root = Path(__file__).parent.parent.parent
#     file_path = project_root / DATA_DIRECTORY / DIJKSTRA_RESULTS_DIRECTORY / file_name
#
#     # Read and load the JSON file
#     with open(file_path, "r") as file:
#         data = json.load(file)
#
#     # Find the index for the given vertex_number
#     idx = data["vertices"].index(vertex_number)
#     return {"vertices": data["vertices"][idx], "count": data["count"][idx]}
#
#
# def read_results_by_vertices(file_name: str, vertices_number: list):
#     """
#     Reads counts for multiple vertex numbers from the given JSON results file.
#     Returns a dict with vertex_number as key and counts as value.
#     """
#     project_root = Path(__file__).parent.parent.parent
#     file_path = project_root / DATA_DIRECTORY / DIJKSTRA_RESULTS_DIRECTORY / file_name
#
#     with open(file_path, "r") as file:
#         data = json.load(file)
#
#     results = {}
#     for v in vertices_number:
#         if v in data["vertices"]:
#             idx = data["vertices"].index(v)
#             results[v] = data["count"][idx]
#         else:
#             print(f"Vertex {v} not found in file.")
#     return results


def extract_methods_and_labels(data):
    method_labels = {}
    heap_methods = []
    naive_methods = []
    for method in data.keys():
        # Create a readable label automatically
        label = (
            method.replace("standard_", "")
            .replace("_stats.json", "")
            .replace("_", " ")
            .title()
        )
        method_labels[method] = label
        if "heap" in method:
            heap_methods.append(method)
        elif "naive" in method:
            naive_methods.append(method)
    return heap_methods, naive_methods, method_labels


def quantum_stat_from_dict(cost_dict, key="mean"):
    vertices = sorted(map(int, cost_dict.keys()))
    y = [cost_dict[str(v)][key] for v in vertices]
    return vertices, y


def order_filenames(all_stats):
    # Map desired type to an identifying substring in the filename
    type_to_key = {
        "sparse": "sparse",
        "half_edges": "half_edges",  # adapt here for your actual filenames!
        "dense": "dense",
        "worstcase": "worstcase",
    }
    desired_order = ["sparse", "half_edges", "dense", "worstcase"]
    ordered_keys = []
    used_keys = set()
    for type_name in desired_order:
        tag = type_to_key[type_name]
        found = [k for k in all_stats if tag in k and k not in used_keys]
        if found:
            ordered_keys.append(found[0])
            used_keys.add(found[0])
    # Add leftovers
    for k in all_stats:
        if k not in ordered_keys:
            ordered_keys.append(k)
    return ordered_keys


def merge_dicts(dicts):
    merged = {}
    for d in dicts:
        for file, data in d.items():
            if file not in merged:
                # Deep copy to avoid reference issues
                merged[file] = {
                    "vertices": data["vertices"].copy(),
                    "count": [c.copy() for c in data["count"]],
                }
            else:
                for i, c in enumerate(data["count"]):
                    merged[file]["count"][i].extend(c)
    return merged


def per_count_row_statistics(counts, vertices=None):
    """
    Compute statistics per row for a 2D list of counts.
    If vertices are provided, use them as the DataFrame index.
    """
    df = pd.DataFrame(counts)
    if vertices is not None:
        df.index = vertices  # Set index for better labeling
    df_stats = pd.DataFrame(
        {
            "mean": df.mean(axis=1),
            "std": df.std(axis=1),
            "median": df.median(axis=1),
            "min": df.min(axis=1),
            "max": df.max(axis=1),
        },
        index=df.index,
    )
    return df_stats
