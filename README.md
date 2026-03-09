# Benchmarks

`run.py` builds and benchmarks comparable implementations across the available toolchains in `src/`, then writes a markdown report to `REPORT.md`.

## Run

```bash
python3 run.py
python3 run.py --runs 1 --warmup 0
python3 run.py --entry rust__llvm
python3 run.py --benchmark mandelbrot
python3 run.py --report-path /tmp/bnch.md
```

## Behavior

- Entries are enabled only when their toolchains are installed.
- The suite uses the retained benchmark set defined in [run.py](/home/user/bnch/run.py).
- Finished binaries are stripped before measurement; the report records observed linkage and stripped state from the built artifact.
- Float outputs are canonicalized before comparison so formatting differences do not count as mismatches.
- Only benchmarks where every active entry succeeds are included in scoring.

## Report

`REPORT.md` contains:

- environment and scoring weights
- benchmark notes
- per-entry metadata, including startup binary size
- one combined summary table with overall score plus per-metric rank and weighted raw average
- per-benchmark results
- mismatches, when present
