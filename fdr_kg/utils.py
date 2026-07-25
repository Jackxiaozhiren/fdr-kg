"""Utility functions for the FDR-KG pipeline."""

import numpy as np
from typing import Dict, List


def load_score_file(positive_path: str, negative_path: str) -> tuple:
    """Load positive and negative scores from numpy files.

    Args:
        positive_path: Path to .npy file with positive scores (m,).
        negative_path: Path to .npy file with negative scores (m, K).

    Returns:
        Tuple of (positive_scores, negative_scores).
    """
    positive_scores = np.load(positive_path)
    negative_scores = np.load(negative_path)
    return positive_scores, negative_scores


def aggregate_per_relation(
    p_values: np.ndarray,
    relations: np.ndarray,
    metric: str = "rejection_rate",
    alpha: float = 0.05,
) -> Dict:
    """Aggregate FDR results per relation.

    Args:
        p_values: Array of p-values.
        relations: Array of relation indices of same length as p_values.
        metric: Aggregation metric.
        alpha: FDR threshold.

    Returns:
        Dictionary mapping relation -> aggregated value.
    """
    unique_relations = np.unique(relations)
    result = {}
    for rel in unique_relations:
        mask = relations == rel
        rel_p = p_values[mask]
        if metric == "rejection_rate":
            result[int(rel)] = np.mean(rel_p < alpha)
        elif metric == "mean_p":
            result[int(rel)] = np.mean(rel_p)
        elif metric == "count":
            result[int(rel)] = len(rel_p)
    return result


def compute_mrr(scores: np.ndarray, positive_indices: np.ndarray) -> float:
    """Compute Mean Reciprocal Rank.

    Args:
        scores: Score matrix of shape (m, K+1) where index 0 is the positive.
        positive_indices: Array of shape (m,) indicating the positive column.

    Returns:
        MRR value.
    """
    m = scores.shape[0]
    reciprocal_ranks = np.zeros(m)
    for i in range(m):
        # Rank of the positive triple among all candidates
        sorted_indices = np.argsort(-scores[i])
        rank = np.where(sorted_indices == positive_indices[i])[0][0] + 1
        reciprocal_ranks[i] = 1.0 / rank
    return float(np.mean(reciprocal_ranks))
