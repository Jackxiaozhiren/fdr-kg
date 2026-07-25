"""Empirical p-value construction from embedding scores via permutation-based negative sampling."""

import numpy as np


def compute_empirical_p_value(positive_score: float, negative_scores: np.ndarray) -> float:
    """Compute empirical p-value for one test triple.

    The p-value is the proportion of negative samples with a score
    greater than or equal to the observed positive score.

    Args:
        positive_score: Score of the ground-truth triple.
        negative_scores: Array of K negative sample scores.

    Returns:
        Empirical p-value in [1/(K+1), 1].
    """
    K = len(negative_scores)
    count_extreme = np.sum(negative_scores >= positive_score)
    return (count_extreme + 1) / (K + 1)


def compute_p_values(positive_scores: np.ndarray, negative_scores: np.ndarray) -> np.ndarray:
    """Compute empirical p-values for all test triples.

    Args:
        positive_scores: Array of shape (m,) with one positive score per test triple.
        negative_scores: Array of shape (m, K) with K negative scores per test triple.

    Returns:
        Array of shape (m,) with empirical p-values.
    """
    m = len(positive_scores)
    K = negative_scores.shape[1]
    n_extreme = np.sum(negative_scores >= positive_scores[:, np.newaxis], axis=1)
    return (n_extreme + 1) / (K + 1)


def compute_z_scores(positive_scores: np.ndarray, negative_scores: np.ndarray) -> np.ndarray:
    """Compute z-scores from positive and negative score distributions.

    Computes empirical z-score = (positive - mean(negatives)) / std(negatives).

    Args:
        positive_scores: Array of shape (m,).
        negative_scores: Array of shape (m, K).

    Returns:
        Array of shape (m,) with z-scores.
    """
    neg_mean = np.mean(negative_scores, axis=1)
    neg_std = np.std(negative_scores, axis=1, ddof=1)
    neg_std = np.maximum(neg_std, 1e-10)  # avoid division by zero
    return (positive_scores - neg_mean) / neg_std
