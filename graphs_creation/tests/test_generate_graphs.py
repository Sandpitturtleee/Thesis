import pytest

from graphs_creation.src.generate_graphs import (
    generate_graph_random,
    generate_graph_worstcase,
    generate_graphs,
)


def is_one_edge_per_pair_list(graph):
    """
    Checks that for every unordered pair of nodes, at most one edge exists (regardless of weight).
    Also checks that undirected property (reciprocity) holds.
    """
    edges_seen = set()
    for node, edges in enumerate(graph):
        for neighbor, weight in edges:
            assert weight == int(
                weight
            ), f"Edge {node}-{neighbor} has non-integer weight!"
            pair = frozenset([node, neighbor])
            if node != neighbor:
                if (pair, weight) not in edges_seen:
                    assert (node, weight) in graph[
                        neighbor
                    ], f"Graph is not undirected for edge {node}-{neighbor}!"
                edges_seen.add((pair, weight))
    pairs = [pair for pair, weight in edges_seen]
    assert len(pairs) == len(
        set(pairs)
    ), "Duplicate edge with different weights detected between same nodes!"


@pytest.mark.parametrize(
    "generator",
    [
        generate_graph_random,
        generate_graph_worstcase,
    ],
)
@pytest.mark.parametrize("num_vertices", [2, 3, 10])
def test_graph_generation_single_connection_per_pair_list(generator, num_vertices):
    graph = generator(num_vertices)
    is_one_edge_per_pair_list(graph)


def test_generate_graphs_list(monkeypatch):
    monkeypatch.setattr(
        "graphs_creation.src.generate_graphs.create_frequency", lambda: [2, 3]
    )
    called = []

    def fake_save_graph_to_json(graph, name):
        called.append((graph, name))

    monkeypatch.setattr(
        "graphs_creation.src.generate_graphs.save_graph_to_json",
        fake_save_graph_to_json,
    )
    generate_graphs()
    assert len(called) == 2 * len([2, 3])
