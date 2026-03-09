# Benchmarks

- Runner: [run.py](/run.py)
- Report: [REPORT.md](/REPORT.md)

Commands:
```bash
python3 run.py
python3 run.py --runs 1 --warmup 0 --build-jobs 16
python3 run.py --entry rust__llvm
python3 run.py --benchmark mandelbrot
python3 run.py --benchmark mandelbrot --report-path /tmp/mandelbrot-report.md
```

Notes:
- Entries are auto-detected from installed toolchains. Use `--entry` to filter them.
- Active benchmarks are the retained suite defined in [run.py](/run.py).
- `--build-jobs` controls build parallelism. It should not change benchmark behavior.
- `--report-path` lets you write a targeted run somewhere else instead of overwriting the main report.
- Final binaries are stripped consistently, and the report shows actual linkage from the finished binary.
- Floating-point checks use canonical fixed precision so formatting differences do not create false mismatches.
- The suite only keeps benchmarks aligned closely enough to compare directly.
- The report stays lean by default: settings, weights, benchmark notes, entry summary, ranking, results, and mismatches.
