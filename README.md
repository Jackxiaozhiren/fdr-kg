# FDR-KG

This repository contains the complete source code, configuration, and analysis scripts for:

> **FDR-Controlled Knowledge Graph Completion: Statistical Inference for Reliable Link Prediction**  
> Zhiren Xiao  
> *Submitted to Knowledge-Based Systems (Elsevier)*

## Overview

The FDR-KG framework reformulates knowledge graph (KG) link prediction evaluation as a large-scale multiple hypothesis testing problem. It constructs empirical p-values from embedding scores via permutation-based negative sampling, then applies Benjamini-Hochberg FDR control, Storey's q-value estimation, and Efron's local FDR to produce per-triple, per-relation, and per-model reliability profiles.

**Key findings:**
- 26–85% of test triples are statistically indistinguishable from noise
- Per-relation FDR rejection rates span 9.1%–96.5%, exposing extreme heterogeneity invisible to MRR
- MRR and FDR produce conflicting model rankings across both WN18RR and FB15k-237

## Repository Structure

- `fdr_kg/` — Core Python package (p-value computation, FDR methods, pipeline)
- `experiments/` — Run scripts, model configurations, and results
- `analysis/` — Scripts to reproduce all tables and figures from the paper
- `paper/` — LaTeX source files for the manuscript
- `submission_package/` — Complete KBS submission materials

## Quick Start

```bash
pip install -r requirements.txt
python experiments/run_pipeline.py --dataset WN18RR
```

## Reproducibility

All experiments use seed 42. Running with the provided code and seed reproduces the exact results in the paper. Multi-seed stability analysis (seeds 42, 123, 456) confirms coefficient of variation < 2% for all FDR metrics.

## Citation

```
@article{xiao2026fdr,
  title={FDR-Controlled Knowledge Graph Completion: Statistical Inference for Reliable Link Prediction},
  author={Xiao, Zhiren},
  journal={Knowledge-Based Systems},
  year={2026}
}
```

## Contact

Zhiren Xiao — 241734106@m.gduf.edu.cn — Guangdong University of Finance
