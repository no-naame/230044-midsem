# Dataset Documentation

## Synthetic Labeled Graph Classification Dataset

**Purpose**: Reproduce the WL subtree kernel graph classification setting from Shervashidze et al. (JMLR 2011) on a controlled toy dataset.

### Dataset Description

- **Total graphs**: 200 (100 per class)
- **Node count range**: 6 to 15 nodes per graph
- **Node label alphabet**: {0, 1, 2}
- **Random seed**: 42

### Class Definitions

| Class | Structure | Label Distribution | Generator |
|-------|-----------|-------------------|-----------|
| 0 ("Tree-like") | Random trees (acyclic) | Biased toward label 0: p=[0.5, 0.3, 0.2] | `nx.random_tree()` |
| 1 ("Cyclic") | Cycle core + tree branches | Biased toward label 1: p=[0.2, 0.5, 0.3] | `nx.cycle_graph()` + random edges |

### Format

Each graph is stored as:
- **Adjacency list**: List of (source, target) edges
- **Node labels**: Dictionary mapping node index to label

### Justification

This mimics the molecular graph classification setting (e.g., MUTAG dataset) where structural differences (tree-like vs. cyclic) and label patterns distinguish classes. The WL kernel should capture these differences through iterative neighborhood label aggregation.

### Limitations vs. Paper's Datasets

- Fewer nodes per graph (6-15 vs. 17-39 in MUTAG)
- Fewer label types (3 vs. 7 atom types in MUTAG)
- No real chemical meaning
- Clearer class separation (structural difference is more pronounced)
