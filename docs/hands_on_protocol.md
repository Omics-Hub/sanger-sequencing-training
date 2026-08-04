# Hands-On Protocol: BioEdit → NCBI BLASTn → MEGA → iTOL

A step-by-step lab protocol for taking a raw `.ab1` chromatogram all the way through to an annotated phylogenetic tree. Written for the GUI-only workflow (no programming required).

**Assumes:** BioEdit, FinchTV, MEGA installed; internet access for NCBI BLASTn and iTOL.

---

## Part 1 — BioEdit: Trim, Assemble, Export FASTA

1. **Open both reads** — `File → Open`, load your F and R `.ab1` files.
2. **Check quality in FinchTV first** (see previous quality-reading steps) — note the approximate trim points where Phred scores consistently clear Q20.
3. **In BioEdit, trim each read** — mask/delete the noisy 5′ start and declining 3′ tail, using your FinchTV-confirmed trim points and the vendor `seq_info.txt` trim length as a cross-check.
4. **Reverse complement the R read** — `Sequence → Nucleic Acid → Reverse Complement`, so both reads face the same direction.
5. **Assemble a consensus** — select both trimmed reads → `Accessory Application → CAP Contig Assembly Program` (or your BioEdit version's equivalent contig assembly tool). Where F and R disagree at a position, open both chromatograms and check the actual peaks before accepting a base.
6. **Export the consensus** — `File → Export → Nucleic Acid` (or copy from the alignment window) → save as FASTA, named clearly per sample (e.g., `1_AhDreb_consensus.fasta`).

**Checkpoint:** you should now have one clean, single FASTA file per sample, representing your best-confidence consensus sequence.

---

## Part 2 — NCBI BLASTn: Confirm Identity, Get Top Hits

1. Go to the NCBI BLASTn web tool: `https://blast.ncbi.nlm.nih.gov/Blast.cgi` → select **nucleotide blast**.
2. **Paste your consensus FASTA** into the query box (or upload the `.fasta` file directly).
3. **Choose your database** — typically `Nucleotide collection (nr/nt)` for a broad identity check, or a more targeted database if your gene/species is known.
4. **Set search parameters:**
   - Under **Algorithm parameters → General Parameters**, set **Max target sequences** to control how many hits are returned (set to **10** for a manageable top-hit list).
   - Under **Max target sequences** or the results filter, apply an **E-value threshold of 1e-5** — this keeps only statistically strong matches and filters out weak/spurious hits.
5. Click **BLAST** and wait for results.
6. **Interpret the hit table:**

   | Metric | What to look for |
   |---|---|
   | Percent identity | High (>95–98%) for a confirmed match |
   | Query coverage | Should span most of the query |
   | E-value | ≤ 1e-5 (very low, near 0 is ideal) |
   | Description | Should match your expected gene/primer target |

7. **Download the top 10 hits as FASTA** — on the results page, select the top 10 hits (checkboxes next to each), then `Download → FASTA (aligned sequences)` or `FASTA (complete sequence)`. Save this file (e.g., `top10_blast_hits.fasta`).
8. **Combine files for alignment** — open both your own consensus FASTA and the downloaded top-10-hits FASTA in a text editor, and combine them into a single multi-FASTA file (e.g., `alignment_input.fasta`). Your own sequence plus the top 10 references is what MEGA will align next.

**Checkpoint:** you should now have one multi-FASTA file containing your sample + up to 10 closest BLAST matches.

---

## Part 3 — MEGA: Alignment, Tree, and Pairwise Distance Matrix

### 3a. Align the sequences

1. Open MEGA → `Align → Edit/Build Alignment → Create a new alignment` → choose **Nucleotide**.
2. `Edit → Insert Sequence from File` (or drag-and-drop) → import your combined `alignment_input.fasta`.
3. Select all sequences → `Alignment → Align by ClustalW` (or MUSCLE) → run with default parameters.
4. Review the alignment window — trim any obviously misaligned ends if needed, then close and save the alignment (`.mas` or export as `.fasta`/`.meg`).

### 3b. Build a phylogenetic tree

1. From the aligned data, go to `Phylogeny → Construct/Test Neighbor-Joining Tree` (or Maximum Likelihood if you want a more rigorous tree and have time).
2. Use default parameters unless your facilitator specifies otherwise (e.g., bootstrap replications — 500 or 1000 is standard for a quick confidence check).
3. Run the analysis — MEGA will display the tree in a Tree Explorer window.
4. **Export the tree in Newick format** — `File → Export Current Tree (Newick)` from the Tree Explorer → save as `.nwk` (e.g., `sample_tree.nwk`). This is the file iTOL needs.

### 3c. Generate a pairwise distance matrix

1. With the same aligned data open, go to `Distance → Compute Pairwise Distances`.
2. Choose a substitution model (e.g., **p-distance** for a simple, quick comparison, or **Kimura 2-parameter** for a more standard genetic-distance estimate).
3. Run — MEGA displays a matrix of pairwise distances between every pair of sequences in your alignment.
4. **Export the matrix** — `File → Export Distance Data` (or copy from the results window) → save as a `.csv`/`.txt` file (e.g., `pairwise_distance_matrix.csv`) or as a Word/Excel-exportable table if your report requires it.

**Checkpoint:** you should now have (1) a `.nwk` tree file and (2) a pairwise distance matrix file.

---

## Part 4 — iTOL: Visualize and Annotate the Tree

1. Go to the iTOL website: `https://itol.embl.de/`.
2. Click **Upload** → select your `sample_tree.nwk` file.
3. The tree renders automatically. Use the **Basic** controls on the right panel to:
   - Switch between circular/rectangular layout
   - Adjust branch length display and font size
4. **Rename leaf labels** if needed — click a leaf label directly, or use `Advanced → Edit labels` to replace raw accession numbers/sample codes with meaningful names (e.g., your sample ID instead of a GenBank accession).
5. **Add annotation datasets** (optional but recommended for a polished figure) — under the **Datasets** panel, add a simple colored strip or symbol dataset (e.g., color-coding by primer, gene target, or sample origin) using a small tab-delimited annotation file per iTOL's template format.
6. **Export the final figure** — `Export` (top menu) → choose SVG, PDF, or PNG depending on where the figure will be used (SVG/PDF for publication-quality, PNG for slides).

**Checkpoint:** a finished, annotated tree image ready for your final report.

---

## Summary: File Handoffs Between Tools

| From | File produced | To | Used for |
|---|---|---|---|
| BioEdit | Consensus `.fasta` | NCBI BLASTn | Identity confirmation |
| NCBI BLASTn | Top-10-hits `.fasta` | MEGA | Alignment reference set |
| MEGA | `.nwk` tree file | iTOL | Tree visualization |
| MEGA | Pairwise distance matrix | Final report | Quantitative comparison |
