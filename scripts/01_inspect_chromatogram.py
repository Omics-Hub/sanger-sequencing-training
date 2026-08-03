#!/usr/bin/env python3
"""
01_inspect_chromatogram.py
---------------------------------
Training script: Open an .ab1 chromatogram and inspect its contents.

Teaches participants:
  - How Sanger chromatogram files (.ab1) are structured (base calls + 4-channel trace data + quality)
  - How to pull out the called sequence, per-base Phred quality scores, and run metadata
  - How to visualise the raw trace so quality issues (mixed peaks, noise, poor spacing) become visible

Usage:
    python 01_inspect_chromatogram.py ../data/raw_ab1/1A-F.ab1
"""

import sys
import argparse
from Bio import SeqIO
import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt


def inspect(ab1_path: str, plot_range: tuple = (0, 400), out_png: str = None):
    record = SeqIO.read(ab1_path, "abi")

    seq = str(record.seq)
    qual = record.letter_annotations.get("phred_quality", [])

    print(f"File: {ab1_path}")
    print(f"Sample/machine model: {record.annotations.get('machine_model')}")
    print(f"Run start:  {record.annotations.get('run_start')}")
    print(f"Run finish: {record.annotations.get('run_finish')}")
    print(f"Called sequence length: {len(seq)} bp")
    if qual:
        avg_q = sum(qual) / len(qual)
        print(f"Average Phred quality: {avg_q:.1f}")
        print(f"Min / Max quality: {min(qual)} / {max(qual)}")
    print(f"First 60 bp: {seq[:60]}")
    print(f"Ambiguous bases (N or IUPAC codes) in first 60 bp: "
          f"{sum(1 for b in seq[:60] if b not in 'ACGT')}")

    # --- Raw 4-channel trace data lives in the ABIF 'DATA' fields ---
    # channel order is given by FWO_1 (Filter Wheel Order), typically G,A,T,C
    abif_raw = record.annotations["abif_raw"]
    order = abif_raw["FWO_1"].decode()  # e.g. b'GATC' -> 'GATC'
    channel_map = {"G": "DATA9", "A": "DATA10", "T": "DATA11", "C": "DATA12"}
    # DATA9-12 are the standard processed trace channels in that FWO_1 order
    traces = {base: abif_raw[channel_map[base]] for base in order}

    colors = {"G": "black", "A": "green", "T": "red", "C": "blue"}
    start, end = plot_range
    plt.figure(figsize=(12, 4))
    for base in order:
        plt.plot(traces[base][start:end], color=colors[base], label=base, linewidth=0.8)
    plt.legend(loc="upper right")
    plt.title(f"Raw trace: {ab1_path.split('/')[-1]}  (data points {start}-{end})")
    plt.xlabel("Data point")
    plt.ylabel("Signal intensity")
    plt.tight_layout()

    out_png = out_png or ab1_path.rsplit("/", 1)[-1].replace(".ab1", "_trace.png")
    plt.savefig(out_png, dpi=150)
    print(f"\nTrace plot saved to: {out_png}")
    print("Look for: sharp single peaks (good), overlapping double peaks (mixed base/heterozygote"
          " or contamination), flat/noisy baseline (poor quality), and even peak spacing (good run).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect a Sanger .ab1 chromatogram")
    parser.add_argument("ab1_file", help="Path to .ab1 file")
    parser.add_argument("--start", type=int, default=0, help="Trace plot start (data points)")
    parser.add_argument("--end", type=int, default=400, help="Trace plot end (data points)")
    args = parser.parse_args()
    inspect(args.ab1_file, plot_range=(args.start, args.end))
