# Reproducibility

## Current public repository boundary

The current checkout contains the FDR-KG implementation and legacy/public benchmark outputs. The files in `experiments/results/` predate the current frozen manuscript evidence and therefore must not be described as manuscript-identical results.

## Requirements for the manuscript archival release

Before creating the manuscript DOI release, freeze and publish (where redistribution is permitted):

- exact commit SHA;
- Python version and operating-system information;
- exact package versions from the environment used for the manuscript run;
- dataset identifiers/version or download instructions;
- model/checkpoint identifiers and hashes where distributable;
- training, evaluation, and candidate-sampling seeds;
- candidate-generation and filtering configuration;
- primary result ledger used by the manuscript;
- SHA-256 checksums for all frozen inputs and derived headline outputs;
- scripts that regenerate manuscript tables and figures from the frozen evidence.

If an input cannot be redistributed, document its provider, identifier/version, acquisition procedure, expected checksum when legally permissible, and the exact transformation required before running the analysis.

## Verification rule

A release should be tagged as the manuscript reproducibility release only after regenerated headline statistics and manuscript tables/figures have been compared with the submitted manuscript. Any mismatch should block the release until reconciled.

## Environment locking

`requirements.txt` is currently a compatibility specification, not an exact historical lock file. Do not create a purported manuscript lock file by guessing versions. Export the exact environment from the machine/container used for the frozen manuscript run and commit that file with the archival release.
