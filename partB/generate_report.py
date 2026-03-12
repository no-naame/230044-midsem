"""Generate report.pdf for Part B using fpdf2."""

import os
from fpdf import FPDF

class Report(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'Part B Report: Weisfeiler-Lehman Graph Kernels', new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, 'Meghavi (Roll: 230044)', new_x="LMARGIN", new_y="NEXT", align='C')
        self.cell(0, 6, 'Paper: Shervashidze, Schweitzer, van Leeuwen, Mehlhorn, Borgwardt (JMLR 2011)', new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5, text)
        self.ln(2)


def main():
    pdf = Report()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Section 1: Paper Summary
    pdf.section_title('1. Paper Summary')
    pdf.body_text(
        'The paper "Weisfeiler-Lehman Graph Kernels" by Shervashidze et al. (JMLR 2011) proposes a family of '
        'efficient graph kernels based on the Weisfeiler-Lehman (WL) test of graph isomorphism. The core method, '
        'the WL subtree kernel, works by iteratively relabeling nodes: at each iteration, a node\'s label is '
        'updated by aggregating and compressing the sorted multiset of its neighbors\' labels. After h iterations, '
        'a graph\'s feature vector is the histogram of all labels across all iterations. The kernel between two '
        'graphs is the dot product of their feature vectors. This achieves O(hm) runtime per graph (linear in '
        'edges), making it dramatically faster than prior graph kernels with O(n^3) or worse complexity, while '
        'achieving state-of-the-art classification accuracy on benchmark molecular and bioinformatics datasets.'
    )

    # Section 2: Reproduction
    pdf.section_title('2. Reproduction Setup and Results')
    pdf.body_text(
        'Dataset: We generated a synthetic labeled graph classification dataset with 200 graphs (100 per class). '
        'Class 0 consists of random trees (acyclic graphs) with node labels biased toward label 0 (p=[0.5, 0.3, 0.2]). '
        'Class 1 consists of cyclic graphs (cycle core with tree branches) with labels biased toward label 1 '
        '(p=[0.2, 0.5, 0.3]). Nodes range from 6 to 15, with labels from {0, 1, 2}. This mimics the molecular '
        'classification setting of the paper (e.g., MUTAG dataset) where structural and label differences '
        'distinguish graph classes.'
    )
    pdf.body_text(
        'Implementation: We implemented the WL subtree kernel following Algorithm 1 and Definition 4 of the paper. '
        'The implementation uses dictionary-based label compression (hash), constructs feature vectors as label '
        'histograms, and computes the kernel matrix as a dot product. Classification uses SVM with precomputed '
        'kernel (sklearn SVC) and 10-fold stratified cross-validation, with C selected via nested 5-fold CV '
        'from {10^-3, ..., 10^3}. Random seed: 42.'
    )
    pdf.body_text(
        'Results: Our WL subtree kernel (h=3) achieves high classification accuracy on the synthetic dataset. '
        'The paper reports 82.05% (+/- 1.36%) on MUTAG (Table 1). Our higher accuracy is expected because the '
        'synthetic dataset has clearer class separation (tree vs. cyclic structure) and different label distributions '
        'between classes, providing stronger signal than real molecular mutagenicity.'
    )

    # Section 3: Ablation
    pdf.section_title('3. Ablation Study Findings')
    pdf.body_text(
        'Ablation 1 - Remove WL Iterations (h=0): Setting h=0 removes all iterative relabeling, reducing the '
        'feature vector to a histogram of original node labels only. No topological information is captured. '
        'This caused a significant accuracy drop, confirming that the iterative neighborhood aggregation is the '
        'essential contribution of the WL kernel. Without it, the kernel relies solely on label frequency '
        'differences between classes, which provides limited discriminative power. '
        '(Paper reference: Definition 4, Equation 2 -- the sum over iterations is reduced to just i=0.)'
    )
    pdf.body_text(
        'Ablation 2 - Remove Label Prefix: In Algorithm 1 Step 2, the node\'s own label l_{i-1}(v) is prepended '
        'to the sorted neighbor label string before compression. Removing this prefix means nodes with different '
        'labels but identical neighborhoods receive the same compressed label, losing node identity information. '
        'This caused a moderate accuracy drop, confirming that preserving node identity during relabeling improves '
        'the kernel\'s discriminative power. '
        '(Paper reference: Algorithm 1, Step 2 -- "Add l_{i-1}(v) as a prefix to s_i(v).")'
    )

    # Section 4: Failure Mode
    pdf.section_title('4. Failure Mode')
    pdf.body_text(
        'Scenario: We constructed 3-regular graphs on 8 nodes where ALL nodes have the same label (0). '
        'In this setting, the WL kernel completely fails to distinguish structurally different graphs.'
    )
    pdf.body_text(
        'Explanation: In a k-regular graph with uniform labels, every node has the same degree and the same '
        'label. After WL iteration 1, every node aggregates the same multiset of neighbor labels (k copies of '
        'the same label), producing the same compressed label for ALL nodes. This pattern repeats in all '
        'subsequent iterations. Therefore, all graphs of the same size and degree produce identical feature '
        'vectors, making classification impossible (accuracy ~ 50%, equivalent to random guessing).'
    )
    pdf.body_text(
        'Connection to Assumptions: This directly demonstrates Assumption 3 from Task 1.2 -- the limitation of '
        'the 1-dimensional WL test. The paper references Cai, Furer, and Immerman (1992) who proved that there '
        'exist non-isomorphic graphs indistinguishable by the 1-dim WL test. Our regular graphs are a concrete '
        'example. Suggested fixes include using higher-dimensional WL tests (k-WL for k > 1), augmenting with '
        'spectral features, or using continuous message-passing (Graph Neural Networks).'
    )

    # Section 5: Reflection
    pdf.section_title('5. Reflection')
    pdf.body_text(
        'What was surprising: The dramatic accuracy drop when removing WL iterations (h=0) was stark -- it '
        'highlights how much the iterative relabeling contributes beyond simple label statistics. Also, the '
        'failure mode on regular graphs is theoretically clean: the kernel literally produces identical feature '
        'vectors for all same-size regular graphs, not just similar ones.'
    )
    pdf.body_text(
        'What I would revisit with more time: (1) Test on a real-world dataset like MUTAG to directly compare '
        'numbers with the paper. (2) Implement the WL edge kernel or WL shortest-path kernel from the paper to '
        'compare against the subtree variant. (3) Explore the effect of different h values more systematically. '
        '(4) Investigate whether adding simple structural features (e.g., clustering coefficient) can rescue '
        'performance on the regular graph failure case.'
    )

    # Save
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'report.pdf')
    pdf.output(output_path)
    print(f"Report saved to {output_path}")
    print(f"Pages: {pdf.pages_count}")


if __name__ == '__main__':
    main()
