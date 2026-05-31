from graphs_analysis.src.standard.dijkstra_naive import (
    dijkstra_naive,
    run_dijkstra_naive,
)


def test_dijkstra_naive_correctness():
    graph = [[(1, 2), (2, 10)], [(2, 3)], []]
    distances, previous, heap_ops = dijkstra_naive(graph, 0)
    assert distances == [0, 2, 5]
    assert previous == [None, 0, 1]
    assert heap_ops > 0


def test_run_dijkstra_naive_averages(monkeypatch):
    def fake_dijkstra_naive(graph, start_node):
        return [], [], 10 * len(graph)

    def fake_load_graph_from_json(name):
        n = int(name.split("_")[0])
        return [[(min(i + 1, n - 1), 2)] for i in range(n)]

    monkeypatch.setattr(
        "graphs_analysis.src.standard.dijkstra_naive.dijkstra_naive",
        fake_dijkstra_naive,
    )
    monkeypatch.setattr(
        "graphs_analysis.src.standard.dijkstra_naive.load_graph_from_json",
        fake_load_graph_from_json,
    )
    monkeypatch.setattr(
        "graphs_analysis.src.helpers.create_frequency", lambda *a, **k: [1, 2, 3, 4]
    )

    vertices, count = run_dijkstra_naive(times=10, graph_type="_R")

    assert vertices == [
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100,
        200,
        300,
        400,
        500,
        600,
        700,
        800,
        900,
        1000,
    ]


def test_run_all_dijkstra_naive(monkeypatch):
    result_side_effects = [
        ([10, 20], [5, 6]),  # RANDOM
        ([10, 20], [7, 8]),  # WORSTCASE
        ([10, 20], [9, 10]),  # SPARSE
    ]
    call_args = []

    def fake_run_dijkstra_naive(times, graph_type):
        return result_side_effects.pop(0)

    def fake_save_results_to_json(**kwargs):
        call_args.append(kwargs)

    monkeypatch.setattr(
        "graphs_analysis.src.standard.dijkstra_naive.run_dijkstra_naive",
        fake_run_dijkstra_naive,
    )
    monkeypatch.setattr(
        "graphs_analysis.src.standard.dijkstra_naive.save_results_to_json",
        fake_save_results_to_json,
    )
    monkeypatch.setattr("graphs_analysis.src.standard.dijkstra_naive.RANDOM", "_R")
    monkeypatch.setattr("graphs_analysis.src.standard.dijkstra_naive.WORSTCASE", "_WC")
    monkeypatch.setattr("graphs_analysis.src.standard.dijkstra_naive.SPARSE", "_S")
    monkeypatch.setattr(
        "graphs_analysis.src.standard.dijkstra_naive.RESULTS_DIRECTORY", "/tmp"
    )
    monkeypatch.setattr(
        "graphs_analysis.src.standard.dijkstra_naive.STANDARD_NAIVE_RANDOM_FILENAME",
        "random.json",
    )
    monkeypatch.setattr(
        "graphs_analysis.src.standard.dijkstra_naive.STANDARD_NAIVE_SPARSE_FILENAME",
        "sparse.json",
    )
    monkeypatch.setattr(
        "graphs_analysis.src.standard.dijkstra_naive.STANDARD_NAIVE_WORSTCASE_FILENAME",
        "worstcase.json",
    )

    from graphs_analysis.src.standard.dijkstra_naive import run_all_dijkstra_naive

    run_all_dijkstra_naive(times=1)

    # Assure the fake save is called with correct args
    assert call_args[0]["name"] == "random.json"
    assert call_args[1]["name"] == "worstcase.json"
    assert call_args[2]["name"] == "sparse.json"
    assert call_args[0]["directory"] == "/tmp"
    assert call_args[0]["vertices"] == [10, 20]
    assert call_args[1]["count"] == [7, 8]
