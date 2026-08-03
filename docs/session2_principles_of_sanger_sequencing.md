# Session 2 — Principles of Sanger Sequencing (1.5 hrs)

## 1. Chain-termination sequencing (Sanger, 1977)

DNA polymerase extends a primer along a single-stranded template, incorporating
normal deoxynucleotides (dNTPs) **and** a small fraction of
dideoxynucleotides (ddNTPs). A ddNTP lacks the 3'-OH group needed to add the
next base, so any strand that incorporates one **terminates** at that
position. Across millions of template copies, termination happens at every
possible position, generating a nested set of fragments of every length,
each ending in a base-specific ddNTP.

## 2. Cycle sequencing chemistry and fluorescent dye terminators

Modern Sanger sequencing uses **BigDye Terminator** cycle sequencing:
- Each of the 4 ddNTPs (ddATP, ddCTP, ddGTP, ddTTP) is labelled with a
  **different fluorescent dye**.
- The reaction is thermal-cycled (like PCR, but with a single primer —
  linear amplification, not exponential).
- Output: a population of fragments of every length, each fluorescently
  colour-coded by its terminal base.

## 3. Capillary electrophoresis and fragment detection

Fragments are injected into a **capillary filled with polymer** and
separated by size under an electric field (small fragments migrate faster).
A laser excites the dyes as fragments pass a detection window near the
capillary outlet, and a camera/detector records the fluorescence emission
as a function of time.

This produces the **4-colour trace** you see in a chromatogram viewer —
one colour per base, in most current chromatogram viewers:
- **Green = A**, **Red = T**, **Black = G**, **Blue = C**
  (this is the palette used by `scripts/01_inspect_chromatogram.py`).

## 4. Base calling and chromatogram generation

Software (e.g. KB Basecaller on the instrument, or Phred) analyses peak
positions and assigns:
- A **called base** at each peak
- A **Phred quality score** (`Q = -10 log10(P_error)`), e.g. Q30 = 1 in 1000
  chance the call is wrong, Q50 ≈ 1 in 100,000
- The result is stored in the **.ab1 (ABIF) file format**, containing both
  the base calls/qualities *and* the raw 4-channel trace data.

Run `scripts/01_inspect_chromatogram.py` live here to show a real trace and
point out: even peak spacing early/mid-read, and where quality typically
degrades toward the read's end.

## 5. Forward and reverse sequencing reads

Every amplicon in this dataset was sequenced twice — once with the
**forward primer** and once with the **reverse primer** (see the paired
`*-F.ab1` / `*-R.ab1` and `*_AhDreb-F.ab1` / `*_AhDreb-R.ab1` files in
`data/raw_ab1/`). Why:
- The **start of a read is usually lower quality** (primer/dye front noise),
  so sequencing from both ends means the region that's weak on the forward
  read is often the strongest part of the reverse read (and vice versa).
- Reading a base from **both strands independently** is the standard way to
  confirm a call is real and not a sequencing artefact — this is exactly
  what `scripts/03_generate_consensus.py` does by reverse-complementing the
  reverse read and reconciling any disagreement with the forward read.

## 6. Factors affecting sequence quality / read accuracy

| Factor | Effect on chromatogram |
|---|---|
| Poor/impure template (residual salts, protein, PCR primers) | High background noise, weak signal |
| Too much or too little template | Overloaded ("blobby") peaks or very short usable read |
| Secondary structure / GC-rich regions | Compressions, peak spacing irregularities |
| Heterozygous site or mixed template (2 alleles/organisms) | Overlapping double peaks at one position |
| Signal decay toward the end of a long read | Progressive drop in peak height & resolution |
| Dye blobs (excess unincorporated terminators) | Broad non-specific peaks, usually near read start |

Tie this table directly to the QC report columns from Session 1
(`Read Q. average` vs `Trim Q. Average`) — a big gap between the two tells
you *where* in the read the problems are, even before opening the
chromatogram.
