"""Empirical p-values and z-scores from negative-sampling embedding scores."""

import numpy as np


def _score_arrays(
    positive_scores: np.ndarray, negative_scores: np.ndarray, *, min_negatives: int
) -> tuple[np.ndarray, np.ndarray]:
    """Check observations are paired, finite and shaped as (m,) and (m, K)."""
    try:
        positive = np.asarray(positive_scores, dtype=float)
        negative = np.asarray(negative_scores, dtype=float)
    except (ValueError, TypeError) as exc:
        raise ValueError("scores must contain numeric values") from exc
    if positive.ndim != 1 or positive.size == 0:
        raise ValueError("positive_scores must be a non-empty one-dimensional vector")
    if negative.ndim != 2 or negative.shape[0] != positive.size:
        raise ValueError("negative_scores must have shape (len(positive_scores), K)")
    if negative.shape[1] < min_negatives:
        raise ValueError(f"negative_scores requires at least {min_negatives} samples per row")
    if not (np.all(np.isfinite(positive)) and np.all(np.isfinite(negative))):
        raise ValueError("scores must be finite (no NaN or infinity)")
    return positive, negative


def compute_empirical_p_value(positive_score: float, negative_scores: np.ndarray) -> float:
    """Estimate the right-tail empirical p-value with the (count + 1)/(K + 1) rule.

    At least one finite negative sample is required. The score must be scalar and
    finite so that NaN comparisons cannot silently become non-extreme samples.
    """
    try:
        positive = np.asarray(positive_score, dtype=float)
        negatives = np.asarray(negative_scores, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("scores must contain numeric values") from exc
    if positive.ndim != 0 or not np.isfinite(positive):
        raise ValueError("positive_score must be a finite scalar")
    if negatives.ndim != 1 or negatives.size == 0 or not np.all(np.isfinite(negatives)):
        raise ValueError("negative_scores must be a non-empty finite one-dimensional vector")
    K = len(negatives)
    count_extreme = np.sum(negatives >= positive)
    return (count_extreme + 1) / (K + 1)


def compute_p_values(positive_scores: np.ndarray, negative_scores: np.ndarray) -> np.ndarray:
    """Return the empirical p-value per observation.

    positive_scores is (m,), negative_scores is (m,K), m >= 1 and K >= 1.
    """
    positive, negative = _score_arrays(positive_scores, negative_scores, min_negatives=1)
    K = negative.shape[1]
    n_extreme = np.sum(negative >= positive[:, np.newaxis], axis=1)
    return (n_extreme + 1) / (K + 1)


def compute_z_scores(positive_scores: np.ndarray, negative_scores: np.ndarray) -> np.ndarray:
    """Standardize positive scores against their paired negatives.

    Uses sample SD (ddof=1), requiring K >= 2. Zero-variance negative rows
    retain the established 1e-10 SD floor.
    """
    positive, negative = _score_arrays(positive_scores, negative_scores, min_negatives=2)
    neg_mean = np.mean(negative, axis=1)
    neg_std = np.std(negative, axis=1, ddof=1)
    neg_std = np.maximum(neg_std, 1e-10)
    return (positive - neg_mean) / neg_std
