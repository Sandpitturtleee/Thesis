from pathlib import Path

import pytest

from config import DATA_DIRECTORY, GENERATED_GRAPHS_DIRECTORY


def remove_test_json_files(file_names):
    if isinstance(file_names, str):
        file_names = [file_names]
    json_dir = (
        Path(__file__).parent / DATA_DIRECTORY / GENERATED_GRAPHS_DIRECTORY
    ).resolve()
    for name in file_names:
        fpath = json_dir / name
        if fpath.exists() and fpath.is_file():
            fpath.unlink()


@pytest.fixture(autouse=True)
def cleanup_json_folder(file_names):
    remove_test_json_files(file_names)
    yield
    remove_test_json_files(file_names)


@pytest.fixture
def sample_graph_dict():
    return {
        "V0": [
            ["V7", 6],
            ["V8", 9],
            ["V1", 9],
            ["V2", 9],
            ["V3", 3],
            ["V4", 4],
            ["V9", 3],
            ["V2", 6],
            ["V4", 8],
            ["V5", 4],
            ["V6", 7],
            ["V9", 8],
        ],
        "V1": [
            ["V0", 9],
            ["V2", 8],
            ["V6", 1],
            ["V4", 9],
            ["V3", 9],
            ["V2", 10],
            ["V3", 6],
            ["V4", 5],
            ["V5", 3],
            ["V9", 1],
        ],
        "V2": [
            ["V0", 9],
            ["V1", 8],
            ["V0", 6],
            ["V3", 2],
            ["V1", 10],
            ["V4", 6],
            ["V5", 2],
            ["V8", 1],
        ],
        "V3": [
            ["V0", 3],
            ["V1", 9],
            ["V2", 2],
            ["V1", 6],
            ["V5", 3],
            ["V6", 8],
            ["V8", 4],
            ["V9", 7],
        ],
        "V4": [
            ["V0", 4],
            ["V1", 9],
            ["V7", 7],
            ["V6", 2],
            ["V8", 4],
            ["V0", 8],
            ["V1", 5],
            ["V5", 4],
            ["V2", 6],
            ["V5", 10],
            ["V8", 2],
        ],
        "V5": [
            ["V4", 4],
            ["V7", 5],
            ["V6", 3],
            ["V8", 4],
            ["V0", 4],
            ["V1", 3],
            ["V2", 2],
            ["V3", 3],
            ["V4", 10],
            ["V9", 5],
        ],
        "V6": [
            ["V1", 1],
            ["V4", 2],
            ["V5", 3],
            ["V0", 7],
            ["V3", 8],
            ["V9", 8],
            ["V7", 7],
            ["V8", 2],
        ],
        "V7": [["V0", 6], ["V4", 7], ["V5", 5], ["V6", 7], ["V8", 8], ["V9", 5]],
        "V8": [
            ["V0", 9],
            ["V4", 4],
            ["V5", 4],
            ["V7", 8],
            ["V6", 2],
            ["V2", 1],
            ["V3", 4],
            ["V4", 2],
            ["V9", 7],
            ["V9", 5],
        ],
        "V9": [
            ["V0", 3],
            ["V5", 5],
            ["V6", 8],
            ["V8", 7],
            ["V7", 5],
            ["V8", 5],
            ["V0", 8],
            ["V1", 1],
            ["V3", 7],
        ],
    }


@pytest.fixture
def sample_graph_list():
    return [
        [[1, 6], [4, 10], [2, 9], [6, 1]],
        [[0, 6], [2, 9], [3, 6], [4, 1], [5, 8], [6, 10], [7, 10], [8, 9], [9, 2]],
        [[1, 9], [0, 9], [4, 4], [5, 10], [6, 2], [9, 9], [7, 10]],
        [[1, 6], [5, 7], [6, 5], [4, 3], [7, 7], [8, 7], [9, 4]],
        [[0, 10], [1, 1], [2, 4], [3, 3], [5, 6], [6, 2], [7, 4], [8, 3], [9, 9]],
        [[1, 8], [2, 10], [3, 7], [4, 6], [8, 10], [9, 7], [6, 7], [7, 1]],
        [[1, 10], [2, 2], [3, 5], [4, 2], [0, 1], [5, 7], [7, 2], [8, 7], [9, 2]],
        [[1, 10], [4, 4], [6, 2], [2, 10], [3, 7], [5, 1], [9, 8]],
        [[1, 9], [4, 3], [5, 10], [6, 7], [3, 7]],
        [[1, 2], [2, 9], [4, 9], [5, 7], [7, 8], [3, 4], [6, 2]],
    ]


@pytest.fixture
def file_names():
    return ["test.json"]
