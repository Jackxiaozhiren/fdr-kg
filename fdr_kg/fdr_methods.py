"""FDR control methods: Benjamini-Hochberg, Storey q-value, Efron local FDR."""

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.stats import gaussian_kde
from typing import Tuple


def benjamini_hochberg(p_values: np.ndarray, alpha: float = 0.05) -> Tuple[np.ndarray, int]:
    """Apply Benjamini-Hochberg FDR control.

    Args:
        p_values: Array of m p-values.
        alpha: FDR threshold (default 0.05).

    Returns:
        rejected: Boolean array indicating rejected hypotheses.
        n_rejected: Number of rejected hypotheses.
    """
    m = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    thresholds = (np.arange(1, m + 1) / m) * alpha
    # Find largest k where p_(k) <= (k/m) * alpha
    below = sorted_p <= thresholds
    if not np.any(below):
        return np.zeros(m, dtype=bool), 0
    k = np.max(np.where(below)) + 1  # 1-indexed count
    rejected = np.zeros(m, dtype=bool)
    rejected[sorted_indices[:k]] = True
    return rejected, int(k)


def benjamini_yekutieli(p_values: np.ndarray, alpha: float = 0.05) -> Tuple[np.ndarray, int]:
    """Apply Benjamini-Yekutieli FDR control (arbitrary dependence).

    Args:
        p_values: Array of m p-values.
        alpha: FDR threshold (default 0.05).

    Returns:
        rejected: Boolean array indicating rejected hypotheses.
        n_rejected: Number of rejected hypotheses.
    """
    m = len(p_values)
    c_m = np.sum(1.0 / np.arange(1, m + 1))
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    thresholds = (np.arange(1, m + 1) / m) * (alpha / c_m)
    below = sorted_p <= thresholds
    if not np.any(below):
        return np.zeros(m, dtype=bool), 0
    k = np.max(np.where(below)) + 1
    rejected = np.zeros(m, dtype=bool)
    rejected[sorted_indices[:k]] = True
    return rejected, int(k)


def storey_qvalues(p_values: np.ndarray, lambda_param: float = 0.5) -> Tuple[np.ndarray, float]:
    """Compute Storey q-values with pi0 estimation.

    Args:
        p_values: Array of m p-values.
        lambda_param: Tuning parameter for pi0 estimation (default 0.5).

    Returns:
        qvalues: Array of q-values (FDR-adjusted).
        pi0: Estimated null proportion.
    """
    m = len(p_values)
    pi0 = np.sum(p_values > lambda_param) / (m * (1 - lambda_param))
    pi0 = min(pi0, 1.0)

    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]

    # q-value = pi0 * m * p_(i) / i
    qvalues = np.zeros(m)
    cumulative_min = 1.0
    for i in range(m - 1, -1, -1):
        q_i = pi0 * m * sorted_p[i] / (i + 1)
        cumulative_min = min(cumulative_min, q_i)
        qvalues[sorted_indices[i]] = cumulative_min

    return qvalues, pi0


def storey_pi0_spline(p_values: np.ndarray) -> float:
    """Estimate pi0 using cubic spline extrapolation.

    Evaluates pi0(lambda) at lambdas in [0.1, 0.9] and fits a cubic spline
    to extrapolate pi0(1).

    Args:
        p_values: Array of m p-values.

    Returns:
        pi0: Estimated null proportion.
    """
    lambdas = np.arange(0.05, 0.95, 0.05)
    m = len(p_values)
    pi0_lambdas = np.array([np.sum(p_values > lam) / (m * (1 - lam)) for lam in lambdas])

    # Cubic spline fit
    spline = UnivariateSpline(lambdas, pi0_lambdas, k=3, s=0.5)
    pi0 = float(spline(1.0))
    pi0 = np.clip(pi0, 0.0, 1.0)
    return pi0


def efron_locfdr(z_scores: np.ndarray, null_mean: float = 0.0, null_sd: float = 1.0) -> np.ndarray:
    """Compute Efron's local FDR from z-scores.

    Uses Gaussian KDE for density estimation.

    Args:
        z_scores: Array of z-scores.
        null_mean: Mean of the null distribution (default 0).
        null_sd: Standard deviation of the null distribution (default 1).

    Returns:
        locfdr: Local FDR values.
    """
    # Density of observed z-scores via KDE (Silverman's rule of thumb)
    kde = gaussian_kde(z_scores)
    f_z = kde(z_scores)

    # Density of theoretical null
    f0_z = np.exp(-0.5 * ((z_scores - null_mean) / null_sd) ** 2) / (null_sd * np.sqrt(2 * np.pi))

    # pi0 estimate from the central matching method
    # Use the median of the ratio near z = 0
    center_mask = np.abs(z_scores) < 0.5
    if np.sum(center_mask) > 0:
        ratios = f_z[center_mask] / (f0_z[center_mask] + 1e-10)
        pi0 = np.median(ratios)
    else:
        pi0 = 1.0

    locfdr = pi0 * f0_z / (f_z + 1e-10)
    locfdr = np.clip(locfdr, 0.0, 1.0)
    return locfdr
