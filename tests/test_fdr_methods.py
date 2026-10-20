"""Deterministic statistical invariants for the released FDR implementations.

These tests exercise existing behavior. They do not recompute or modify archived
manuscript results, and passing them is not a proof of FDR control for every design.
"""

import unittest

import numpy as np

from fdr_kg.fdr_methods import (
    benjamini_hochberg,
    benjamini_yekutieli,
    efron_locfdr,
    storey_pi0_spline,
    storey_qvalues,
)


class TestFalseDiscoveryRateMethods(unittest.TestCase):
    def test_bh_and_by_known_thresholds(self):
        p = np.array([0.8, 0.03, 0.001, 0.02])
        bh, n_bh = benjamini_hochberg(p, alpha=0.05)
        by, n_by = benjamini_yekutieli(p, alpha=0.05)
        np.testing.assert_array_equal(bh, [False, True, True, True])
        np.testing.assert_array_equal(by, [False, False, True, False])
        self.assertEqual(n_bh, 3)
        self.assertEqual(n_by, 1)

    def test_no_rejections(self):
        p = np.array([0.3, 0.7, 1.0])
        for method in (benjamini_hochberg, benjamini_yekutieli):
            with self.subTest(method=method.__name__):
                rejected, n = method(p, alpha=0.05)
                self.assertEqual(n, 0)
                np.testing.assert_array_equal(rejected, np.zeros(3, dtype=bool))

    def test_by_rejections_subset_of_bh(self):
        rng = np.random.default_rng(2026)
        p = rng.uniform(size=500)
        p[:10] = np.geomspace(1e-7, 1e-3, 10)
        for level in (0.01, 0.05, 0.1):
            with self.subTest(alpha=level):
                bh, n_bh = benjamini_hochberg(p, alpha=level)
                by, n_by = benjamini_yekutieli(p, alpha=level)
                self.assertTrue(np.all(~by | bh))
                self.assertEqual(n_bh, int(bh.sum()))
                self.assertEqual(n_by, int(by.sum()))

    def test_storey_qvalues_known_example_and_monotonicity(self):
        p = np.array([0.8, 0.03, 0.001, 0.02])
        q, pi0 = storey_qvalues(p, lambda_param=0.5)
        self.assertAlmostEqual(pi0, 0.5)
        np.testing.assert_allclose(q, [0.4, 0.02, 0.002, 0.02])
        self.assertTrue(np.all((q >= 0) & (q <= 1)))
        self.assertTrue(np.all(np.diff(q[np.argsort(p)]) >= -1e-12))

    def test_storey_permutation_equivariance(self):
        rng = np.random.default_rng(101)
        p = rng.uniform(size=100)
        permutation = rng.permutation(len(p))
        baseline, pi0 = storey_qvalues(p)
        permuted, pi0_perm = storey_qvalues(p[permutation])
        self.assertAlmostEqual(pi0, pi0_perm)
        np.testing.assert_allclose(permuted, baseline[permutation])

    def test_local_fdr_is_bounded_for_nondegenerate_scores(self):
        rng = np.random.default_rng(7)
        z = rng.normal(size=120)
        output = efron_locfdr(z)
        self.assertEqual(output.shape, z.shape)
        self.assertTrue(np.isfinite(output).all())
        self.assertTrue(np.all((0.0 <= output) & (output <= 1.0)))

    def test_invalid_pvalue_vectors_raise_instead_of_silent_outputs(self):
        inputs = [
            np.array([]),
            np.array([0.1, -0.001]),
            np.array([0.1, 1.001]),
            np.array([0.2, np.nan]),
            np.array([0.2, np.inf]),
            np.array([[0.1, 0.2]]),
        ]
        for method in (benjamini_hochberg, benjamini_yekutieli, storey_qvalues, storey_pi0_spline):
            for p in inputs:
                with self.subTest(method=method.__name__, p=repr(p)):
                    with self.assertRaisesRegex(ValueError, "p_values"):
                        method(p)

    def test_invalid_alpha_fails_closed(self):
        for method in (benjamini_hochberg, benjamini_yekutieli):
            for alpha in (-0.01, 1.01, np.nan, np.inf, [0.05]):
                with self.subTest(method=method.__name__, alpha=repr(alpha)):
                    with self.assertRaisesRegex(ValueError, "alpha"):
                        method(np.array([0.01, 0.5]), alpha=alpha)

    def test_invalid_storey_lambda_fails_closed(self):
        for bad in (-0.001, 1.0, 1.01, np.inf, np.nan, [0.5]):
            with self.subTest(lambda_param=repr(bad)):
                with self.assertRaisesRegex(ValueError, "lambda_param"):
                    storey_qvalues(np.array([0.01, 0.5]), lambda_param=bad)

    def test_pvalue_boundaries_remain_permitted(self):
        p = np.array([0.0, 1.0, 0.1])
        for method in (benjamini_hochberg, benjamini_yekutieli):
            rejected, count = method(p)
            self.assertTrue(rejected[0])
            self.assertFalse(rejected[1])
            self.assertEqual(count, int(rejected.sum()))
        for alpha in (0.0, 1.0):
            rejected, count = benjamini_hochberg(p, alpha)
            self.assertEqual(count, int(rejected.sum()))


if __name__ == "__main__":
    unittest.main()
