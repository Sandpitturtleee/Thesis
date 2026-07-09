import math
import random

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import AmplificationProblem, Grover


def grover_oracle(n, targets):
    """Construct a phase oracle that marks the target basis states."""

    circ = QuantumCircuit(n)

    for target in targets:
        bitstring = format(target, f"0{n}b")

        # Flip qubits corresponding to 0 bits
        for qubit, bit in enumerate(bitstring):
            if bit == "0":
                circ.x(qubit)

        # Multi-controlled Z
        circ.h(n - 1)
        if n == 1:
            circ.z(0)
        else:
            circ.mcx(list(range(n - 1)), n - 1)
        circ.h(n - 1)

        # Undo the X gates
        for qubit, bit in enumerate(bitstring):
            if bit == "0":
                circ.x(qubit)

    return circ


def grover_search(size, marked_states, iterations):
    """Run Grover search using a fixed number of iterations."""

    if not marked_states:
        return None

    n = math.ceil(math.log2(size))

    oracle = grover_oracle(n, marked_states)

    target_bitstrings = {
        format(i, f"0{n}b")
        for i in marked_states
    }

    problem = AmplificationProblem(
        oracle=oracle,
        is_good_state=lambda x: x in target_bitstrings,
    )

    sampler = StatevectorSampler()

    grover = Grover(
        sampler=sampler,
        iterations=iterations,
    )

    result = grover.amplify(problem)

    return int(result.assignment, 2)


def find_min(nums):
    """
    Dürr-Høyer minimum finding simulation.

    This follows the paper:
      1. Pick a random threshold index y.
      2. Repeat until the running-time budget is exhausted.
      3. Return y.
    """

    N = len(nums)

    # Threshold index
    y = random.randrange(N)

    # Paper's running-time budget
    time_limit = 22.5 * math.sqrt(N) + 1.4 * math.log2(N)

    total_time = 0.0

    while True:

        # Mark every j with T[j] < T[y]
        marked_states = [
            i for i in range(N)
            if nums[i] < nums[y]
        ]

        # Current threshold is already minimum
        if not marked_states:
            break

        n = math.ceil(math.log2(N))

        # Optimal Grover iterations (known M because this is a simulation)
        optimal_num_iterations = max(
            1,
            math.floor(
                math.pi
                / (
                    4
                    * math.asin(
                        math.sqrt(
                            len(marked_states)
                            / (2 ** n)
                        )
                    )
                )
            ),
        )

        # Stage 2a costs log2(N)
        search_cost = math.log2(N) + optimal_num_iterations

        # Interrupt if the running-time budget would be exceeded
        if total_time + search_cost > time_limit:
            break

        total_time += search_cost

        y_prime = grover_search(
            N,
            marked_states,
            optimal_num_iterations,
        )

        if y_prime is None or y_prime < 0 or y_prime >= N:
            break

        # print(nums)
        # print(y_prime)
        if nums[y_prime] < nums[y]:
            y = y_prime

    return y, nums[y], total_time, time_limit


if __name__ == "__main__":

    random.seed()

    N = 16

    nums = list(range(N))
    random.shuffle(nums)

    print("Array:")
    print(nums)

    idx, value, runtime, limit = find_min(nums)

    print("\nQuantum minimum finding")
    print("-----------------------")
    print(f"Minimum index : {idx}")
    print(f"Minimum value : {value}")
    print(f"Runtime used  : {runtime:.2f}")
    print(f"Runtime limit : {limit:.2f}")

    # Verification
    true_idx = min(range(N), key=lambda i: nums[i])
    print("\nVerification")
    print("------------")
    print(f"True index   : {true_idx}")
    print(f"True minimum : {nums[true_idx]}")
    print(f"Success      : {idx == true_idx}")