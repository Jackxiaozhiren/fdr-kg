# FDR-KG: Statistical Quality Assurance for Knowledge Graph Link Prediction

This repository hosts the FDR-KG framework and the source material for:

> **Reliable Knowledge Discovery in Knowledge Graphs: A Statistical Quality Assurance Framework for Link Prediction**
> Zhiren Xiao
> Submitted to **Expert Systems with Applications (Elsevier)**

## Status note

An earlier version of this study was previously submitted to *Knowledge-Based Systems* (Elsevier) and was not
accepted; the journal flagged unintentional textual overlap. The manuscript has been systematically rewritten,
the experimental protocol corrected, and the WN18RR evidence regenerated under a frozen, hash-verified protocol
before being submitted to ESWA. Historical KBS-era materials are retained under `historical/` for audit only and
do **not** reflect the current submission.

## Overview

The FDR-KG framework formulates a **conditional benchmark diagnostic** for knowledge graph (KG) link prediction.
For each retained test triple it samples $K$ filtered tail corruptions, compares the observed score with the
sampled score distribution, and derives an empirical $p$-value that measures score extremeness under the declared
candidate-tail sampling scheme. It then applies the standard largest-$k$ Benjamini–Hochberg rule and Storey's
fixed-lambda $\hat\pi_0$ estimator as benchmark diagnostics. These quantities describe score behavior under the
declared conditional scheme; they do not by themselves assert factual truth in a complete KG or provide
unconditional validity or deployment guarantees.

**Accepted evidence (WN18RR, seed 42, 2,924 retained test triples, K=100):**

| Model | Sampled MRR | $\hat\pi_0$ | BH rejections (rate) |
|---|---|---|---|
| RotatE | 0.5882 | 0.2510 | 1,751 (59.88%) |
| ConvE (inverse-triple exception) | 0.5360 | 0.2770 | 1,527 (52.22%) |
| TransE | 0.5077 | 0.2873 | 1,438 (49.18%) |
| ComplEx | 0.0709 | 0.7503 | 0 (0.00%) |

Sampled MRR and BH-rate rankings agree, with RotatE leading both. Multi-seed (42, 123, 456) BH-rate sample
coefficients of variation are 0.54% (TransE), 0.39% (RotatE), and 1.09% (ConvE). Accepted sensitivity covers
$K \in \{25,50,100\}$ and $\lambda \in \{0.3,0.5,0.7\}$ only. FB15k-237 historical results are not part of the
accepted evidence and are quarantined.

## Repository Structure

- `fdr_kg/` — Core Python package (empirical p-value construction, BH, Storey, pipeline)
- `experiments/`, `analysis/` — KBS-era run scripts, configurations, and analysis outputs
- `historical/` — Superseded KBS-era manuscript and submission package (2026-07-26), kept for audit; contains
  outdated numbers and must not be treated as the current submission
- `requirements.txt`, `LICENSE`

## Reproducibility

The numbers in the accepted manuscript were produced from frozen, hash-verified WN18RR artifacts (exports,
candidate manifests, leakage audits, and the primary-number ledger) recorded in the submission's orchestration
record. This repository implements the framework, but a generic checkout is **not claimed** to reproduce every
reported number; exact reproduction requires the frozen protocol, recorded training and candidate seeds, and the
corresponding verified artifacts.

## Citation

```
@article{xiao2026reliable,
  title={Reliable Knowledge Discovery in Knowledge Graphs: A Statistical Quality Assurance Framework for Link Prediction},
  author={Xiao, Zhiren},
  journal={Expert Systems with Applications},
  year={2026}
}
```

## Contact

Zhiren Xiao — 241734106@m.gduf.edu.cn — Guangdong University of Finance, Guangzhou, China
