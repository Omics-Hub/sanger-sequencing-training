# Session 3 — Hands-on Sequence Analysis and Guided Practice (3 hrs)

All commands below assume you're in the repository root with the Python
environment from `scripts/requirements.txt` installed
(`pip install -r scripts/requirements.txt`).

## Part A — Instructor-led demonstration

Suggested demo dataset: **`1_AhDreb-F.ab1` / `1_AhDreb-R.ab1`** (a full-length,
generally good-quality pair — good for showing what a healthy read looks
like before moving to a messier one).

### a. Open and interpret the chromatogram
```bash
python scripts/01_inspect_chromatogram.py data/raw_ab1/1_AhDreb-F.ab1 --end 500
```
Opens the file, prints run metadata + called sequence + quality summary, and
saves a trace plot (`*_trace.png`) for the group to inspect together.

Prompts for discussion:
- Where does the trace look cleanest? Where does it degrade?
- Do any positions show two overlapping peaks?

### b. Assess sequence quality
Look together at:
- **Peak shape** — sharp vs. broad/rounded
- **Spacing** — even vs. compressed
- **Background noise** — flat baseline vs. noisy baseline
- **Mixed peaks** — two colours stacked at one position
- **Phred quality scores** — printed by the script (`Average Phred quality`,
  `Min / Max quality`)

Compare this file's live-computed average quality against the vendor
`Read Q. average` for the same sample in
`data/seq_info/P38376_KNUST_F_seq_info.txt` — they should be very close,
reinforcing that the vendor metrics are reproducible.

### c. Trim low-quality regions & generate a consensus
```bash
python scripts/02_trim_quality.py data/raw_ab1/1_AhDreb-F.ab1 --threshold 20
python scripts/02_trim_quality.py data/raw_ab1/1_AhDreb-R.ab1 --threshold 20

python scripts/03_generate_consensus.py \
    --forward data/raw_ab1/1_AhDreb-F.ab1 \
    --reverse data/raw_ab1/1_AhDreb-R.ab1
```
This reproduces the vendor's `Trim length` / `Trim Q. Average` columns, then
builds a single consensus sequence from the F/R pair (reverse-complementing
the reverse read and resolving any disagreements by quality score).

### d. Confirm sequence identity using BLASTn
Open the generated `*_consensus.fasta` file, copy the sequence, and submit
it manually at **https://blast.ncbi.nlm.nih.gov/Blast.cgi** (Nucleotide
BLAST / blastn against the `nt` database). Discuss with participants:
- Top hit organism / gene — does it match the "Gene / Trait" annotation in
  the vendor `.seq.info.txt` file for this sample?
- **Percent identity** and **E-value** — what counts as a confident match?
- Query coverage — does the whole consensus align, or only part of it?

*(BLAST is done through the NCBI web interface rather than a local/API
call, matching how most participants will actually confirm results after
this training.)*

### e. Sequence alignment to verify gene identity / detect variants
With two or more consensus sequences for the same gene/primer target
(e.g. compare `1_AhDreb` vs `2_AhDreb` vs `3_AhDreb` consensuses, all
sequenced with the `AhDreb` primer), align them with any simple pairwise or
multiple sequence alignment tool (e.g. Clustal Omega web tool, or
`Bio.Align.PairwiseAligner` as already used inside
`03_generate_consensus.py`) and look for:
- Conserved regions (confirms same gene/locus)
- SNPs or indels between samples (real biological variation vs. residual
  sequencing error — cross-check the quality score at that position before
  concluding it's a true variant)

### f. Common sequencing artefacts & troubleshooting
| Artefact seen in chromatogram | Likely cause | Troubleshooting step |
|---|---|---|
| Read starts weak/noisy for the first ~20-40 bp | Normal primer-binding noise | Trim it (already handled by the Mott's algorithm trimming step) |
| Whole read flat/noisy, `Trim length = 0` | Failed reaction, poor template, wrong primer | Repeat PCR/sequencing reaction; check gel image |
| Two overlapping peaks at many positions | Mixed template (contamination, heterozygosity, or non-specific PCR) | Re-check PCR specificity (single band?); consider cloning before sequencing |
| Sudden quality drop mid-read then N's | Secondary structure / GC-rich region | Try a different sequencing primer, or additives (e.g. betaine) in the reaction |
| Signal decays steadily after ~600-700 bp | Normal capillary sequencing read-length limit | Design internal primers if you need sequence further into the amplicon |

Use the failed rows in `data/seq_info/` (`Trim length = 0`, e.g. the
"Snake Tomato" rows, `AiNAC3`, or `02A/02B/02C_..._MeaGPL1-R`) as concrete
examples participants can open themselves in Part B.

## Part B — Guided participant exercise

Assign each participant (or small group) a **different** F/R pair from
`data/raw_ab1/` that was **not** used in the demo, e.g.:
- `2_AhDreb-F.ab1` / `2_AhDreb-R.ab1`
- `3_AhDreb-F.ab1` / `3_AhDreb-R.ab1`
- `1A-F.ab1` / `1A-R.ab1`
- `2A-F.ab1` / `2A-R.ab1`
- `3B-F.ab1` / `3B-R.ab1`
- `4A-F.ab1` / `4A-R.ab1`

Each group should independently:
1. Run `01_inspect_chromatogram.py` on both reads and assess quality visually.
2. Run `02_trim_quality.py` on both reads and compare their computed
   Trim length/Trim Q. Average against the closest matching row in
   `data/seq_info/P38376_KNUST_F_seq_info.txt` /
   `..._R_seq_info.txt` (note: filenames and vendor sample names don't
   correspond 1:1 in this teaching dataset — this is itself a good exercise
   in matching samples by length/quality signature rather than assuming
   filenames line up).
3. Run `03_generate_consensus.py` to build a consensus sequence.
4. Submit the consensus to NCBI BLASTn and identify the closest match.
5. Report back: read quality, trimmed length, top BLAST hit, and any
   artefacts observed — with facilitator feedback on interpretation.

**Facilitator note:** keep an eye out for groups assigned a pair where one
or both reads have a `Trim length` at or near 0 — this becomes a natural
teaching moment about troubleshooting failed reads (Part A.f) instead of a
"broken script" support request.
