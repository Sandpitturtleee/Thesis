# File: data_analysis/tests/test_helpers.py

import io
import json
import pytest

import json
import os
from pathlib import Path

from config import DATA_DIRECTORY, DIJKSTRA_RESULTS_DIRECTORY
# Import the real helpers module under test
from data_analysis.src import helpers


@pytest.fixture
def patch_path(monkeypatch):
    class FakePath(helpers.Path):
        _flavour = helpers.Path('.')._flavour

        def mkdir(self, parents=True, exist_ok=True):
            return None

    monkeypatch.setattr(helpers, "Path", FakePath)
    monkeypatch.setattr(helpers, "DATA_DIRECTORY", 'data')
    monkeypatch.setattr(helpers, "DIJKSTRA_RESULTS_DIRECTORY", 'dijkstra_results')
    return FakePath


def test_read_results_from_json(monkeypatch, patch_path):
    fake_files = ['result1.json', 'result2.json', 'ignore.txt']
    project_root = Path(__file__).parent.parent.parent
    path = project_root / DATA_DIRECTORY / DIJKSTRA_RESULTS_DIRECTORY
    dir_path = patch_path(path)

    monkeypatch.setattr("os.listdir", lambda path: fake_files)

    file_data_map = {
        str(dir_path / 'result1.json'): '{"a":1}',
        str(dir_path / 'result2.json'): '{"b":2}'
    }

    def fake_open(file, mode='r', *args, **kwargs):
        key = str(file)   # Always compare as string
        if key in file_data_map and 'r' in mode:
            return io.StringIO(file_data_map[key])
        raise FileNotFoundError(file)

    monkeypatch.setattr("builtins.open", fake_open)

    results = helpers.read_results_from_json()
    assert "result1.json" in results
    assert "result2.json" in results
    assert "ignore.txt" not in results
    assert results["result1.json"] == {"a": 1}
    assert results["result2.json"] == {"b": 2}
