"""Reproduce all tables from the paper using pre-computed FDR results."""

import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "experiments", "results")


def reproduce_table1_wn18rr():
    """Reproduce Table 1: Overall FDR metrics on WN18RR."""
    path = os.path.join(RESULTS_DIR, "WN18RR", "fdr_summary.json")
    with open(path) as f:
        data = json.load(f)

    print("=" * 80)
    print("Table 1: Overall FDR Metrics on WN18RR (K=100)")
    print("=" * 80)
    print(f"{'Model':<12} {'MRR':<8} {'pi0':<8} {'R(0.05)':<10} {'locFDR<0.05':<12}")
    print("-" * 80)
    for model in ["TransE", "RotatE", "ComplEx", "ConvE"]:
        r = data[model]
        mrr = r.get("mrr", "N/A")
        print(f"{model:<12} {mrr:<8} {r['pi0_spline']:<8.3f} {r['bh_rejected']:<10} {r['locfdr_below_005']:<12}")
    print()


def reproduce_table3_fb15k():
    """Reproduce Table 3: Overall FDR metrics on FB15k-237."""
    path = os.path.join(RESULTS_DIR, "FB15k-237", "fdr_summary.json")
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Table 3: FB15k-237 results not available yet.")
        return

    print("=" * 80)
    print("Table 3: Overall FDR Metrics on FB15k-237 (K=100)")
    print("=" * 80)
    print(f"{'Model':<12} {'MRR':<8} {'pi0':<8} {'R(0.05)':<10} {'locFDR<0.05':<12}")
    print("-" * 80)
    for model in ["TransE", "RotatE", "ComplEx", "ConvE"]:
        r = data[model]
        mrr = r.get("mrr", "N/A")
        print(f"{model:<12} {mrr:<8} {r['pi0_spline']:<8.3f} {r['bh_rejected']:<10} {r['locfdr_below_005']:<12}")
    print()


if __name__ == "__main__":
    reproduce_table1_wn18rr()
    reproduce_table3_fb15k()
