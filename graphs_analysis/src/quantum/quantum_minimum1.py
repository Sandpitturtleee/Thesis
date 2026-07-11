import math
import random

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

        # Undo X gates
        for qubit, bit in enumerate(reversed(bitstring)):
            if bit == "0":
                circ.x(qubit)

    return circ


def grover_search(size, marked_states, iterations):
    """
    Run Grover search.
    Returns selected state and probabilities.
    """

    if not marked_states:
        return None, None

    n = math.ceil(math.log2(size))

    oracle = grover_oracle(n, marked_states)

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

    # Qiskit version compatible:
    # circuit_results[0] is already a dictionary
    probabilities = result.circuit_results[0]

    return int(result.assignment, 2), probabilities


def find_min(active_distances):
    """
    Dürr-Høyer minimum finding with full logging.

    active_distances must already be padded to a power of two.
    """

    N = len(active_distances)

    finite_indices = list(range(N))

    finite_values = list(active_distances)

    y_local = random.randrange(N)

    time_limit = 22.5 * math.sqrt(N) + 1.4 * math.log2(N)

    total_time = 0.0

    iteration = 1

    while True:

        print("\n" + "=" * 60)
        print(f"Iteration {iteration}")
        print("=" * 60)

        print("\nCurrent threshold:")
        print(f" Local index    : {y_local}")
        print(f" Value          : {finite_values[y_local]}")

        marked_states = [
            i for i in range(N) if finite_values[i] < finite_values[y_local]
        ]

        print("\nMarked states:")

        for i in marked_states:

            print(f" Local {i:2d} | " f"Value {finite_values[i]}")

        if not marked_states:

            print("\nNo better state exists.")
            break

        n = math.ceil(math.log2(N))

        optimal_iterations = max(
            1,
            math.floor(
                math.pi / (4 * math.asin(math.sqrt(len(marked_states) / (2**n))))
            ),
        )

        print(f"\nGrover iterations: " f"{optimal_iterations}")

        search_cost = math.log2(N) + optimal_iterations

        if total_time + search_cost > time_limit:

            print("\nRuntime limit exceeded.")
            break

        total_time += search_cost

        measured_local, probabilities = grover_search(
            N, marked_states, optimal_iterations
        )

        print("\nMeasurement probabilities")
        print("-" * 60)

        for state, probability in sorted(
            probabilities.items(), key=lambda x: x[1], reverse=True
        ):

            local_index = int(state, 2)

            print(
                f"{state} | "
                f"Local {local_index:2d} | "
                f"Value {finite_values[local_index]} | "
                f"P={probability:.6f}"
            )

        print("\nMeasured result:")
        print(f" Local index : {measured_local}")
        print(f" Value       : {finite_values[measured_local]}")

        if finite_values[measured_local] < finite_values[y_local]:

            print("\nThreshold updated.")

            y_local = measured_local

        else:

            print("\nThreshold unchanged.")

        print(f"\nRuntime:" f" {total_time:.2f}/{time_limit:.2f}")

        iteration += 1

    return (y_local, finite_values[y_local], total_time, time_limit)


if __name__ == "__main__":

    random.seed()

    # N = 16
    #
    #
    # nums = list(range(N))
    #
    # random.shuffle(nums)

    nums = [23, 10, 14]

    original_N = len(nums)

    # Pad to power of two
    power = 1
    while power < len(nums):
        power *= 2

    while len(nums) < power:
        nums.append(float("inf"))

    N = len(nums)

    print("Array:")
    print(nums)

    idx, value, runtime, limit = find_min(nums)

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print(f"Minimum index : {idx}")

    print(f"Minimum value : {value}")

    print(f"Runtime used  : {runtime:.2f}")

    print(f"Runtime limit : {limit:.2f}")

    true_idx = min(range(N), key=lambda i: nums[i])

    print("\nVerification")
    print("-" * 60)

    print(f"True index   : {true_idx}")

    print(f"True minimum : {nums[true_idx]}")

    print(f"Success      : {idx == true_idx}")
