"""
Dijkstra Results Loader
-----------------------

This module provides utilities for loading, parsing, and organizing Dijkstra algorithm results
from JSON files, as well as utilities for handling associated statistics and plotting information.

Functions:
----------
- read_results_from_json: Loads all JSON result files for Dijkstra runs from a given directory.
- extract_methods_and_labels: Categorizes result files into heap/naive based on filename and creates labels.
- quantum_stat_from_dict: Extracts values of a particular statistic (e.g., mean) from a dictionary keyed by vertex count.
- order_filenames: Orders filenames in a preferred sequence for consistent analysis/presentation.
- per_count_row_statistics: Computes row-wise summary statistics on a 2D list of counts.
- merge_dicts_standard: Merges a list of standard result dictionaries (concatenates runs).
- merge_stats_dicts: Merges arbitrary stats dictionaries (deep copy).
- get_type_from_filename: Infers graph type from the result filename using the color map.
- add_custom_legend: Adds a legend to a Matplotlib axis using a controlled order of handles.

Types:
------
- ResultDict: Dict[str, dict]  # Mapping from filename to parsed result content
- MethodLabels: Dict[str, str] # Mapping from method/file name to human-readable label

"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from config import COLOR_MAP, DATA_DIRECTORY, LEGEND_ORDER, GRAPH_LABELS_MAP

ResultDict = Dict[str, dict]
MethodLabels = Dict[str, str]


def read_results_from_json(directory: str) -> ResultDict:
    """
    Reads all JSON result files for Dijkstra algorithm runs from the results directory.

    For each `.json` file found in the `../data/directory/` directory (relative to project root),
    the function loads its contents and adds it to a dictionary using the filename as key.

    Parameters
    ----------
    directory : str
        Name of the subdirectory under DATA_DIRECTORY where JSON files are stored.

    Returns
    -------
    ResultDict
        Dictionary where keys are JSON filenames and values are their contents (parsed from JSON).
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


def extract_methods_and_labels(
    data: ResultDict,
) -> Tuple[List[str], List[str], MethodLabels]:
    """
    Categorize methods/files into heap- or naive-based algorithms, and generate readable labels.

    Parameters
    ----------
    data : ResultDict
        Loaded JSON data keyed by filename.

    Returns
    -------
    heap_methods : List[str]
        Filenames/keys corresponding to heap-based Dijkstra runs.
    naive_methods : List[str]
        Filenames/keys corresponding to naive-based Dijkstra runs.
    method_labels : MethodLabels
        Mapping from each method/file key to a human-readable label.
    """
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


def quantum_stat_from_dict(
    cost_dict: Dict[str, Dict[str, float]],
    key: str = "mean",
) -> Tuple[List[int], List[float]]:
    """
    Extract lists of vertex counts and corresponding statistics for plotting.

    Parameters
    ----------
    cost_dict : Dict[str, Dict[str, float]]
        Mapping from vertex count (as string) to a dictionary of statistics.
    key : str
        Statistic to extract (e.g., "mean", "std", "min", etc.).

    Returns
    -------
    vertices : List[int]
        Sorted list of vertex counts (converted to int).
    y : List[float]
        List of values corresponding to the specified statistic.
    """
    vertices = sorted(map(int, cost_dict.keys()))
    y = [cost_dict[str(v)][key] for v in vertices]
    return vertices, y


def order_filenames(all_stats: ResultDict) -> List[str]:
    """
    Orders the input filenames in a canonical order for consistent reporting.

    Parameters
    ----------
    all_stats : ResultDict:
        Dict of filenames or keys to be ordered.

    Returns
    -------
    ordered_keys : List[str]
        Ordered list of keys based on preferred sequence (sparse, half_edges, dense, worstcase).
    """
    type_to_key = {
        "sparse": "sparse",
        "half_edges": "half_edges",
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
    for k in all_stats:
        if k not in ordered_keys:
            ordered_keys.append(k)
    return ordered_keys


def per_count_row_statistics(
    counts: List[List[int]],
    vertices: Optional[List[int]] = None,
) -> pd.DataFrame:
    """
    Compute per-row statistics for a 2D list of counts.
    Useful for summarizing statistics for each problem size.

    Parameters
    ----------
    counts : List[List[int]]
        Two-dimensional list: counts[vertex][run_index]
    vertices : Optional[List[int]]
        Vertex counts for indexing (if provided).

    Returns
    -------
    pd.DataFrame
        pd.DataFrame with statistics: mean, std, median, min, max for each row/vertex.
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


def merge_dicts_standard(dicts: List[ResultDict]) -> ResultDict:
    """
    Merge a list of result dicts by concatenating run counts for each problem size.

    Parameters
    ----------
    dicts : List[ResultDict]
        List of result dictionaries to merge.

    Returns
    -------
    merged : ResultDict
        Merged dictionary of all runs (deep copy, counts concatenated).
    """
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


import copy


def merge_stats_dicts(dicts: List[ResultDict]) -> ResultDict:
    """
    Merge a list of stats dictionaries by deep copying newer entries.

    Parameters
    ----------
    dicts : List[ResultDict]
        List of stats dictionaries.

    Returns
    -------
    merged : ResultDict
        Merged dictionary, overriding duplicates.
    """
    merged = {}
    for d in dicts:
        for k, v in d.items():
            merged[k] = copy.deepcopy(v)
    return merged


def get_type_from_filename(filename: str) -> Optional[str]:
    """
    Infer the graph/problem type encoded in the given filename.

    Parameters
    ----------
    filename : str

    Returns
    -------
    Optional[str]
        Corresponding type key found in COLOR_MAP, or None if missing.
    """
    for key in COLOR_MAP:
        if key in filename:
            return key
    return None


def add_custom_legend(
    ax,
    handles_dict: Dict[str, Any],
    extra_curves: Optional[List[Any]] = None,
    extra_labels: Optional[List[str]] = None,
) -> None:
    """
    Add a custom legend to a matplotlib axis, in ordered fashion.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        An axes object to add the legend to.
    handles_dict : Dict[str, Any]
        Mapping from label key to Line2D/patch handle.
    extra_curves : Optional[List[Any]]
        Additional handles to add to the legend.
    extra_labels : Optional[List[str]]
        Additional label strings corresponding to extra_curves.

    Returns
    -------
    None
    """
    handles = [
        handles_dict[key]
        for key in LEGEND_ORDER
        if key in handles_dict
    ]

    labels = [
        GRAPH_LABELS_MAP.get(key, key)
        for key in LEGEND_ORDER
        if key in handles_dict
    ]

    if extra_curves and extra_labels:
        handles.extend(extra_curves)
        labels.extend(extra_labels)

    ax.legend(handles, labels)
