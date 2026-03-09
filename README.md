# Benchmarks

`run.py` builds and benchmarks the retained implementations in `src/` and writes the report to `REPORT.md`.

## Run

```bash
python3 run.py
python3 run.py --runs 1 --warmup 0
python3 run.py --entry rust__llvm
python3 run.py --benchmark mandelbrot
python3 run.py --benchmark knucleotide
python3 run.py --report-path /tmp/bnch.md
```

## Behavior

- Entries are enabled only when their toolchains are installed.
- The suite uses the retained benchmark set defined in [run.py](/home/user/bnch/run.py).
- Benchmarks may take input either from command-line args or from committed fixtures under `fixtures/`.
- Finished binaries are stripped before measurement; the report records observed linkage and stripped state from the built artifact.
- Go is benchmarked in its normal static-binary mode rather than a non-default shared-link setup.
- Float outputs are canonicalized before comparison so formatting differences do not count as mismatches.
- Only benchmarks where every active entry succeeds are included in scoring.

## Selection

- The suite stays directly comparable across all retained languages.
- `k-nucleotide` is included as the one retained text/hash workload family; it uses a committed deterministic FASTA fixture and processes the `>THREE` section only.
- No current language is removed. Each retained entry still adds a distinct runtime/toolchain profile: C baselines, Go static runtime, Rust LLVM, Nim via C, OCaml native, and MoonBit native.
