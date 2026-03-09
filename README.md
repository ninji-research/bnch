# Benchmarks

- Runner: [run.py](/run.py)
- Report: [REPORT.md](/REPORT.md)

Commands:
```bash
python3 run.py
python3 run.py --runs 1 --warmup 0 --workers 16
python3 run.py --entry c__gcc
python3 run.py --benchmark mandelbrot
```

Entries:
- `c__gcc`
- `c__clang`
- `rust__llvm`
- `nim__gcc`
- `nim__clang`
- `ocaml__native`
- `moonbit__native`

Benchmarks:
- `ackermann`
- `binarytrees`
- `mandelbrot`
- `spectralnorm`
- `fannkuch`
- `nbody`
- `picalc`
- `startup`
