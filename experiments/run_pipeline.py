"""
Run the complete FDR-KG evaluation pipeline on WN18RR and FB15k-237.

Requires pre-computed score files (positive and negative scores for each
model-dataset combination). Score files are stored in experiments/results/.

Usage:
    python run_pipeline.py --dataset WN18RR
    python run_pipeline.py --dataset FB15k-237
    python run_pipeline.py --dataset all
"""

import argparse
import json
import os
import sys
import numpy as np

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fdr_kg.pipeline import run_fdr_pipeline, FDRConfig, rejections_at_alpha
from fdr_kg.fdr_methods import storey_pi0_spline
from fdr_kg.utils import aggregate_per_relation


DATASETS = ["WN18RR", "FB15k-237"]
MODELS = ["TransE", "RotatE", "ComplEx", "ConvE"]

# Paths relative to this repository
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def load_scores(dataset: str, model: str, k: int = 100):
    """Load score files for a given dataset and model."""
    score_dir = os.path.join(RESULTS_DIR, dataset, model)
    pos_path = os.path.join(score_dir, f"positive_scores_K{k}.npy")
    neg_path = os.path.join(score_dir, f"negative_scores_K{k}.npy")
    rel_path = os.path.join(score_dir, "relation_ids.npy")

    if not (os.path.exists(pos_path) and os.path.exists(neg_path)):
        print(f"  [SKIP] Score files not found for {model} on {dataset}")
        return None

    positive = np.load(pos_path)
    negative = np.load(neg_path)
    relations = np.load(rel_path) if os.path.exists(rel_path) else None
    return {"positive": positive, "negative": negative, "relations": relations}


def run_dataset(dataset: str, k: int = 100):
    """Run the FDR pipeline for all models on one dataset."""
    print(f"\n{'='*60}")
    print(f"  Dataset: {dataset}")
    print(f"  K = {k}")
    print(f"{'='*60}")

    results = {}
    for model in MODELS:
        print(f"\n  Processing {model}...")
        data = load_scores(dataset, model, k)
        if data is None:
            continue

        config = FDRConfig(K=k, alpha_bh=0.05, storey_lambda=0.5)
        result = run_fdr_pipeline(data["positive"], data["negative"], config)

        results[model] = {
            "m": len(data["positive"]),
            "pi0_spline": result.pi0_spline,
            "pi0_storey": result.pi0_storey,
            "bh_rejected": result.bh_rejection_count,
            "by_rejected": result.by_rejection_count,
            "locfdr_below_005": result.locfdr_below_005,
            "bh_rejection_rate": result.bh_rejection_count / len(data["positive"]),
            "rejections_by_alpha": rejections_at_alpha(
                result.p_values, [0.01, 0.05, 0.10, 0.20]
            ),
        }

        # Per-relation analysis
        if data["relations"] is not None:
            per_rel = aggregate_per_relation(result.p_values, data["relations"])
            results[model]["per_relation_rejection_rates"] = per_rel

        print(f"    pi0_spline = {result.pi0_spline:.3f}")
        print(f"    BH rejected = {result.bh_rejection_count}")
        print(f"    BY rejected = {result.by_rejection_count}")
        print(f"    locFDR<0.05 = {result.locfdr_below_005}")

    # Save summary
    out_path = os.path.join(RESULTS_DIR, dataset, "fdr_summary.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Summary saved to {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Run FDR-KG Pipeline")
    parser.add_argument(
        "--dataset",
        type=str,
        default="WN18RR",
        choices=DATASETS + ["all"],
        help="Dataset to evaluate",
    )
    parser.add_argument("--K", type=int, default=100, help="Negative samples per triple")
    args = parser.parse_args()

    if args.dataset == "all":
        for ds in DATASETS:
            run_dataset(ds, args.K)
    else:
        run_dataset(args.dataset, args.K)


if __name__ == "__main__":
    main()
