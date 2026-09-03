"""
Quantum Grover Search and Minimum Finding Utilities
--------------------------------------------------

This module implements Grover's quantum search and the Boyer-Brassard-Høyer-Tapp (BBHT)
minimum finding algorithm using Qiskit primitives.

Functions:
----------
- random_finite_index: Randomly chooses a non-infinite entry in an array.
- pad_to_power_of_two_with_indices: Pads index/value lists to a power of two for quantum circuits.
- grover_oracle: Constructs a Grover phase oracle for given target indices.
- grover_search: Runs Grover's algorithm for a set number of iterations to find a marked state.
- bbht_search: Universal exponential search for minimum, as per BBHT.
- find_min: Finds (probabilistically) the minimum in a quantum-inspired way.

Types:
------
- None (general utility functions only)
"""

import math
import random
from typing import Any, List, Optional, Tuple

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import AmplificationProblem, Grover


def random_finite_index(arr: List[float]) -> int:
    """
    Returns a random index from arr where the value is not inf.

    Parameters
    ----------
    arr : List[float]
        The array to sample from.

    Returns
    -------
    Int
        Index of a finite entry
    """
    valid_indices = [i for i, val in enumerate(arr) if val != float("inf")]
    return random.choice(valid_indices)


def pad_to_power_of_two_with_indices(
    indices: List[int], distances: List[float]
) -> Tuple[List[int], List[float]]:
    """
    Pad the index and value lists so their length is the next power of two.
    Entries beyond the original length are padded with inf.

    Parameters
    ----------
    indices : List[int]
        Valid indices.
    distances : List[float]
        Corresponding values.

    Returns
    -------
    Tuple[List[int], List[float]]
        Padded indices and padded values.
    """
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


def grover_oracle(n: int, targets: List[int]) -> QuantumCircuit:
    """
    Construct a phase oracle that marks the 'targets' basis states.

    Parameters
    ----------
    n : int
        Number of qubits.
    targets : List[int]
        List of indices to mark as solutions.

    Returns
    -------
    QuantumCircuit
        The oracle as a quantum circuit.
    """
    circ = QuantumCircuit(n)

    for target in targets:
        bitstring = format(target, f"0{n}b")

        for qubit, bit in enumerate(bitstring):
            if bit == "0":
                circ.x(qubit)

        circ.h(n - 1)
        if n == 1:
            circ.z(0)
        else:
            circ.mcx(list(range(n - 1)), n - 1)
        circ.h(n - 1)

        for qubit, bit in enumerate(reversed(bitstring)):
            if bit == "0":
                circ.x(qubit)

    return circ


def grover_search(
    size: int, marked_states: List[int], iterations: int
) -> Optional[int]:
    """
    Run Grover's algorithm with a given oracle and iteration count.

    Parameters
    ----------
    size : int
        Size of the search space.
    marked_states : List[int]
        Indices considered as solutions.
    iterations : int
        Number of Grover iterations.

    Returns
    -------
    Optional[int]
        Index of the found solution, or None if not found.
    """
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


def bbht_search(size: int, marked_states: List[int]) -> Tuple[Optional[int], int]:
    """
    Universal exponential search: Boyer–Brassard–Høyer–Tapp algorithm.

    Parameters
    ----------
    size : int
        Search space size.
    marked_states : List[int]
        Good states.

    Returns
    -------
    Tuple[Optional[int], int]
        (Found index/candidate, iteration cost)
    """
    if not marked_states:
        return None, 0

    lam = 6 / 5
    m = 1
    cost = 0
    initialization_cost = math.log2(size)

    while True:
        upper = max(1, int(m))
        j = random.randrange(upper)

        cost += initialization_cost

        candidate = grover_search(size=size, marked_states=marked_states, iterations=j)

        cost += j

        if candidate is not None:
            return candidate, cost

        if m >= math.sqrt(size):
            m = math.sqrt(size)
        else:
            m *= lam


def find_min(
    active_distances: List[float], time_limit: int = 1
) -> tuple[int, Any, float | Any, float]:
    """
    Finds (probabilistically) the minimum index and its value using a Grover-style approach.

    Parameters
    ----------
    active_distances : List[float]
        Array whose minimum is to be found.
    time_limit : int, optional
        Whether to enforce a time limit (default 1: yes).

    Returns
    -------
    Tuple[int, float, float, float]
        (Minimum index, minimum value, time used, time limit)
    """
    size = len(active_distances)
    threshold = random_finite_index(arr=active_distances)
    run_limit = 22.5 * math.sqrt(size) + 1.4 * math.log2(size)
    total_time = 0.0

    while True:
        marked_states = [
            i for i in range(size) if active_distances[i] < active_distances[threshold]
        ]
        if not marked_states:
            break

        y_prime, search_cost = bbht_search(size=size, marked_states=marked_states)

        total_time += search_cost
        if total_time > run_limit and time_limit == 1:
            break

        if y_prime is None:
            break

        if active_distances[y_prime] < active_distances[threshold]:
            threshold = y_prime

    return (
        threshold,
        active_distances[threshold],
        total_time,
        run_limit,
    )
