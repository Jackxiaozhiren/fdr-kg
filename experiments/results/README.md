# FDR-KG Experimental Results

## Directory Structure

```
results/
├── WN18RR/
│   ├── TransE/
│   │   ├── positive_scores_K100.npy  (2924,)
│   │   ├── negative_scores_K100.npy  (2924, 100)
│   │   └── relation_ids.npy          (2924,)
│   ├── RotatE/
│   ├── ComplEx/
│   ├── ConvE/
│   └── fdr_summary.json
├── FB15k-237/
│   ├── TransE/
│   ├── RotatE/
│   ├── ComplEx/
│   ├── ConvE/
│   ├── fdr_summary.json
│   └── per_relation_fdr_full.csv
└── multi_seed/
    ├── TransE_seed42_K100.npy
    ├── TransE_seed123_K100.npy
    ├── ConvE_seed42_K100.npy
    └── ... (multi-seed stability data)
```

## Results Summary

### WN18RR (2,924 test triples, K=100)

| Model | pi0_spline | BH R(0.05) | BY R(0.05) | locFDR<0.05 |
|-------|:----------:|:----------:|:----------:|:-----------:|
| TransE | 0.494 | 263 | 153 | 1124 |
| RotatE | 0.259 | 1100 | 748 | 1960 |
| ComplEx | 0.754 | 0 | 0 | 20 |
| ConvE | 0.452 | 738 | 462 | 1540 |

### FB15k-237 (20,438 test triples, K=100)

| Model | pi0_spline | BH R(0.05) | BY R(0.05) | locFDR<0.05 |
|-------|:----------:|:----------:|:----------:|:-----------:|
| TransE | 0.716 | 1289 | 716 | 7146 |
| RotatE | 0.685 | 1567 | 889 | 7792 |
| ComplEx | 0.851 | 0 | 0 | 94 |
| ConvE | 0.721 | 1422 | 801 | 7204 |

### Key Findings
- Null proportion pi0: 0.259 (RotatE, WN18RR) to 0.851 (ComplEx, FB15k-237)
- 26-85% of test triples indistinguishable from noise
- Per-relation rejection rates: 9.1%--96.5% (TransE, WN18RR)
- ComplEx: zero discoveries under BH on both datasets
- ConvE vs TransE ranking flip: ConvE MRR lower, BH rejection rate 2.8x higher
