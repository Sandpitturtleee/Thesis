import json
from pathlib import Path
from typing import Dict, List, Tuple

from config import DATA_DIRECTORY

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


def read_results_from_json(directory, name):
    file_path = create_file_path(directory=directory, name=name)
    with open(file_path, "r") as f:
        results = json.load(f)
    vertices = results["vertices"]
    count = results["count"]
    return vertices, count
