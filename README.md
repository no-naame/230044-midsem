# 230044 — Mid-Semester Examination

**Student**: Meghavi (Roll: 230044)
**Course**: Advanced Machine Learning
**Paper**: [Weisfeiler-Lehman Graph Kernels](https://jmlr.org/papers/v12/shervashidze11a.html) — Shervashidze, Schweitzer, van Leeuwen, Mehlhorn, Borgwardt (JMLR 2011)

---

## What This Project Does

This project reproduces the **Weisfeiler-Lehman (WL) subtree kernel** for graph classification, as described in the paper. The WL kernel works by:

1. Iteratively relabeling graph nodes by aggregating sorted neighbor labels
2. Compressing augmented labels via hashing (dictionary lookup)
3. Building feature vectors as histograms of all labels across iterations
4. Computing the kernel as a dot product of feature vectors
5. Classifying graphs with SVM using the precomputed kernel matrix

We validated the implementation on:
- A **synthetic dataset** (200 graphs: trees vs. cyclic) — **88.00% accuracy**
- The **real MUTAG dataset** from the paper (188 molecular graphs) — **81.99% accuracy** at h=3, matching the paper's reported **82.05%** to within 0.06 percentage points

## Results Summary

| Experiment | Accuracy | Paper |
|---|---|---|
| Synthetic dataset (h=3) | 88.00% (+/- 5.57%) | N/A |
| MUTAG dataset (h=3) | **81.99%** | **82.05%** (+/- 0.36%) |
| Ablation: h=0 (no iterations) | 81.00% | — |
| Ablation: no label prefix | 86.00% | — |
| Failure: regular graphs, uniform labels | 50.00% (random) | — |

---

## Repository Structure

```
230044-midsem/
├── README.md                      # This file
├── .gitignore
├── llm_usage_partA.json           # Part A LLM disclosure
│
└── partB/
    ├── requirements.txt           # Python dependencies (pip install -r)
    ├── report.pdf                 # 2-page summary report
    ├── generate_report.py         # Script to regenerate report.pdf
    │
    ├── task_1_1.ipynb             # Q1: Core contribution (markdown)
    ├── task_1_2.ipynb             # Q1: Key assumptions (markdown)
    ├── task_1_3.ipynb             # Q1: Baseline comparison (markdown)
    │
    ├── task_2_1.ipynb             # Q2: Synthetic dataset generation
    ├── task_2_2.ipynb             # Q2: WL kernel implementation
    ├── task_2_3.ipynb             # Q2: Results & reproducibility
    ├── task_2_4_mutag.ipynb       # Q2: Validation on real MUTAG dataset
    │
    ├── task_3_1.ipynb             # Q3: Two-component ablation study
    ├── task_3_2.ipynb             # Q3: Failure mode analysis
    │
    ├── llm_task_*.json            # 10 LLM disclosure files
    │
    ├── data/
    │   ├── README.md              # Dataset documentation
    │   ├── synthetic_dataset.pkl  # Generated synthetic dataset
    │   └── MUTAG/                 # Real MUTAG dataset (TUDataset format)
    │       ├── MUTAG_A.txt
    │       ├── MUTAG_graph_indicator.txt
    │       ├── MUTAG_graph_labels.txt
    │       ├── MUTAG_node_labels.txt
    │       ├── MUTAG_edge_labels.txt
    │       └── README.txt
    │
    └── results/                   # All generated plots
        ├── dataset_examples.png
        ├── confusion_matrix.png
        ├── accuracy_comparison.png
        ├── ablation_comparison.png
        ├── failure_mode_examples.png
        ├── failure_mode_heatmap.png
        ├── mutag_accuracy_vs_h.png
        ├── mutag_confusion_matrix.png
        └── full_comparison.png
```

## How to Run

### Prerequisites

- Python 3.10+ (tested on 3.14)
- No GPU required — everything runs on CPU

### Setup

```bash
# Clone the repository
git clone https://github.com/no-naame/230044-midsem.git
cd 230044-midsem

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r partB/requirements.txt

# Install Jupyter kernel
python -m ipykernel install --user --name=wl-kernel --display-name "WL Kernel"
```

### Run All Notebooks

Notebooks must be run **in order** since later ones depend on outputs from earlier ones:

```bash
cd partB

# Step 1: Generate synthetic dataset
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=wl-kernel task_2_1.ipynb --output task_2_1.ipynb

# Step 2: Run WL kernel on synthetic data
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=wl-kernel task_2_2.ipynb --output task_2_2.ipynb

# Step 3: Results analysis
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=wl-kernel task_2_3.ipynb --output task_2_3.ipynb

# Step 4: Validate on real MUTAG dataset
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=wl-kernel task_2_4_mutag.ipynb --output task_2_4_mutag.ipynb

# Step 5: Ablation study (depends on synthetic dataset from step 1)
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=wl-kernel task_3_1.ipynb --output task_3_1.ipynb

# Step 6: Failure mode (depends on WL results from step 2)
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=wl-kernel task_3_2.ipynb --output task_3_2.ipynb

# Step 7: Regenerate report
python generate_report.py
```

Or open the notebooks interactively in Jupyter:

```bash
jupyter notebook
```

### MUTAG Dataset

The MUTAG dataset (120KB) is included in `partB/data/MUTAG/`. It was downloaded from [TUDataset](https://chrsmrrs.github.io/datasets/). If you need to re-download:

```bash
cd partB/data
curl -L -o MUTAG.zip "https://www.chrsmrrs.com/graphkerneldatasets/MUTAG.zip"
unzip MUTAG.zip
```

---

## What Was Implemented from the Paper

| Paper Component | Status | Notes |
|---|---|---|
| Algorithm 1 (WL relabeling, 4 steps) | Implemented | Multiset collection, sorting, prefix, compression, relabeling |
| Algorithm 2 (hash function for N graphs) | Implemented | Dictionary-based label compression |
| Definition 4 / Eq. 2 (WL subtree kernel) | Implemented | Feature vector = histogram of labels across all iterations |
| Kernel = dot product (Eq. 2) | Implemented | K = X @ X.T |
| C-SVM classification (Sec 4.2.2) | Implemented | sklearn SVC(kernel='precomputed'), 10-fold CV |
| Nested CV for C selection (Sec 4.2.2) | Implemented | Inner 5-fold CV, C from {10^-3, ..., 10^3} |
| MUTAG evaluation (Table 1) | Reproduced | 81.99% vs paper's 82.05% |
| Ablation: h=0 | Tested | 7pp accuracy drop confirms iteration importance |
| Ablation: no label prefix | Tested | 2pp drop confirms prefix contribution |
| Failure mode: regular graphs | Demonstrated | 50% accuracy, identical feature vectors |

### What Was NOT Implemented

- WL edge kernel (Section 3.3)
- WL shortest path kernel (Section 3.4)
- Evaluation on NCI1, NCI109, ENZYMES, D&D datasets
- 10x repeated CV protocol (we use single 10-fold CV)
- Runtime benchmarking (Section 4.1)

---

## LLM Usage

This project was a **collaborative effort** between the student (Meghavi, 230044) and Claude (claude-opus-4-6) via Claude Code CLI. All LLM interactions are documented in `partB/llm_task_*.json` (10 files, one per task). The student provided the research direction, paper understanding, and design decisions. Claude assisted with code generation, structuring, and articulation.

## References

- Shervashidze, N., Schweitzer, P., van Leeuwen, E.J., Mehlhorn, K., Borgwardt, K.M. (2011). Weisfeiler-Lehman Graph Kernels. *Journal of Machine Learning Research*, 12, 2539-2561.
- Debnath, A.K. et al. (1991). Structure-activity relationship of mutagenic aromatic and heteroaromatic nitro compounds. *J. Med. Chem.*, 34(2):786-797.
