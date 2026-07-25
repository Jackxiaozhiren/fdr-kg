"""
FDR-KG: False Discovery Rate Control for Knowledge Graph Completion.

Core package implementing the three-level evaluation protocol:
1. Per-triple: empirical p-values + local FDR
2. Per-relation: stratified FDR analysis
3. Per-model: global FDR metrics + model ranking
"""

__version__ = "1.0.0"
