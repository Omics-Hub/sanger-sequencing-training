# Sanger Sequencing Data Analysis — Hands-On Training

<!-- See assets/logos/README.md to add organisational logos here -->

A hands-on training module covering the full path from **PCR product to
verified gene identity**: the biology behind Sanger sequencing, how to read
the QC reports that sequencing vendors send back, and practical chromatogram
analysis using real `.ab1` files as test data.

This repo is built for **Day 2** of the training programme:

| Session | Duration | Topic |
|---|---|---|
| [1. From PCR to Sequence Data](docs/session1_pcr_to_sequence_data.md) | 30 min | PCR → sequencing workflow, PCR QC/purification, overview of sequencing output files |
| [2. Principles of Sanger Sequencing](docs/session2_principles_of_sanger_sequencing.md) | 1.5 hrs | Chain-termination chemistry, dye terminators, capillary electrophoresis, base calling, F/R reads, quality factors |
| [3. Hands-on Sequence Analysis & Guided Practice](docs/session3_hands_on_practice.md) | 3 hrs | Instructor demo + guided participant exercise: open chromatograms, assess quality, trim, build consensus, BLAST, align, troubleshoot |

## Repository structure

```
sanger-sequencing-training/
├── README.md                     ← you are here
├── docs/                         ← session-by-session facilitator guides
│   ├── session1_pcr_to_sequence_data.md
│   ├── session2_principles_of_sanger_sequencing.md
│   └── session3_hands_on_practice.md
├── data/
│   ├── raw_ab1/                  ← 14 real .ab1 chromatogram files (test data)
│   └── seq_info/                 ← vendor QC summary reports (metadata worked example)
├── scripts/
│   ├── 01_inspect_chromatogram.py   ← open an .ab1, print metadata/quality, plot trace
│   ├── 02_trim_quality.py           ← Mott's algorithm quality trimming
│   ├── 03_generate_consensus.py     ← build F/R consensus sequence
│   └── requirements.txt
└── assets/logos/                 ← see assets/logos/README.md
```

## Test data

`data/raw_ab1/` contains 14 real chromatogram files used as training material,
sequenced on an ABI 3730 capillary sequencer, in forward/reverse pairs:

```
1A-F.ab1 / 1A-R.ab1          2A-F.ab1 / 2A-R.ab1
3B-F.ab1 / 3B-R.ab1          4A-F.ab1 / 4A-R.ab1
1_AhDreb-F.ab1 / 1_AhDreb-R.ab1
2_AhDreb-F.ab1 / 2_AhDreb-R.ab1
3_AhDreb-F.ab1 / 3_AhDreb-R.ab1
```

`data/seq_info/` contains two vendor-style QC summary reports
(`P38376_KNUST_F_seq_info.txt`, `P38376_KNUST_R_seq_info.txt`) — the same
kind of per-project summary table returned by sequencing providers such as
**Functional Biosciences** or **Genewiz/Azenta**, used in Session 1 to teach
participants how to interpret Read Length, Read HQ, Read/Trim Q. Average,
etc.

## Setup

```bash
git clone <this-repo-url>
cd sanger-sequencing-training
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r scripts/requirements.txt
```

## Quick start (mirrors the Session 3 demo)

```bash
# 1. Inspect a chromatogram
python scripts/01_inspect_chromatogram.py data/raw_ab1/1_AhDreb-F.ab1

# 2. Quality-trim a read
python scripts/02_trim_quality.py data/raw_ab1/1_AhDreb-F.ab1

# 3. Build a consensus from the F/R pair
python scripts/03_generate_consensus.py \
    --forward data/raw_ab1/1_AhDreb-F.ab1 \
    --reverse data/raw_ab1/1_AhDreb-R.ab1

# 4. Confirm identity: paste the resulting *_consensus.fasta into
#    https://blast.ncbi.nlm.nih.gov/Blast.cgi (blastn, nt database)
```

Full facilitator walkthroughs, discussion prompts, and the guided participant
exercise are in [`docs/session3_hands_on_practice.md`](docs/session3_hands_on_practice.md).

## Why these scripts instead of just showing a GUI tool

Participants can absolutely use a GUI viewer (e.g. Chromas, FinchTV,
CodonCode Aligner, SnapGene) day-to-day — but walking through what a
trimming/consensus tool is actually doing, with short readable scripts,
demystifies the QC numbers vendors send back and gives participants a
reproducible, inspectable method rather than a black box.

## Acknowledgements / attribution

Test data and QC reports provided for training purposes as part of this
programme. Logos to be added per each organisation's brand guidelines — see
[`assets/logos/README.md`](assets/logos/README.md).

## License

Training materials (docs, scripts) in this repository: MIT License (see
`LICENSE`). Sequencing data files in `data/` retain whatever terms apply to
the original samples/project and are included here solely as training test
data.
