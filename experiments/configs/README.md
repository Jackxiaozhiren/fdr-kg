# FDR-KG: Model and FDR Configuration

## Benchmark Datasets
- WN18RR (Dettmers et al., 2018): 40,943 entities, 11 relations, 2,924 test triples
- FB15k-237 (Toutanova et al., 2015): 14,541 entities, 237 relations, 20,438 test triples

## KG Embedding Models
### TransE (Bordes et al., 2013)
- Embedding dimension: 256
- Scoring function: L2 negative distance
- Learning rate: 0.001, Batch size: 256, Epochs: 20

### RotatE (Sun et al., 2019)
- Embedding dimension: 256
- Scoring function: rotation-based distance
- Learning rate: 0.001, Batch size: 256, Epochs: 20
- Phase embedding: 128 (half of total dimension)

### ComplEx (Trouillon et al., 2016)
- Embedding dimension: 256
- Scoring function: complex bilinear product
- Learning rate: 0.001, Batch size: 256, Epochs: 20

### ConvE (Dettmers et al., 2018)
- Embedding dimension: 256
- Scoring function: 2D convolutional
- Learning rate: 0.001, Batch size: 256, Epochs: 20

## FDR Pipeline Configuration
- Negative samples per test triple (K): 100 (default)
- Filtered setting: exclude known true tails
- Storey pi0 estimation: cubic spline over lambda in [0.1, 0.9]
- Local FDR: Gaussian KDE, Silverman's rule bandwidth
- Multi-seed stability: seeds {42, 123, 456}

## Hardware
- Apple M1, 16GB RAM
- WN18RR: ~3-5 min per model
- FB15k-237: ~25-35 min per model
