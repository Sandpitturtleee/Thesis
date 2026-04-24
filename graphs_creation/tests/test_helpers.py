import json

import graphs_creation.src.helpers
from config import GENERATED_GRAPHS_DIRECTORY, MAX_GRAPH_SIZE
from graphs_creation.src.helpers import (
    create_file_path,
    create_frequency,
    save_graph_to_json,
)


def test_create_file_path(tmp_path, monkeypatch):
    dummy_file = tmp_path / "dummy.py"
    dummy_file.write_text("")
    monkeypatch.setattr(graphs_creation.src.helpers, "__file__", str(dummy_file))

    path = graphs_creation.src.helpers.create_file_path(
        directory=GENERATED_GRAPHS_DIRECTORY, name="10_random"
    )
    assert path.name == "10_random.json"
    assert path.parent.name == GENERATED_GRAPHS_DIRECTORY


def test_save_graph_to_json(sample_graph_list):
    save_graph_to_json(sample_graph_list, "test")
    file_path = create_file_path(directory=GENERATED_GRAPHS_DIRECTORY, name="test")
    assert file_path.exists()
    with open(file_path) as f:
        data = json.load(f)
    assert data == sample_graph_list


def test_create_frequency():
    freq = create_frequency()
    assert isinstance(freq, list)
    assert 0 not in freq
    assert freq[0] == 10
    assert freq[-1] == MAX_GRAPH_SIZE
    assert all(isinstance(x, int) for x in freq)
