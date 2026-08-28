# FDR-KG: Statistical Quality Assurance for Knowledge Graph Link Prediction

Companion software and reproducibility materials for:

> **Reliable Knowledge Discovery in Knowledge Graphs: A Statistical Quality Assurance Framework for Link Prediction**
> Zhiren Xiao

## Overview

FDR-KG is a statistical quality-assurance framework for knowledge-graph link prediction. For each retained test triple, it samples filtered tail corruptions, compares the observed model score with the sampled score distribution, constructs an empirical p-value under the declared candidate-sampling scheme, and applies false-discovery-rate procedures as conditional benchmark diagnostics.

These diagnostics characterize model-score behavior under the stated evaluation protocol. They do not establish factual truth in a complete knowledge graph, causal validity, clinical validity, or deployment guarantees.

## What this repository contains

- `fdr_kg/` — core Python implementation;
- `experiments/` — experiment drivers and legacy/public benchmark outputs;
- `analysis/` — utilities for inspecting released outputs;
- `requirements.txt` — install requirements;
- `LICENSE` — MIT license;
- `CITATION.cff` — software citation metadata;
- `docs/REPRODUCIBILITY.md` — reproducibility boundary and verification guidance;
- `docs/DATA_AVAILABILITY.md` — data and artifact availability statement.

## Important evidence boundary

The public files currently under `experiments/results/` are retained benchmark outputs from an earlier public experiment state. They are **not designated as the frozen evidence package for the current manuscript** and should not be used to infer the manuscript's headline values unless a versioned release explicitly identifies them as such.

The manuscript-facing evidence was generated under a separately frozen, hash-verified protocol. Before archival release, the exact manuscript artifact set should be deposited as a versioned release with checksums and a persistent DOI. See `docs/REPRODUCIBILITY.md`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m compileall fdr_kg
```

For exploratory execution of the public pipeline:

```bash
python experiments/run_pipeline.py --help
```

Do not treat a newly generated run as manuscript-identical unless the same dataset snapshot, model artifacts, seeds, candidate-generation protocol, package versions, and configuration recorded for the manuscript are used.

## Reproducibility policy

A manuscript reproduction release should satisfy all of the following before its DOI is cited in the paper:

1. freeze the exact manuscript configuration and random seeds;
2. include or legally reference every required input artifact;
3. record cryptographic checksums for all frozen inputs and derived headline outputs;
4. record the exact Python/package environment used for the manuscript run;
5. provide one command or documented sequence that regenerates manuscript tables/figures from the frozen artifacts;
6. verify that regenerated headline values match the manuscript before tagging the release.

## Citation

Use GitHub's **Cite this repository** function, generated from `CITATION.cff`, when citing the software repository. After the associated article is formally published, `CITATION.cff` can be updated with a `preferred-citation` entry for the article.

## License

MIT. Third-party datasets, pretrained models, APIs, and other external assets remain subject to their original licenses and terms.

## Contact

Zhiren Xiao — 241734106@m.gduf.edu.cn — Guangdong University of Finance, Guangzhou, China
