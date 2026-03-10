from Data.helpers import load_graph_from_json, \
    illustrate_dijkstra_multi_color_legend
from dijkstra import dijkstra_binheap, dijkstra_fibheap

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Przykład użycia:
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }
    # print(graph)

    loaded_graph = load_graph_from_json("10")
    print(loaded_graph)

    (results, elapsed) = dijkstra_binheap(loaded_graph, 'V0')
    distances, previous = results
    print("Elapsed time:", elapsed)
    # elapsed, distances, previous = dijkstra_binheap(loaded_graph, 'V86')
    print("Odległości:", distances)
    print("Poprzednicy:", previous)

    # distances, previous = dijkstra_fibheap(loaded_graph, 'V86')
    # # print("Odległości:", distances)
    # # print("Poprzednicy:", previous)

    # graph = {
    #     'V0': [('V7', 3), ('V2', 4), ('V6', 1), ('V1', 7), ('V4', 1), ('V3', 1), ('V4', 10), ('V7', 6), ('V8', 10),
    #            ('V9', 9)],
    #     'V1': [('V0', 7), ('V5', 9), ('V6', 7), ('V2', 9), ('V3', 7), ('V4', 9), ('V7', 4), ('V9', 1)],
    #     'V2': [('V0', 4), ('V9', 9), ('V7', 2), ('V1', 9), ('V3', 3), ('V4', 1), ('V5', 7), ('V6', 9), ('V7', 7),
    #            ('V8', 10)],
    #     'V3': [('V9', 6), ('V0', 1), ('V2', 3), ('V1', 7), ('V4', 1)],
    #     'V4': [('V0', 1), ('V2', 1), ('V5', 5), ('V3', 1), ('V1', 9), ('V0', 10), ('V6', 6), ('V9', 9)],
    #     'V5': [('V1', 9), ('V4', 5), ('V7', 9), ('V2', 7), ('V6', 1)],
    #     'V6': [('V0', 1), ('V1', 7), ('V9', 5), ('V2', 9), ('V5', 1), ('V4', 6)],
    #     'V7': [('V0', 3), ('V2', 2), ('V5', 9), ('V0', 6), ('V2', 7), ('V8', 2), ('V1', 4)],
    #     'V8': [('V7', 2), ('V9', 7), ('V2', 10), ('V0', 10), ('V9', 8)],
    #     'V9': [('V2', 9), ('V3', 6), ('V6', 5), ('V8', 7), ('V0', 9), ('V4', 9), ('V8', 8), ('V1', 1)]
    # }
    #
    # distances = {'V0': 0, 'V1': 7, 'V2': 2, 'V3': 1, 'V4': 1, 'V5': 2, 'V6': 1, 'V7': 3, 'V8': 5, 'V9': 6}
    # previous = {'V0': None, 'V1': 'V0', 'V2': 'V4', 'V3': 'V0', 'V4': 'V0', 'V5': 'V6', 'V6': 'V0', 'V7': 'V0',
    #             'V8': 'V7', 'V9': 'V6'}

    illustrate_dijkstra_multi_color_legend(loaded_graph, previous, source='A')
