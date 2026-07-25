"""
FDR-KG: Complete FDR Computation Pipeline.

This module implements the full evaluation pipeline:
1. Load pre-computed positive and negative scores
2. Compute empirical p-values
3. Apply BH FDR control
4. Compute Storey q-values
5. Compute Efron local FDR
6. Aggregate per-relation and per-model metrics
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Optional
from .pvalues import compute_p_values, compute_z_scores
from .fdr_methods import (
    benjamini_hochberg,
    benjamini_yekutieli,
    storey_qvalues,
    storey_pi0_spline,
    efron_locfdr,
)


@dataclass
class FDRConfig:
    """Configuration for the FDR pipeline.

    Attributes:
        K: Number of negative samples per test triple.
        alpha_bh: FDR level for BH procedure.
        storey_lambda: Tuning parameter for Storey's method.
    """
    K: int = 100
    alpha_bh: float = 0.05
    storey_lambda: float = 0.5


@dataclass
class FDRResult:
    """Results from the FDR-KG pipeline.

    Attributes:
        p_values: Empirical p-values (m,).
        z_scores: Z-scores (m,).
        bh_rejected: Boolean mask of BH-rejected hypotheses (m,).
        bh_rejection_count: Number of BH-rejected hypotheses.
        by_rejected: Boolean mask of BY-rejected hypotheses (m,).
        by_rejection_count: Number of BY-rejected hypotheses.
        qvalues: Storey q-values (m,).
        pi0_storey: Estimated null proportion (Storey fixed lambda).
        pi0_spline: Estimated null proportion (Storey spline).
        locfdr: Efron local FDR values (m,).
        locfdr_below_005: Number of triples with local FDR < 0.05.
    """
    p_values: np.ndarray = field(repr=False)
    z_scores: np.ndarray = field(repr=False)
    bh_rejected: np.ndarray = field(repr=False)
    bh_rejection_count: int = 0
    by_rejected: np.ndarray = field(repr=False)
    by_rejection_count: int = 0
    qvalues: np.ndarray = field(repr=False)
    pi0_storey: float = 1.0
    pi0_spline: float = 1.0
    locfdr: np.ndarray = field(repr=False)
    locfdr_below_005: int = 0


def run_fdr_pipeline(
    positive_scores: np.ndarray,
    negative_scores: np.ndarray,
    config: Optional[FDRConfig] = None,
) -> FDRResult:
    """Run the complete FDR-KG evaluation pipeline.

    Args:
        positive_scores: Array of shape (m,) with one positive score per triple.
        negative_scores: Array of shape (m, K) with K negative scores per triple.
        config: FDR pipeline configuration.

    Returns:
        FDRResult with all computed metrics.
    """
    if config is None:
        config = FDRConfig()

    m = len(positive_scores)

    # Step 1: Empirical p-values
    p_values = compute_p_values(positive_scores, negative_scores)
    z_scores = compute_z_scores(positive_scores, negative_scores)

    # Step 2: BH FDR control
    bh_rejected, bh_count = benjamini_hochberg(p_values, config.alpha_bh)

    # Step 3: BY FDR control (arbitrary dependence)
    by_rejected, by_count = benjamini_yekutieli(p_values, config.alpha_bh)

    # Step 4: Storey q-values
    qvalues, pi0_storey = storey_qvalues(p_values, config.storey_lambda)

    # Step 5: Storey pi0 spline
    pi0_spline = storey_pi0_spline(p_values)

    # Step 6: Efron local FDR
    locfdr = efron_locfdr(z_scores)
    locfdr_below_005 = int(np.sum(locfdr < 0.05))

    return FDRResult(
        p_values=p_values,
        z_scores=z_scores,
        bh_rejected=bh_rejected,
        bh_rejection_count=bh_count,
        by_rejected=by_rejected,
        by_rejection_count=by_count,
        qvalues=qvalues,
        pi0_storey=pi0_storey,
        pi0_spline=pi0_spline,
        locfdr=locfdr,
        locfdr_below_005=locfdr_below_005,
    )


def rejections_at_alpha(
    p_values: np.ndarray, alphas: list[float]
) -> Dict[float, int]:
    """Compute BH rejection counts at multiple FDR levels.

    Args:
        p_values: Array of m p-values.
        alphas: List of FDR thresholds.

    Returns:
        Dictionary mapping alpha -> rejection count.
    """
    results = {}
    for alpha in alphas:
        _, count = benjamini_hochberg(p_values, alpha)
        results[alpha] = count
    return results
