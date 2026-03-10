from dijkstra import dijkstra_binheap, dijkstra_fibheap
from Data.generate_graphs import load_graph_from_json

json_folder = "../data/json"
# Press the green button in the gutter to run the script.
if __name__ == '__main__':




    # Przykład użycia:
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }
    print(graph)


    # loaded_graph = load_graph_from_json("1000.json")

    distances, previous = dijkstra_binheap(loaded_graph, 'V0')
    print("Odległości:", distances)
    print("Poprzednicy:", previous)

    print()

    distances, previous = dijkstra_fibheap(loaded_graph, 'B')
    print("Odległości:", distances)
    print("Poprzednicy:", previous)
