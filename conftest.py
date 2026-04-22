import pytest

from graphs_creation.tests.data import FILE_NAMES, GRAPH_DICT, GRAPH_LIST


@pytest.fixture
def sample_graph_dict():
    return GRAPH_DICT


@pytest.fixture
def sample_graph_list():
    return GRAPH_LIST


@pytest.fixture
def file_names():
    return FILE_NAMES
