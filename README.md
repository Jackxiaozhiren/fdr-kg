# FDR-KG: Statistical Quality Assurance for Knowledge Graph Link Prediction

This repository contains the complete source code, configuration, and analysis scripts for:

> **Reliable Knowledge Discovery in Knowledge Graphs: A Statistical Quality Assurance Framework for Link Prediction**  
> Zhiren Xiao  
> *Submitted to Knowledge-Based Systems (Elsevier)*

## Overview

The FDR-KG framework reformulates knowledge graph (KG) link prediction evaluation as a large-scale multiple hypothesis testing problem, providing statistical quality assurance for knowledge-based systems that consume KG completion output. It constructs empirical p-values from embedding scores via permutation-based negative sampling, then applies Benjamini-Hochberg FDR control, Storey's q-value estimation, and Efron's local FDR in concert to produce per-triple, per-relation, and per-model reliability profiles.

**Key findings:**
- 26–85% of test triples are statistically indistinguishable from noise across models and benchmarks (estimated null proportion π̂₀ = 0.259 to 0.851)
- Per-relation discovery rates span from below 10% to above 95% under a single model, exposing extreme heterogeneity in prediction reliability
- Model rankings by MRR and by FDR power capture distinct dimensions of quality: RotatE leads on MRR while TransE leads on statistically significant discoveries

## Repository Structure

- `fdr_kg/` — Core Python package (p-value computation, FDR methods, pipeline)
- `experiments/` — Run scripts, model configurations, and results
- `analysis/` — Scripts to reproduce all tables and figures from the paper
- `paper/` — LaTeX source files for the manuscript
- `submission_package/` — Complete KBS submission materials (v2, 2026-07-26)

## Quick Start

```bash
pip install -r requirements.txt
python experiments/run_pipeline.py --dataset WN18RR --model TransE
```

## Reproducibility

All main experiments use seed 42. Multi-seed stability analysis (seeds 42, 123, 456 across TransE, RotatE, ConvE) confirms coefficient of variation < 2% for BH rejection rate and < 6% for π̂₀, indicating that single-seed FDR comparisons are reliable.

All models are trained with 20 epochs (embedding dimension d=256, learning rate 0.001, batch size 256) using the PyKEEN framework on a standard CPU (Apple M1, 16GB RAM). The full FDR pipeline completes in 3–35 minutes per model depending on dataset size.

## Citation

```
@article{xiao2026reliable,
  title={Reliable Knowledge Discovery in Knowledge Graphs: A Statistical Quality Assurance Framework for Link Prediction},
  author={Xiao, Zhiren},
  journal={Knowledge-Based Systems},
  year={2026}
}
```

## Contact

Zhiren Xiao — 241734106@m.gduf.edu.cn — Guangdong University of Finance, Guangzhou, China
