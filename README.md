# FDR-KG: Statistical Quality Assurance for Knowledge Graph Link Prediction

> **Project status — historical precursor.** This repository preserves an earlier methodological and manuscript-development route for statistical quality assurance in knowledge-graph link prediction. It is **not** the frozen evidence repository for the current Journal of Biomedical Informatics manuscript. The manuscript-active JBI code, frozen protocol, derived results, and versioned release are maintained at [`Jackxiaozhiren/jbi-biomedical-reliability-screen`](https://github.com/Jackxiaozhiren/jbi-biomedical-reliability-screen), specifically release `v1.0.1` for the final audited submission state.

The earlier working manuscript associated with this repository used the title:

> **Reliable Knowledge Discovery in Knowledge Graphs: A Statistical Quality Assurance Framework for Link Prediction**
> Zhiren Xiao

That route preceded the later biomedical, externally validated JBI formulation. Historical public experiment outputs remain here for provenance and method development; they must not be cited as the frozen evidence for the JBI paper. See [`docs/PROJECT_LINEAGE.md`](docs/PROJECT_LINEAGE.md).

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
- `docs/PROJECT_LINEAGE.md` — relationship to the later JBI-specific research route;
- `docs/REPRODUCIBILITY.md` — reproducibility boundary and verification guidance;
- `docs/DATA_AVAILABILITY.md` — data and artifact availability statement.

## Evidence boundary

The public files currently under `experiments/results/` are retained outputs from an earlier public experiment state. They are **not designated as frozen evidence for the current JBI manuscript** and should not be used to infer its headline values.

For the final JBI manuscript, use the dedicated repository and versioned release:

- repository: `Jackxiaozhiren/jbi-biomedical-reliability-screen`
- release: `v1.0.1`
- manuscript route: *From ranked links to audited decisions: an externally validated reliability screen for knowledge-graph-based drug repurposing*

The JBI repository contains the frozen protocol, manuscript-facing derived result exports, compact external-validation summaries, generated figures, and release checksum manifest. This repository remains useful as a historical software/method-development record rather than as the archival JBI evidence package.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m compileall fdr_kg
```

For exploratory execution of the historical/public pipeline:

```bash
python experiments/run_pipeline.py --help
```

Do not treat a newly generated run as manuscript-identical unless the same dataset snapshot, model artifacts, seeds, candidate-generation protocol, package versions, and configuration are explicitly frozen and verified.

## Reproducibility policy

A manuscript reproduction release should satisfy all of the following before its DOI is cited in a paper:

1. freeze the exact manuscript configuration and random seeds;
2. include or legally reference every required input artifact;
3. record cryptographic checksums for all frozen inputs and derived headline outputs;
4. record the exact Python/package environment used for the manuscript run;
5. provide one command or documented sequence that regenerates manuscript tables/figures from the frozen artifacts;
6. verify that regenerated headline values match the manuscript before tagging the release.

The later JBI-specific repository applies this stricter release boundary; this historical repository does not retroactively claim that its legacy outputs satisfy the JBI frozen-evidence standard.

## Citation

Use GitHub's **Cite this repository** metadata from `CITATION.cff` only when citing the FDR-KG software itself. For the current JBI study or its numerical results, cite the JBI article and the `jbi-biomedical-reliability-screen` versioned release instead.

## License

MIT. Third-party datasets, pretrained models, APIs, and other external assets remain subject to their original licenses and terms.

## Contact

Zhiren Xiao — 241734106@m.gduf.edu.cn — Guangdong University of Finance, Guangzhou, China
