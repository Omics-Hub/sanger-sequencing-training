#!/usr/bin/env python3
"""
02_trim_quality.py
---------------------------------
Training script: Trim low-quality ends off a Sanger read.

Teaches participants:
  - Why the start and end of a Sanger read are usually low quality (primer
    binding noise at the start; signal decay/dye blobs at the end)
  - How commercial reports (Functional Biosciences, Genewiz/Azenta) define
    "Trim Length" / "Trim Q. Average" using a sliding quality-window algorithm
  - How to reproduce that trimming step yourself instead of trusting a black box

Method: Mott's modified trimming algorithm (the same approach used by phred/
Sequencher/CodonCode and referenced in the vendor .seq.info reports as
"Trim quality value (window=20, threshold)"):
    1. Convert each Phred quality score q to an error probability-based score: q - threshold
    2. Compute the running sum of these scores across the read
    3. The trimmed region is the stretch between the running sum's minimum
       (before it starts climbing) and its maximum (best cumulative window)

Usage:
    python 02_trim_quality.py ../data/raw_ab1/1_AhDreb-F.ab1 --threshold 20
"""

import argparse
from Bio import SeqIO


def mott_trim(qualities, threshold=20):
    """Return (start, end) indices (0-based, end exclusive) of the high-quality region."""
    scores = [q - threshold for q in qualities]
    running_sum = 0
    max_sum = 0
    start = end = 0
    tmp_start = 0
    for i, s in enumerate(scores):
        running_sum += s
        if running_sum < 0:
            running_sum = 0
            tmp_start = i + 1
        if running_sum > max_sum:
            max_sum = running_sum
            start = tmp_start
            end = i + 1
    return start, end


def trim_ab1(ab1_path, threshold=20, out_fasta=None):
    record = SeqIO.read(ab1_path, "abi")
    qual = record.letter_annotations["phred_quality"]
    seq = str(record.seq)

    start, end = mott_trim(qual, threshold=threshold)
    trimmed_seq = seq[start:end]
    trimmed_qual = qual[start:end]
    avg_q = sum(trimmed_qual) / len(trimmed_qual) if trimmed_qual else 0

    print(f"File: {ab1_path}")
    print(f"Raw length: {len(seq)} bp")
    print(f"Trimmed region: bases {start}-{end} ({end - start} bp)")
    print(f"Trimmed average quality: {avg_q:.1f}")
    if end - start == 0:
        print("WARNING: no region passed the quality threshold -- this read likely failed "
              "(compare to a 'Trim length = 0' row in the vendor .seq.info.txt file).")

    out_fasta = out_fasta or ab1_path.rsplit("/", 1)[-1].replace(".ab1", "_trimmed.fasta")
    name = ab1_path.rsplit("/", 1)[-1].replace(".ab1", "")
    with open(out_fasta, "w") as fh:
        fh.write(f">{name} trimmed[{start}:{end}] avgQ={avg_q:.1f}\n")
        for i in range(0, len(trimmed_seq), 60):
            fh.write(trimmed_seq[i:i + 60] + "\n")
    print(f"Trimmed FASTA written to: {out_fasta}")
    return trimmed_seq, avg_q


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quality-trim a Sanger .ab1 read (Mott's algorithm)")
    parser.add_argument("ab1_file", help="Path to .ab1 file")
    parser.add_argument("--threshold", type=int, default=20,
                         help="Phred quality threshold (vendor reports typically use 20)")
    args = parser.parse_args()
    trim_ab1(args.ab1_file, threshold=args.threshold)
