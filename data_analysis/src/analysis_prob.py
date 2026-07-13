from config import DIJKSTRA_RESULTS_DIRECTORY
from data_analysis.src.helpers import (
    read_results_from_json,
    save_merged_prob_stats_by_file,
)


def prob_stats_analysis():
    dijkstra_results = read_results_from_json(directory=DIJKSTRA_RESULTS_DIRECTORY)
    final_result_dict = compute_and_merge_all_probs(all_data=dijkstra_results)
    save_merged_prob_stats_by_file(merged_stats_dict=final_result_dict)


def compute_dijkstra_success_prob(all_data):
    """
    For each file, computes success probability if dijkstra per vertex.
    Returns: { filename: {vertex: {...}} }
    """
    results = {}
    for filename, file_data in all_data.items():
        if not filename.startswith("quantum"):
            continue
        file_result = {}
        vertices = file_data["vertices"]
        invalid_counts = file_data["invalid_counts"]
        length = len(invalid_counts[0])
        for i, v in enumerate(vertices):
            invalid_total = sum(invalid_counts[i])
            success_prob = 1 - (invalid_total / length) if length > 0 else 0
            file_result[v] = {
                "dijkstra_success_prob": success_prob,
                "invalid_total": invalid_total,
                "calls_total": length,
            }
        results[filename] = file_result
    return results


def compute_find_min_success_prob(all_data):
    """
    For each file, computes success probability against mismatch counts per vertex.
    Returns: { filename: {vertex: {...}} }
    """
    results = {}
    for filename, file_data in all_data.items():
        if not filename.startswith("quantum"):
            continue
        file_result = {}
        vertices = file_data["vertices"]
        mismatch_counts = file_data["mismatch_counts"]
        search_calls = file_data["search_calls"]
        for i, v in enumerate(vertices):
            mismatch_total = sum(mismatch_counts[i])
            search_total = int(sum(search_calls[i]))
            success_prob = (
                1 - (mismatch_total / search_total) if search_total > 0 else 0
            )
            file_result[v] = {
                "find_min_success_prob": success_prob,
                "mismatch_total": mismatch_total,
                "search_total": search_total,
            }
        results[filename] = file_result
    return results


def compute_mismatch_without_invalid_prob(all_data):
    """
    Computes (per file!) for each vertex, the probability that a mismatch did NOT result in invalid.
    Returns: { filename: {vertex: {...}} }
    """
    results = {}
    for filename, file_data in all_data.items():
        if not filename.startswith("quantum"):
            continue
        file_result = {}
        vertices = file_data["vertices"]
        mismatch_counts = file_data["mismatch_counts"]
        invalid_counts = file_data["invalid_counts"]
        for i, v in enumerate(vertices):
            mismatch_total = 0
            mismatch_and_invalid = 0
            for mismatch, invalid in zip(mismatch_counts[i], invalid_counts[i]):
                if mismatch > 0:
                    mismatch_total += 1
                    if invalid > 0:
                        mismatch_and_invalid += 1
            prob = (
                1 - (mismatch_and_invalid / mismatch_total) if mismatch_total > 0 else 0
            )
            file_result[v] = {
                "mismatch_without_invalid_prob": prob,
                "mismatch_and_invalid": mismatch_and_invalid,
                "mismatch_total": mismatch_total,
            }
        results[filename] = file_result
    return results


def compute_invalid_when_mismatch_prob(all_data):
    """
    Computes (per file!) for each vertex, the probability that when a mismatch happened it resulted in invalid dijkstra result
    Returns: { filename: {vertex: {...}} }
    """
    results = {}
    for filename, file_data in all_data.items():
        if not filename.startswith("quantum"):
            continue
        file_result = {}
        vertices = file_data["vertices"]
        mismatch_counts = file_data["mismatch_counts"]
        invalid_counts = file_data["invalid_counts"]
        for i, v in enumerate(vertices):
            mismatch_total = 0
            mismatch_and_invalid = 0
            for mismatch, invalid in zip(mismatch_counts[i], invalid_counts[i]):
                if mismatch > 0:
                    mismatch_total += 1
                    if invalid > 0:
                        mismatch_and_invalid += 1
            prob = (mismatch_and_invalid / mismatch_total) if mismatch_total > 0 else 0
            file_result[v] = {
                "invalid_when_mismath_prob": prob,
                "mismatch_and_invalid": mismatch_and_invalid,
                "mismatch_total": mismatch_total,
            }
        results[filename] = file_result
    return results


def compute_and_merge_all_probs(all_data):
    dijkstra_dict = compute_dijkstra_success_prob(all_data)
    find_min_dict = compute_find_min_success_prob(all_data)
    mismatch_wo_invalid_dict = compute_mismatch_without_invalid_prob(all_data)
    invalid_when_mismatch_dict = compute_invalid_when_mismatch_prob(all_data)

    merged_results = {}

    for filename in all_data:
        if not filename.startswith("quantum"):
            continue
        # Keep this order!
        vertices = all_data[filename]["vertices"]
        merged_results[filename] = {}
        for v in vertices:
            merged_entry = {}
            if filename in dijkstra_dict and v in dijkstra_dict[filename]:
                merged_entry.update(dijkstra_dict[filename][v])
            if filename in find_min_dict and v in find_min_dict[filename]:
                merged_entry.update(find_min_dict[filename][v])
            if (
                filename in mismatch_wo_invalid_dict
                and v in mismatch_wo_invalid_dict[filename]
            ):
                merged_entry.update(mismatch_wo_invalid_dict[filename][v])
            if (
                filename in invalid_when_mismatch_dict
                and v in invalid_when_mismatch_dict[filename]
            ):
                merged_entry.update(invalid_when_mismatch_dict[filename][v])
            merged_results[filename][v] = merged_entry

    return merged_results
