# Built-in modules
import math

# Imports from Qiskit
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCMTGate, ZGate, grover_operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_distribution

from graphs_analysis.src.quantum.dijkstra_quantum import dijkstra_quantum

# Imports from Qiskit Runtime


def grover_oracle(marked_states):
    """Build a Grover oracle for multiple marked states

    Here we assume all input marked states have the same number of bits

    Parameters:
        marked_states (str or list): Marked states of oracle

    Returns:
        QuantumCircuit: Quantum circuit representing Grover oracle
    """
    if not isinstance(marked_states, list):
        marked_states = [marked_states]
    # Compute the number of qubits in circuit
    num_qubits = len(marked_states[0])

    qc = QuantumCircuit(num_qubits)
    # Mark each target state in the input list
    for target in marked_states:
        # Flip target bit-string to match Qiskit bit-ordering
        rev_target = target[::-1]
        # Find the indices of all the '0' elements in bit-string
        zero_inds = [
            ind for ind in range(num_qubits) if rev_target.startswith("0", ind)
        ]
        # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
        # where the target bit-string has a '0' entry
        if zero_inds:
            qc.x(zero_inds)
        qc.compose(MCMTGate(ZGate(), num_qubits - 1, 1), inplace=True)
        if zero_inds:
            qc.x(zero_inds)
    return qc


# Pop all items

if __name__ == "__main__":
    # -------------------------Step 1-------------------------
    graph = [
        [[3, 4], [5, 3]],
        [[3, 3], [8, 5]],
        [],
        [[5, 9], [0, 4], [4, 3], [1, 3], [9, 4]],
        [[3, 3], [5, 2]],
        [[3, 9], [7, 8], [0, 3], [4, 2]],
        [],
        [[5, 8], [9, 8]],
        [[1, 5]],
        [[7, 8], [3, 4]],
    ]
    dijkstra_quantum(graph, start_node=0)
