# Benchmarks

`run.py` builds the retained implementations in `src/`, benchmarks them, and writes [REPORT.md](/home/user/bnch/REPORT.md).

## Run

```bash
python3 run.py
python3 run.py --runs 1 --warmup 0
python3 run.py --entry rust__llvm,go__gc
python3 run.py --benchmark mandelbrot,knucleotide
python3 run.py --report-path /tmp/bnch.md
```

## What It Does

- Activates only entries whose toolchains are installed.
- Uses the benchmark set and scoring weights defined in [run.py](/home/user/bnch/run.py).
- Accepts benchmark input from CLI args or committed fixtures under `fixtures/`.
- Strips built binaries before measurement and records observed linkage and stripped state.
- Canonicalizes float outputs before comparison.
- Scores only benchmarks where every active entry succeeds.

## Coverage

- Numeric kernels: `binarytrees`, `mandelbrot`, `spectralnorm`, `fannkuch`, `nbody`
- Text and sequence workloads: `knucleotide`, `fasta`, `revcomp`

## Retained Scope

- The suite keeps the current cross-language set: C, Go, Rust, Nim, OCaml, and MoonBit.
- The suite keeps only the high-value workload families: numeric kernels plus lean text/sequence generation, parsing, and transform workloads.
