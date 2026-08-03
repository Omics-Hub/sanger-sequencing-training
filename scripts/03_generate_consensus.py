#!/usr/bin/env python3
"""
03_generate_consensus.py
---------------------------------
Training script: Build a consensus sequence from a Forward + Reverse read pair.

Teaches participants:
  - Why every amplicon is sequenced from both directions (Forward and Reverse primer)
  - How to reverse-complement the Reverse read so both reads face the same strand
  - How to align the two trimmed reads and call a consensus base at each position,
    preferring the higher-quality base when the reads disagree (a mismatch usually
    means a sequencing error, not a real variant -- but persistent disagreement at
    the same position across replicates can indicate a true polymorphism)

This is a simplified teaching version of what tools like CodonCode Aligner /
Geneious do automatically when you "assemble" a contig from paired reads.

Usage:
    python 03_generate_consensus.py \
        --forward ../data/raw_ab1/1_AhDreb-F.ab1 \
        --reverse ../data/raw_ab1/1_AhDreb-R.ab1
"""

import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner

import sys, os
import importlib.util
# import the trimming function directly from the sibling script file (02_trim_quality.py)
spec = importlib.util.spec_from_file_location(
    "trim_quality", os.path.join(os.path.dirname(__file__), "02_trim_quality.py"))
trim_quality = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trim_quality)


def load_trimmed(ab1_path, threshold=20):
    record = SeqIO.read(ab1_path, "abi")
    qual = record.letter_annotations["phred_quality"]
    seq = str(record.seq)
    start, end = trim_quality.mott_trim(qual, threshold=threshold)
    return seq[start:end], qual[start:end]


def build_consensus(fwd_path, rev_path, threshold=20):
    fwd_seq, fwd_qual = load_trimmed(fwd_path, threshold)
    rev_seq_raw, rev_qual_raw = load_trimmed(rev_path, threshold)

    # Reverse-complement the reverse read (and reverse its quality scores to match)
    rev_seq = str(Seq(rev_seq_raw).reverse_complement())
    rev_qual = list(reversed(rev_qual_raw))

    print(f"Forward trimmed length: {len(fwd_seq)} bp")
    print(f"Reverse trimmed length (after revcomp): {len(rev_seq)} bp")

    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -0.5
    aligner.mismatch_score = -1
    aligner.match_score = 2
    alignment = aligner.align(fwd_seq, rev_seq)[0]

    aligned_fwd, aligned_rev = str(alignment[0]), str(alignment[1])

    consensus = []
    mismatches = 0
    fi = ri = 0  # pointers into original (ungapped) quality arrays
    for a, b in zip(aligned_fwd, aligned_rev):
        qa = fwd_qual[fi] if a != "-" else -1
        qb = rev_qual[ri] if b != "-" else -1
        if a != "-":
            fi += 1
        if b != "-":
            ri += 1

        if a == "-":
            consensus.append(b)
        elif b == "-":
            consensus.append(a)
        elif a == b:
            consensus.append(a)
        else:
            mismatches += 1
            # disagreement: keep the base with higher Phred quality
            consensus.append(a if qa >= qb else b)

    consensus_seq = "".join(consensus)
    identity = alignment.score  # not a percentage; informational only
    print(f"Alignment length: {len(aligned_fwd)}")
    print(f"Mismatched columns: {mismatches}")
    print(f"Consensus length: {len(consensus_seq)} bp")

    out_name = fwd_path.rsplit("/", 1)[-1].split(".")[0].replace("-F", "").replace("_F", "")
    out_fasta = f"{out_name}_consensus.fasta"
    with open(out_fasta, "w") as fh:
        fh.write(f">{out_name}_consensus (from {fwd_path.split('/')[-1]} + {rev_path.split('/')[-1]})\n")
        for i in range(0, len(consensus_seq), 60):
            fh.write(consensus_seq[i:i + 60] + "\n")
    print(f"Consensus FASTA written to: {out_fasta}")
    print("\nNext step for participants: paste this FASTA into NCBI BLASTn "
          "(https://blast.ncbi.nlm.nih.gov/Blast.cgi) to confirm gene identity.")
    return consensus_seq


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a consensus sequence from paired F/R Sanger reads")
    parser.add_argument("--forward", required=True, help="Path to forward .ab1 file")
    parser.add_argument("--reverse", required=True, help="Path to reverse .ab1 file")
    parser.add_argument("--threshold", type=int, default=20, help="Quality trim threshold")
    args = parser.parse_args()
    build_consensus(args.forward, args.reverse, threshold=args.threshold)
