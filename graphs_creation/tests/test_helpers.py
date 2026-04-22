import json
import time
from pathlib import Path

import pytest

import graphs_creation.src.helpers
from config import JSON_DICT_DIRECTORY, JSON_LIST_DIRECTORY, MAX_FREQUENCY
from graphs_creation.src.helpers import (
    create_file_path,
    create_frequency,
    save_graph_to_json_dict,
    save_graph_to_json_list,
)


def remove_test_json_files(file_names):
    json_dir = (Path(__file__).parent.parent.parent / JSON_DICT_DIRECTORY).resolve()
    for name in file_names:
        fpath = json_dir / name
        if fpath.exists():
            fpath.unlink()
    json_dir = (Path(__file__).parent.parent.parent / JSON_LIST_DIRECTORY).resolve()
    for name in file_names:
        fpath = json_dir / name
        if fpath.exists():
            fpath.unlink()


@pytest.fixture(autouse=True)
def cleanup_json_folder(file_names):
    remove_test_json_files(file_names)
    yield
    remove_test_json_files(file_names)


def test_create_file_path(tmp_path, monkeypatch):
    dummy_file = tmp_path / "dummy.py"
    dummy_file.write_text("")
    monkeypatch.setattr(graphs_creation.src.helpers, "__file__", str(dummy_file))

    path = graphs_creation.src.helpers.create_file_path(
        directory=JSON_DICT_DIRECTORY, name="10_random"
    )
    assert path.name == "10_random.json"
    assert path.parent.name == JSON_DICT_DIRECTORY


def test_save_graph_to_json_dict(sample_graph_dict):
    save_graph_to_json_dict(sample_graph_dict, "testdict")
    file_path = create_file_path(directory=JSON_DICT_DIRECTORY, name="testdict")
    assert file_path.exists()
    with open(file_path) as f:
        data = json.load(f)
    assert data == sample_graph_dict


def test_save_graph_to_json_list(sample_graph_list):
    save_graph_to_json_list(sample_graph_list, "testlist")
    file_path = create_file_path(directory=JSON_LIST_DIRECTORY, name="testlist")
    assert file_path.exists()
    with open(file_path) as f:
        data = json.load(f)
    assert data == sample_graph_list


def test_create_frequency():
    freq = create_frequency()
    assert isinstance(freq, list)
    assert 0 not in freq
    assert freq[0] == 10
    assert freq[-1] == MAX_FREQUENCY
    assert all(isinstance(x, int) for x in freq)
