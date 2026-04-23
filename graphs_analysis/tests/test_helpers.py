import time

from config import MAX_FREQUENCY
from graphs_analysis.src.helpers import (
    create_frequency,
    load_graph_from_json_dict,
    load_graph_from_json_list,
    timing_decorator,
)
from graphs_creation.src.helpers import save_graph_to_json_dict, save_graph_to_json_list


def test_load_graph_from_json_dict(sample_graph_dict):
    save_graph_to_json_dict(sample_graph_dict, "testdict")
    loaded_graph = load_graph_from_json_dict("testdict")
    assert loaded_graph == sample_graph_dict


def test_load_graph_from_json_list(sample_graph_list):
    save_graph_to_json_list(sample_graph_list, "testlist")
    loaded_graph = load_graph_from_json_list("testlist")
    assert loaded_graph == sample_graph_list


def test_timing_decorator():
    @timing_decorator
    def waste_time(t):
        time.sleep(t)
        return t * 2

    result, elapsed = waste_time(0.1)
    assert result == 0.2
    assert elapsed >= 0.1


def test_create_frequency():
    freq = create_frequency()
    assert isinstance(freq, list)
    assert 0 not in freq
    assert freq[0] == 10
    assert freq[-1] == MAX_FREQUENCY
    assert all(isinstance(x, int) for x in freq)
