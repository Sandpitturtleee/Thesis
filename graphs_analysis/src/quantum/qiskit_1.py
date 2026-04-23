import random

import numpy as np
from qiskit import *
from qiskit.circuit.library import GroverOperator


# nums = unsorted array of numbers
def find_min(nums, iters):
    N = len(nums)
    t = nums[random.randint(0, N - 1)]  # Choosing a random threshhold value
    targets = [
        i for i in range(N) if nums[i] <= t
    ]  # Marking elements of nums that are <= threshhold
    for i in range(iters):
        new_t = nums[
            grover_search(targets, N)
        ]  # Grover search to find element smaller than current threshhold
        if new_t < t:
            t = new_t
            targets = [target for target in targets if nums[target] <= t]
    return t


def grover_search(targets, N):
    d = int(np.ceil(np.log2(N)))
    oracle = np.identity(2**d)
    for target in targets:
        oracle[target, target] = -1  # Building oracle
    oc = QuantumCircuit(d)
    oc.unitary(oracle, range(d))
    grover_op = GroverOperator(oc, insert_barriers=True)
    qc = QuantumCircuit(d, d)
    qc.h(range(d))  # Initializing equal superposition
    r = int(np.sqrt(N))
    for i in range(r):
        qc = qc.compose(grover_op)
    qc.measure(range(d), range(d))
    backend = Aer.get_backend("qasm_simulator")
    qc.decompose().draw()
    job = execute(qc, backend)
    result = int(list(job.result().get_counts().keys())[0], 2)
    return result


m = list(range(16))
print(m)
find_min(m, 64)
