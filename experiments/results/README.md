# FDR-KG Experimental Results

**Important**: The `.npy` score files (positive_scores_K*.npy, negative_scores_K*.npy) required to run the FDR pipeline from scratch are not included in this repository due to file size limits. To reproduce the results:

1. Install dependencies: `pip install -r requirements.txt`
2. Train models and generate scores using PyKEEN, or
3. Download pre-computed score files from the [GitHub Release](https://github.com/Jackxiaozhiren/fdr-kg/releases)

The `fdr_summary.json` files in the WN18RR and FB15k-237 directories contain the pre-computed FDR results used in the paper. The `per_relation_fdr_full.csv` contains per-relation statistics for FB15k-237.

## Directory Structure

```
results/
├── WN18RR/
│   ├── fdr_summary.json     ← Pre-computed FDR results (Table 1)
│   ├── TransE/               ← Score files (available on request)
│   ├── RotatE/
│   ├── ComplEx/
│   └── ConvE/
├── FB15k-237/
│   ├── fdr_summary.json     ← Pre-computed FDR results (Table 3)
│   ├── per_relation_fdr_full.csv
│   ├── TransE/               ← Score files (available on request)
│   ├── RotatE/
│   ├── ComplEx/
│   └── ConvE/
└── multi_seed/               ← Multi-seed stability data
```

## Results Summary

### WN18RR (2,924 test triples, K=100)

| Model | pi0_spline | BH R(0.05) | BY R(0.05) | locFDR<0.05 | MRR |
|-------|:----------:|:----------:|:----------:|:-----------:|:---:|
| TransE | 0.494 | 263 | 153 | 1124 | 0.560 |
| RotatE | 0.259 | 1100 | 748 | 1960 | 0.601 |
| ComplEx | 0.754 | 0 | 0 | 20 | 0.274 |
| ConvE | 0.452 | 738 | 462 | 1540 | 0.469 |

### FB15k-237 (20,438 test triples, K=100)

| Model | pi0_spline | BH R(0.05) | BY R(0.05) | locFDR<0.05 | MRR |
|-------|:----------:|:----------:|:----------:|:-----------:|:---:|
| TransE | 0.716 | 1289 | 716 | 7146 | 0.340 |
| RotatE | 0.685 | 1567 | 889 | 7792 | 0.354 |
| ComplEx | 0.851 | 0 | 0 | 94 | 0.215 |
| ConvE | 0.721 | 1422 | 801 | 7204 | 0.334 |
