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

from config import DATA_DIRECTORY, DIJKSTRA_RESULTS_DIRECTORY


def read_results_from_json() -> dict:
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
    path = project_root / DATA_DIRECTORY / DIJKSTRA_RESULTS_DIRECTORY
    path.mkdir(parents=True, exist_ok=True)
    data = {}
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r") as file:
                file_data = json.load(file)
                data[filename] = file_data
    return data
