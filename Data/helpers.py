import json
from pathlib import Path


def create_file_path(name):
    base_path = Path(__file__).parent.parent / "data" / "json"
    base_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.json"
    file_path = base_path / file_name
    return file_path


def save_graph_to_json(graph, name):
    graph = {node: [list(edge) for edge in edges] for node, edges in graph.items()}
    file_path = create_file_path(name=name)
    with open(file_path, 'w') as f:
        json.dump(graph, f, indent=2)


def load_graph_from_json(name):
    file_path = create_file_path(name=name)
    with open(file_path, 'r') as f:
        data = json.load(f)
    graph = {node: [tuple(edge) for edge in edges] for node, edges in data.items()}
    return graph
