# Dataset Documentation

## 1. Synthetic Labeled Graph Classification Dataset

**File**: `synthetic_dataset.pkl`

**Purpose**: Controlled toy dataset to test the WL subtree kernel on a graph classification task with known structural differences.

### Description

| Property | Value |
|----------|-------|
| Total graphs | 200 (100 per class) |
| Node count range | 6 to 15 |
| Node label alphabet | {0, 1, 2} |
| Random seed | 42 |

- **Class 0 ("Tree-like")**: Random trees via `nx.random_labeled_tree()`. Labels biased toward 0 (p=[0.5, 0.3, 0.2]).
- **Class 1 ("Cyclic")**: Cycle core + tree branches via `nx.cycle_graph()` + random attachment. Labels biased toward 1 (p=[0.2, 0.5, 0.3]).

### Format (pickle)

```python
{
    'graphs': [
        {
            'adj_list': [(u, v), ...],      # undirected edges
            'node_labels': {node_id: label}, # int labels
            'n_nodes': int,
            'n_edges': int
        },
        ...
    ],
    'labels': np.array([0, 0, ..., 1, 1, ...])  # class labels
}
```

### Results

WL subtree kernel (h=3) + SVM: **88.00% (+/- 5.57%)** 10-fold CV accuracy.

---

## 2. MUTAG — Real Molecular Dataset from the Paper

**Directory**: `MUTAG/`

**Source**: [TUDataset](https://chrsmrrs.github.io/datasets/) — originally from Debnath et al. (1991)

**Reference**: Debnath, A.K., Lopez de Compadre, R.L., Debnath, G., Shusterman, A.J., and Hansch, C. Structure-activity relationship of mutagenic aromatic and heteroaromatic nitro compounds. J. Med. Chem. 34(2):786-797 (1991).

### Description

| Property | Value |
|----------|-------|
| Total graphs | 188 |
| Avg nodes | 17.93 |
| Avg edges | 19.79 |
| Node labels | 7 (C, N, O, F, I, Cl, Br) |
| Classes | 2 (mutagenic / non-mutagenic) |
| Class split | 125 mutagenic, 63 non-mutagenic |

Molecules are represented as graphs: atoms = nodes, bonds = edges. The task is to predict whether a compound has mutagenic effect on the bacterium *Salmonella typhimurium*.

### TUDataset Format

| File | Description |
|------|-------------|
| `MUTAG_A.txt` | Edge list (row, col), 1-indexed |
| `MUTAG_graph_indicator.txt` | Maps each node to its graph ID |
| `MUTAG_graph_labels.txt` | +1 (mutagenic) or -1 (non-mutagenic) |
| `MUTAG_node_labels.txt` | Atom type: 0=C, 1=N, 2=O, 3=F, 4=I, 5=Cl, 6=Br |
| `MUTAG_edge_labels.txt` | Bond type: 0=aromatic, 1=single, 2=double, 3=triple |

### Results

WL subtree kernel (h=3) + SVM: **81.99%** — matches the paper's reported **82.05%** to within 0.06pp.

| h | Accuracy | Features |
|---|----------|----------|
| 0 | 84.62% | 7 |
| 1 | 86.67% | 40 |
| 2 | 83.51% | 214 |
| 3 | 81.99% | 786 |
| 4 | 82.98% | 1983 |
| 5 | 82.95% | 3749 |
