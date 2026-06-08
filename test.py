import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_small(graph):
    g = nx.DiGraph()
    g.add_nodes_from(range(len(graph)))
    for node, edges in enumerate(graph):
        for dest, weight in edges:
            g.add_edge(node, dest, weight=weight)
    pos = nx.spring_layout(g, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(g, pos, with_labels=True, node_color='lightblue', node_size=100, arrowsize=20)
    edge_labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_color='red')
    plt.title('Graph')
    plt.show()


# Pop all items

if __name__ == "__main__":
    graph = [
  [[1, 1], [2, 20], [3, 20], [4, 20], [5, 20], [6, 20], [7, 20], [8, 20], [9, 20]],
  [[0, 1], [2, 1], [3, 18], [4, 18], [5, 18], [6, 18], [7, 18], [8, 18], [9, 18]],
  [[0, 20], [1, 1], [3, 1], [4, 16], [5, 16], [6, 16], [7, 16], [8, 16], [9, 16]],
  [[0, 20], [1, 18], [2, 1], [4, 1], [5, 14], [6, 14], [7, 14], [8, 14], [9, 14]],
  [[0, 20], [1, 18], [2, 16], [3, 1], [5, 1], [6, 12], [7, 12], [8, 12], [9, 12]],
  [[0, 20], [1, 18], [2, 16], [3, 14], [4, 1], [6, 1], [7, 10], [8, 10], [9, 10]],
  [[0, 20], [1, 18], [2, 16], [3, 14], [4, 12], [5, 1], [7, 1], [8, 8], [9, 8]],
  [[0, 20], [1, 18], [2, 16], [3, 14], [4, 12], [5, 10], [6, 1], [8, 1], [9, 6]],
  [[0, 20], [1, 18], [2, 16], [3, 14], [4, 12], [5, 10], [6, 8], [7, 1], [9, 1]],
  [[0, 20], [1, 18], [2, 16], [3, 14], [4, 12], [5, 10], [6, 8], [7, 6], [8, 1]]
]
    draw_graph_small(graph)