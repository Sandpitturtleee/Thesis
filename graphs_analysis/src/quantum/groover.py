import numpy as np
from qutip import *
from qutip.core.gates import hadamard_transform

# ----- Basic gates -----
H = hadamard_transform(1)
X = sigmax()
I = qeye(2)

if __name__ == "__main__":
    import numpy as np
    from qutip import *

    # ----- Basic gates -----
    H = hadamard_transform(1)
    X = sigmax()
    I = qeye(2)

    # ----- Helper functions -----
    def gate_on_qubit(gate, qubit, total):
        ops = []
        for i in range(total):
            ops.append(gate if i == qubit else I)
        return tensor(ops)

    # ----- Initial state |0000> -----
    state = tensor(basis(2, 0), basis(2, 0), basis(2, 0), basis(2, 0))

    # ----- X on ancilla -----
    state = gate_on_qubit(X, 3, 4) * state

    # ----- Hadamard on all qubits -----
    H_all = tensor(H, H, H, H)
    state = H_all * state

    # ----- Oracle construction -----
    oracle_matrix = np.eye(16)
    print(oracle_matrix)

    def mark_state(bitstring):
        idx = int(bitstring, 2)
        oracle_matrix[idx, idx] = -1

    # mark |111> and |001> (ancilla = 0 here)
    mark_state("1110")
    mark_state("0010")
    mark_state("1010")

    oracle = Qobj(oracle_matrix, dims=[[2, 2, 2, 2], [2, 2, 2, 2]])
    state = oracle * state

    # ----- Diffuser -----

    H3 = tensor(H, H, H, I)
    X3 = tensor(X, X, X, I)

    diff_matrix = np.eye(16)
    diff_matrix[int("1110", 2), int("1110", 2)] = -1

    mc_phase = Qobj(diff_matrix, dims=[[2, 2, 2, 2], [2, 2, 2, 2]])
    diffuser = H3 * X3 * mc_phase * X3 * H3

    state = diffuser * state

    # ----- Measurement probabilities -----
    probs = np.abs(state.full()) ** 2

    for i, p in enumerate(probs):
        print(format(i, "04b"), p[0])

# ilosc powtórzen pi/4 * pierwiastek z N
