import math
import random

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import AmplificationProblem, Grover


def pad_to_power_of_two_with_indices(indices, distances):

    finite = [
        (idx, dist) for idx, dist in zip(indices, distances) if dist != float("inf")
    ]
    finite_indices, finite_distances = zip(*finite) if finite else ([], [])

    count = len(finite_indices)
    if count == 0:
        print("No finite entries.")
        return [], []

    next_pow2 = 2 ** math.ceil(math.log2(count))

    padded_indices = list(finite_indices) + [float("inf")] * (next_pow2 - count)
    padded_distances = list(finite_distances) + [float("inf")] * (next_pow2 - count)
    return padded_indices, padded_distances


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
        for qubit, bit in enumerate(reversed(bitstring)):
            if bit == "0":
                circ.x(qubit)

    return circ


def grover_search(size, marked_states, iterations):
    if not marked_states:
        return None

    n = math.ceil(math.log2(size))

    oracle = grover_oracle(n=n, targets=marked_states)
    target_bitstrings = {format(i, f"0{n}b") for i in marked_states}

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

    if result.assignment is None:
        return None

    candidate = int(result.assignment, 2)

    if candidate in marked_states:
        return candidate

    return None


def bbht_search(size, marked_states):
    """
    Boyer-Brassard-Høyer-Tapp exponential search.
    Returns (candidate, cost).
    """
    if not marked_states:
        return None, 0

    lam = 6 / 5
    m = 1
    cost = 0

    while True:
        upper = max(1, int(m))
        j = random.randrange(upper)

        candidate = grover_search(size=size, marked_states=marked_states, iterations=j)

        cost += j

        if candidate is not None:
            return candidate, cost

        if m >= math.sqrt(size):
            m = math.sqrt(size)
        else:
            m *= lam


def find_min(active_distances):
    size = len(active_distances)
    threshold = random.randrange(size)
    time_limit = 22.5 * math.sqrt(size) + 1.4 * math.log2(size)
    total_time = 0.0

    while True:
        marked_states = [
            i for i in range(size) if active_distances[i] < active_distances[threshold]
        ]

        if not marked_states:
            break

        y_prime, search_cost = bbht_search(size=size, marked_states=marked_states)
        oracle_cost = math.log2(size) * search_cost
        total_time = total_time + search_cost + oracle_cost
        if total_time > time_limit:
            break

        total_time += search_cost

        if y_prime is None:
            break

        if active_distances[y_prime] < active_distances[threshold]:
            threshold = y_prime

    return (
        threshold,
        active_distances[threshold],
        total_time,
        time_limit,
    )


if __name__ == "__main__":

    random.seed()

    N = 16

    nums = list(range(N))
    random.shuffle(nums)

    nums = [23, 10, 14]
    N = len(nums)
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
