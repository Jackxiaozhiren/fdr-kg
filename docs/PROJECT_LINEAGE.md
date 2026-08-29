# Project lineage: FDR-KG to the JBI-specific reliability screen

## Status

`fdr-kg` is preserved as an earlier method-development and manuscript-route repository for false-discovery-rate diagnostics in knowledge-graph link prediction. It predates the dedicated JBI reproducibility repository and is not the frozen evidence source for the final JBI submission.

## Historical route

The earlier route used the working manuscript title:

> *Reliable Knowledge Discovery in Knowledge Graphs: A Statistical Quality Assurance Framework for Link Prediction*

The local research history later moved through KBS/ESWA-oriented development and then converged on a biomedical, externally validated reliability-screen formulation for the Journal of Biomedical Informatics.

## Current manuscript-active route

The final JBI manuscript is:

> *From ranked links to audited decisions: an externally validated reliability screen for knowledge-graph-based drug repurposing*

Its public reproducibility repository is:

- https://github.com/Jackxiaozhiren/jbi-biomedical-reliability-screen
- final audited release line: `v1.0.1`

That repository contains the JBI-specific frozen protocol, derived manuscript result exports, compact external-validation summaries, figures, citation metadata, and release checksum manifest.

## Evidence rule

Do **not** use `fdr-kg/experiments/results/` to reconstruct or cite headline values from the JBI manuscript. Those files are retained historical/public benchmark outputs from an earlier experiment state.

Use `fdr-kg` when the object of citation is the historical software or method-development record itself. Use the dedicated JBI repository/release when the object of citation is the JBI study, its final numerical results, external validation, or manuscript-facing reproducibility package.

## Why both repositories remain public

Keeping both repositories preserves research provenance without rewriting history:

- `fdr-kg` documents the earlier statistical-quality-assurance route and exploratory public implementation;
- `jbi-biomedical-reliability-screen` documents the later manuscript-active biomedical reliability audit under a stricter frozen-evidence boundary.

The two repositories should therefore be read as successive stages of one research lineage, not as two independent final-paper evidence packages.
