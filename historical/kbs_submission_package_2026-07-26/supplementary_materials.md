# FDR-KG: Supplementary Materials

## Code Availability

The complete source code and analysis scripts for all experiments are available at:
https://github.com/Jackxiaozhiren/fdr-kg

The repository includes trained model checkpoints, per-relation FDR statistics, and scripts for reproducing all figures and tables.

## Data Availability

WN18RR and FB15k-237 are publicly available benchmarks. The specific train/validation/test splits used are the standard splits provided with the datasets. WN18RR is distributed by Dettmers et al. (2018); FB15k-237 is distributed by Toutanova et al. (2015).

## Reproducibility

All experiments were conducted using Python 3.9 with PyKEEN 1.10.1, NumPy, and SciPy.

**Model configuration:**
- Embedding dimension: $d = 256$
- Learning rate: $0.001$
- Batch size: $256$
- Training epochs: $20$
- Random seed: $42$ (all models)

**FDR pipeline configuration:**
- Negative samples per test triple: $K = 100$
- Filtered setting: excluding all known true tails from training, validation, and test sets
- Storey $\pi_0$ estimation: cubic spline extrapolation over $\lambda \in \{0.1, \dots, 0.9\}$
- Local FDR: Gaussian KDE with bandwidth selected via Silverman's rule of thumb
- Hardware: Apple M1, 16GB RAM

**Runtime:**
- WN18RR (2,924 test triples): approximately 3--5 minutes per model
- FB15k-237 (20,438 test triples): approximately 25--35 minutes per model

## Extended Results

The following results are available in the code repository:
1. Full per-relation FDR statistics for all four models on WN18RR (TransE, RotatE, ComplEx, ConvE)
2. FB15k-237 per-relation FDR statistics (all 237 relations)
3. BH rejection counts at all FDR levels ($\alpha = 0.01, 0.05, 0.10, 0.20$)
4. Local FDR values for all individual test triples on both datasets
5. Sensitivity analysis results for additional $K$ and $\lambda$ values
6. $q$-value distributions for all models
7. Complete score files (positive and negative) for all 4 models on WN18RR

## WN18RR Test Triple Exclusion

The WN18RR dataset contains 3,134 test triples. We retain 2,924 triples for FDR analysis. The excluded 210 triples (6.7%) involve head-relation pairs where fewer than 100 valid negative tail entities exist under the filtered setting, because nearly all candidate tail entities are known positives. This near-exhaustive positive coverage makes negative sampling infeasible and $p$-value construction unreliable. Following the standard filtered setting convention, these triples are excluded from the FDR pipeline; their exclusion does not affect comparative conclusions drawn across models, since all models are evaluated on the identical set of 2,924 triples.

## FB15k-237 Per-Relation FDR Statistics

The complete per-relation FDR statistics for all 237 FB15k-237 relations under TransE, RotatE, ComplEx, and ConvE are available in the GitHub repository (`experiments/results/fb15k237/per_relation_fdr_full.csv`). Key aggregate findings (summarized in §4.6 of the main text):

- **Raw $p < 0.05$ rate range:** 0.8%--84.3% across 237 relations (TransE: 0.8%--72.1%; RotatE: 1.2%--84.3%)
- **Knowledge-blind relations:** 31 relations (13.1%) with near-zero raw $p < 0.05$ rates (<5%) under both TransE and RotatE
- **Highly reliable relations:** 47 relations (19.8%) with >50% raw $p < 0.05$ rates under both models
- **Cross-model Spearman $\rho$:** >0.85 (relation difficulty is largely a property of the relation type rather than the model architecture)

A supplementary figure visualizing the per-relation reliability distribution across all 237 FB15k-237 relations is provided as `figures/fb15k237_per_relation_distribution.pdf`.

## Multi-Seed FDR Stability Analysis

To assess the stability of FDR metrics across random initializations, we retrained TransE and ConvE under three random seeds each ($\{42, 123, 456\}$, 20 epochs, $K=100$). Both models exhibit highly stable FDR metrics across seeds (coefficient of variation < 2% for $\hat{\pi}_0$, BH rejection rate, and MRR). Complete per-seed results and score files are available in the GitHub repository. See the main text (§4.7, Limitations) for a summary of these findings.

## Per-Relation Sample Size Cautions

For WN18RR per-relation analysis (Table 2), three relations have small sample sizes: Relation 6 ($n = 26$), Relation 7 ($n = 22$), and Relation 8 ($n = 3$). FDR rejection rates for these relations should be interpreted cautiously. Relation 8 ($n = 3$, both models achieve 100% rejection) is included for completeness but is too small for reliable statistical inference.
