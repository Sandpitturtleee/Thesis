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

from config import DATA_DIRECTORY, DIJKSTRA_RESULTS_DIRECTORY, DIJKSTRA_STATS_DIRECTORY


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


def save_stats_by_file(stats_by_file):
    """
    Save stats for classic/standard files.
    Each is wrapped in a top-level 'cost' key.
    """
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / DATA_DIRECTORY / DIJKSTRA_STATS_DIRECTORY
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving stats to {output_dir}")

    for file_name, stats in stats_by_file.items():
        file_name_out = Path(file_name).stem + "_stats.json"
        out_path = output_dir / file_name_out

        # Convert DataFrame to dict and wrap in 'cost'
        wrapped = {"cost": stats.to_dict(orient="index")}

        with open(out_path, 'w') as f:
            json.dump(wrapped, f, indent=4)
    print(f"Stats saved to {output_dir}")


def save_stats_by_file_quantum(stats_by_file):
    """
    Save quantum stats for each file.
    stats_by_file = {file_name: {key: DataFrame, ...}, ...}
    """
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / DATA_DIRECTORY / DIJKSTRA_STATS_DIRECTORY
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving stats to {output_dir}")

    for file_name, field_stats in stats_by_file.items():
        file_name_out = Path(file_name).stem + "_stats.json"
        out_path = output_dir / file_name_out

        # Build a dictionary: {field_name: stats_df_as_dict}
        output_dict = {}
        for key, df in field_stats.items():
            output_dict[key] = df.to_dict(orient="index")

        # Save as JSON
        import json
        with open(out_path, 'w') as f:
            json.dump(output_dict, f, indent=4)
    print(f"Quantum stats saved to {output_dir}")


def read_results_by_vertex(file_name: str, vertex_number: int):
    """
    Reads a specific JSON result file for Dijkstra algorithm runs and returns data for a selected vertex number.

    Parameters
    ----------
    file_name : str
        Name of the .json result file to read (e.g., "some_results.json")
    vertex_number : int
        Number of vertices to look for in the file.

    Returns
    -------
    dict
        A dictionary with the matching 'vertices' value and corresponding 'count' list, or None if not found.
    """
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / DATA_DIRECTORY / DIJKSTRA_RESULTS_DIRECTORY / file_name

    # Read and load the JSON file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Find the index for the given vertex_number
    idx = data["vertices"].index(vertex_number)
    return {"vertices": data["vertices"][idx], "count": data["count"][idx]}


def read_results_by_vertices(file_name: str, vertices_number: list):
    """
    Reads counts for multiple vertex numbers from the given JSON results file.
    Returns a dict with vertex_number as key and counts as value.
    """
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / DATA_DIRECTORY / DIJKSTRA_RESULTS_DIRECTORY / file_name

    with open(file_path, "r") as file:
        data = json.load(file)

    results = {}
    for v in vertices_number:
        if v in data["vertices"]:
            idx = data["vertices"].index(v)
            results[v] = data["count"][idx]
        else:
            print(f"Vertex {v} not found in file.")
    return results


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
