import random

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import AmplificationProblem, Grover


def grover_oracle(n, targets):
    circ = QuantumCircuit(n)
    for binary_idx in [format(t, f"0{n}b") for t in targets]:
        for qubit, bit in enumerate(binary_idx):
            if bit == "0":
                circ.x(qubit)
        circ.h(n - 1)
        if n == 1:
            circ.z(0)
        else:
            circ.mcx(list(range(n - 1)), n - 1)
        circ.h(n - 1)
        for qubit, bit in enumerate(binary_idx):
            if bit == "0":
                circ.x(qubit)
    return circ


def grover_search(nums, targets):
    n = int(np.ceil(np.log2(len(nums))))
    oracle_circuit = grover_oracle(n, targets)
    target_bitstrings = {format(t, f"0{n}b") for t in targets}
    is_good = lambda bits: bits in target_bitstrings
    problem = AmplificationProblem(oracle_circuit, is_good_state=is_good)
    sampler = StatevectorSampler()
    grover = Grover(sampler=sampler)
    result = grover.amplify(problem)
    idx = int(result.assignment, 2)
    return idx


def find_min(nums, iters):
    N = len(nums)
    t = nums[random.randint(0, N - 1)]
    targets = [i for i in range(N) if nums[i] <= t]
    for _ in range(iters):
        new_idx = grover_search(nums, targets)
        new_t = nums[new_idx]
        if new_t < t:
            t = new_t
            targets = [i for i in targets if nums[i] <= t]
    return t


if __name__ == "__main__":
    m = list(range(16))
    random.shuffle(m)
    print("Unsorted:", m)
    found_min = find_min(m, 3)
    print("quantum found min:", found_min)
