import json
from pathlib import Path
import time


def create_file_path(name):
    base_path = Path(__file__).parent.parent / "data" / "json"
    base_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.json"
    file_path = base_path / file_name
    return file_path


def save_graph_to_json_dict(graph, name):
    graph = {node: [list(edge) for edge in edges] for node, edges in graph.items()}
    file_path = create_file_path(name=name)
    with open(file_path, 'w') as f:
        json.dump(graph, f, separators=(',', ':'))  # compact/minified JSON

def save_graph_to_json_list(graph, name):
    file_path = create_file_path(name=name)
    with open(file_path, 'w') as f:
        f.write("[\n")
        for idx, neighbors in enumerate(graph):
            line = "  " + json.dumps(neighbors)
            if idx != len(graph) - 1:
                line += ","
            f.write(line + "\n")
        f.write("]")


def load_graph_from_json(name):
    file_path = create_file_path(name=name)
    with open(file_path, 'r') as f:
        data = json.load(f)
    graph = {node: [tuple(edge) for edge in edges] for node, edges in data.items()}
    return graph


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        # print(f"{func.__name__} executed in {elapsed:.6f} seconds")
        return result, elapsed

    return wrapper


def create_frequency():
    frequency = []
    frequency += list(range(0, 101, 10))
    # frequency += list(range(200, 1001, 100))
    # frequency += list(range(2000, 10001, 1000))
    # frequency += list(range(20000, 100001, 10000))
    frequency.pop(0)
    return frequency
