from data_analysis.src.plots_other import draw_graph_small
from thesis_config import (GRAPH_DENSE, GRAPH_HALF_EDGES, GRAPH_SPARSE,
                           GRAPH_SPECIAL_CASE)

if __name__ == "__main__":
    print()
    draw_graph_small(graph=GRAPH_SPARSE)
    draw_graph_small(graph=GRAPH_HALF_EDGES)
    draw_graph_small(graph=GRAPH_DENSE)
    draw_graph_small(graph=GRAPH_SPECIAL_CASE)
