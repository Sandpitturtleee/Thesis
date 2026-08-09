# Built-in modules
import math

from networkx import display
# Imports from Qiskit
from qiskit import MissingOptionalLibraryError, QuantumCircuit
from qiskit.circuit.library import (MCMTGate, PhaseOracleGate, ZGate,
                                    grover_operator)
from qiskit.primitives import StatevectorSampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_distribution
from qiskit_algorithms import AmplificationProblem, Grover

from graphs_analysis.src.dijkstra_validation import (dijkstra_lib,
                                                     is_dijkstra_valid)
from graphs_analysis.src.quantum.dijkstra_quantum import dijkstra_quantum
from graphs_analysis.src.standard.dijkstra_heap import dijkstra_heap

if __name__ == "__main__":
    # -------------------------Step 1-------------------------
    loaded_graph = [
        [
            [1, 30],
            [2, 34],
            [3, 28],
            [4, 6],
            [5, 61],
            [6, 21],
            [7, 21],
            [8, 19],
            [9, 39],
        ],
        [[0, 30], [2, 7], [3, 6], [4, 12], [5, 28], [6, 89], [7, 42], [8, 16], [9, 13]],
        [[0, 34], [1, 7], [3, 36], [4, 22], [5, 8], [6, 79], [7, 84], [8, 70], [9, 22]],
        [
            [0, 28],
            [1, 6],
            [2, 36],
            [4, 50],
            [5, 51],
            [6, 49],
            [7, 35],
            [8, 58],
            [9, 11],
        ],
        [
            [0, 6],
            [1, 12],
            [2, 22],
            [3, 50],
            [5, 30],
            [6, 83],
            [7, 96],
            [8, 72],
            [9, 27],
        ],
        [[0, 61], [1, 28], [2, 8], [3, 51], [4, 30], [6, 8], [7, 9], [8, 47], [9, 43]],
        [[0, 21], [1, 89], [2, 79], [3, 49], [4, 83], [5, 8], [7, 6], [8, 35], [9, 86]],
        [[0, 21], [1, 42], [2, 84], [3, 35], [4, 96], [5, 9], [6, 6], [8, 59], [9, 82]],
        [
            [0, 19],
            [1, 16],
            [2, 70],
            [3, 58],
            [4, 72],
            [5, 47],
            [6, 35],
            [7, 59],
            [9, 80],
        ],
        [
            [0, 39],
            [1, 13],
            [2, 22],
            [3, 11],
            [4, 27],
            [5, 43],
            [6, 86],
            [7, 82],
            [8, 80],
        ],
    ]
    start_node = 0
    # invalid_count = 0
    # lengths_naive, previous_naive, elapsed, mismatch_count, search_count = (
    #     dijkstra_quantum(graph=loaded_graph, start_node=start_node, time_limit=1)
    # )
    # T = [
    #     30,
    #     34,
    #     28,
    #     6,
    #     61,
    #     21,
    #     21,
    #     19,
    #     39,
    #     float("inf"),
    #     float("inf"),
    #     float("inf"),
    #     float("inf"),
    #     float("inf"),
    #     float("inf"),
    #     float("inf"),
    # ]
    # y = 2
    # marked_states = [j for j in range(len(T)) if T[j] < T[y]]
    # print(marked_states)

    lengths_heap, previous_heap, elapsed = dijkstra_heap(
        graph=loaded_graph, start_node=start_node
    )
