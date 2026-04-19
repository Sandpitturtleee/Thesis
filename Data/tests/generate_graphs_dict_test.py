import pytest

from Data.src.generate_graphs_dict import (
    generate_graph_dict,
    generate_graph_worst_case_dict,
    generate_graphs_dict,
)


def is_one_edge_per_pair(graph):
    """
    Check that for every unordered pair of nodes, at most one edge exists (regardless of weight).
    Also checks undirected property (reciprocity).
    """
    edges_seen = set()
    for node, edges in graph.items():
        for neighbor, weight in edges:
            pair = frozenset([node, neighbor])
            assert weight == int(
                weight
            ), f"Edge {node}-{neighbor} has non-integer weight!"
            if node != neighbor:
                if (pair, weight) not in edges_seen:
                    assert (node, weight) in [
                        (n, w) for n, w in graph[neighbor]
                    ], f"Graph is not undirected for edge {node}-{neighbor}!"
                edges_seen.add((pair, weight))
    pairs = [pair for pair, weight in edges_seen]
    assert len(pairs) == len(
        set(pairs)
    ), "Duplicate edge with different weights detected between same nodes!"


@pytest.mark.parametrize(
    "generator",
    [
        generate_graph_dict,
        generate_graph_worst_case_dict,
    ],
)
@pytest.mark.parametrize("num_vertices", [2, 3, 10])
def test_graph_generation_single_connection_per_pair(generator, num_vertices):
    graph = generator(num_vertices)
    is_one_edge_per_pair(graph)


def test_generate_graphs_dict(monkeypatch):
    monkeypatch.setattr(
        "Data.src.generate_graphs_dict.create_frequency", lambda: [2, 3]
    )
    called = []

    def fake_save_graph_to_json_dict(graph, name):
        called.append((graph, name))

    monkeypatch.setattr(
        "Data.src.generate_graphs_dict.save_graph_to_json_dict",
        fake_save_graph_to_json_dict,
    )
    generate_graphs_dict()
    assert len(called) == 2 * len([2, 3])
