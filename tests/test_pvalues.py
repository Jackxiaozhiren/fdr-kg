"""Paired-score validation and reproducibility checks for empirical p-values."""

import unittest

import numpy as np

from fdr_kg.pvalues import compute_empirical_p_value, compute_p_values, compute_z_scores


class TestPairedScoreValidation(unittest.TestCase):
    def test_empirical_values_match_scalar_reference(self):
        p = np.array([0.5, 0.4, 1.0])
        n = np.array([[0.8, 0.3, 0.4], [0.2, 0.6, 0.4], [0.1, 0.2, 0.3]])
        out = compute_p_values(p, n)
        np.testing.assert_allclose(out, [0.5, 0.75, 0.25])
        for idx, result in enumerate(out):
            self.assertEqual(result, compute_empirical_p_value(p[idx], n[idx]))

    def test_single_negative_valid_for_pvalue_not_z_score(self):
        p = np.array([0.5])
        n = np.array([[0.2]])
        np.testing.assert_allclose(compute_p_values(p, n), [0.5])
        with self.assertRaisesRegex(ValueError, "at least 2"):
            compute_z_scores(p, n)

    def test_mismatched_lengths_are_rejected(self):
        p = np.array([0.1])
        n = np.array([[0.2, 0.3], [0.3, 0.4]])
        for func in (compute_p_values, compute_z_scores):
            with self.subTest(func=func.__name__):
                with self.assertRaisesRegex(ValueError, "shape"):
                    func(p, n)

    def test_nonfinite_inputs_are_rejected(self):
        base = np.array([0.5])
        samples = np.array([[0.2, 0.1]])
        for func in (compute_p_values, compute_z_scores):
            for p, n in ((np.array([np.nan]), samples),
                         (base, np.array([[np.inf, 0.1]]))):
                with self.subTest(func=func.__name__, p=str(p), n=str(n)):
                    with self.assertRaisesRegex(ValueError, "finite"):
                        func(p, n)

    def test_empty_and_invalid_shapes_are_rejected(self):
        bad = [
            (np.array([]), np.empty((0, 2))),
            (np.array([[0.5]]), np.array([[0.2, 0.1]])),
            (np.array([0.5]), np.array([0.2, 0.1])),
            (np.array([0.5]), np.empty((1, 0))),
        ]
        for fn in (compute_p_values, compute_z_scores):
            for p, n in bad:
                with self.subTest(fn=fn.__name__, p=p.shape, n=n.shape):
                    with self.assertRaises(ValueError):
                        fn(p, n)

    def test_scalar_score_validation(self):
        for positive, negatives in (
            (np.nan, [0.2, 0.3]),
            (0.5, []),
            (0.5, [np.nan, 0.3]),
            (0.5, [[0.3, 0.4]]),
        ):
            with self.subTest(positive=str(positive), negatives=str(negatives)):
                with self.assertRaises(ValueError):
                    compute_empirical_p_value(positive, negatives)

    def test_z_score_known_reference_and_zero_variance(self):
        np.testing.assert_allclose(
            compute_z_scores(np.array([3.0]), np.array([[1.0, 2.0, 3.0]])),
            [1.0],
        )
        self.assertTrue(
            np.isfinite(compute_z_scores(np.array([3.0]), np.array([[2.0, 2.0]]))).all()
        )


if __name__ == "__main__":
    unittest.main()
