# Session 1 — From PCR to Sequence Data (30 min)

## 1. Workflow: PCR amplification → Sanger sequencing

```
Genomic DNA / cDNA
        │  (gene-specific primers)
        ▼
   PCR amplification  ──►  Gel electrophoresis (confirm single band, expected size)
        │
        ▼
   PCR clean-up / purification (remove primers, dNTPs, salts)
        │
        ▼
   Cycle sequencing (BigDye Terminator chemistry, one primer at a time)
        │
        ▼
   Post-sequencing clean-up (remove unincorporated dye terminators)
        │
        ▼
   Capillary electrophoresis on a genetic analyzer (e.g. ABI 3730)
        │
        ▼
   .ab1 chromatogram + base-called sequence (FASTA)
```

This repository's `data/raw_ab1/` files are real output from this pipeline
(sequenced on an **ABI 3730**, per the AB1 file metadata) — a good anchor for
this discussion.

## 2. PCR product quality assessment and purification

Before sending a PCR product for sequencing, submitters normally confirm:
- **Single, clean band** of the expected size on an agarose gel (a smear or
  multiple bands means non-specific amplification, which will produce a
  messy/mixed chromatogram downstream).
- **Sufficient concentration** — sequencing facilities specify a minimum
  ng/µl for a given amplicon size (too little template gives weak/no signal;
  too much can overload the reaction and cause blobbing).
- **Primer/dye removal** — leftover primers or unincorporated dNTPs from PCR
  interfere with the sequencing reaction if the product isn't purified
  (column clean-up or ExoSAP-IT treatment).

**Discussion prompt:** ask participants what they think happens to the
chromatogram if a poorly purified or double-banded PCR product is submitted —
tie this back to the "mixed peaks" and "high background noise" they will see
in Session 3.

## 3. Overview of sequencing outputs

When a facility such as **Functional Biosciences** or **Genewiz (Azenta)**
returns results, participants typically receive:

| File type | What it contains |
|---|---|
| `.ab1` | The raw chromatogram: 4-channel fluorescence trace + base calls + per-base Phred quality scores + run metadata (instrument, run date/time). This is the file format used throughout this training. |
| `.fasta` / `.seq` | Plain-text called sequence, no trace or quality information — useful for BLAST/alignment but you lose the ability to inspect quality visually. |
| `.seq.info.txt` / summary report | A per-project **QC summary table** across all submitted reads (see Session 1 handout: `data/seq_info/`) — this is what we will decode next. |

### Reading the vendor QC summary file

Open `data/seq_info/P38376_KNUST_F_seq_info.txt` and
`data/seq_info/P38376_KNUST_R_seq_info.txt` with participants and walk
through the columns:

| Column | Meaning |
|---|---|
| **Name** | Sample identifier, often encoding sample #, plant ID/variety, and primer used (e.g. `11F_106_12A_Nkentema_MeaGPL1-F`) |
| **Primer** | Primer(s) used for the sequencing reaction |
| **Gene / Trait** | The target gene and the trait it's associated with (submitter-provided annotation) |
| **Read Length (bp)** | Total number of bases called by the instrument software, good and bad |
| **Read HQ** | Number of *high-quality* bases (above the Phred threshold) found anywhere in the read |
| **Read Q. average** | Average Phred quality across the *entire* raw read |
| **Trim length (bp)** | Length of the contiguous high-quality window kept after quality trimming (see Session 3 — this is the Mott's-algorithm trimming we will reproduce ourselves) |
| **Trim Q. Average** | Average Phred quality *within that trimmed window* — should be noticeably higher than the raw average |

Point out the failed reads in the handout — e.g. the three **"Snake Tomato"**
rows and the `AiNAC3` row all show **Trim length = 0**, meaning the entire
read failed the quality threshold. The reverse-read summary
(`P38376_KNUST_R_seq_info.txt`) shows the same pattern for
`02A/02B/02C_..._MeaGPL1-R` and `04H_..._MIPSV-R` (Trim length = 0) — a good
prompt to ask participants *why* a read might fail completely (poor
template, failed reaction, wrong primer, degraded sample).

> **Facilitator tip:** the reverse-read file header also reports
> `Trim quality value (window=20, threshold): 20` — this is the exact
> parameter used by `scripts/02_trim_quality.py` in Session 3, so you can
> show participants that the numbers in the vendor report are reproducible,
> not a black box.
