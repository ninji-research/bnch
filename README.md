# bnch

`bnch` is a fixed-host benchmark harness for canonical, production-ready native-language implementations.

Objective:

> Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking.

## Core Philosophy

- Correctness gates ranking
- One canonical entry per language in the main track
- Fixed host, fixed fixtures, fixed output contracts
- Category-balanced composite with raw metric views kept visible
- Permanent low-burden production optimizations are allowed and disclosed
- Variant compiler and backend runs stay separate from the main track
- Experimental entries stay opt-in and never count as canonical retained-suite coverage

## Main Track

The default run compares canonical entries in:

- C
- Go
- Rust
- Nim
- OCaml
- MoonBit

Experimental track:

- Sarif currently has real experimental `mandelbrot`, `fasta`, `nbody`, `revcomp`, `spectralnorm`, and `knucleotide` entries. They stay excluded from the default suite until broader retained-benchmark coverage and the self-hosting/toolchain story are both stronger.
- Sarif `fasta` uses the sibling Sarif toolchain's maintained text-builder/runtime support, `nbody` uses its maintained float/runtime-arg support, `revcomp` uses its maintained stdin-text/text-builder/runtime support, `spectralnorm` uses the maintained list-based float substrate, and `knucleotide` uses maintained typed-list plus stdin-text/text-builder support. They are gated by the experimental track policy and by Sarif toolchain availability on the current machine, not by missing source-level capabilities.

The suite is single-threaded and uses release-style builds.

## What The Harness Produces

Per benchmark entry:

- Median runtime
- Peak memory
- Build time
- Stripped binary size

Across the suite:

- Category-balanced composite score
- Metric-specific views for speed, memory, build cost, and size
- Decision profiles for different priorities
- Benchmark coverage with category, base weight, effective weight, capabilities, unique coverage, and retention rationale
- Entry policy disclosure for permanent low-burden optimizations

## Retained Workloads

The current suite covers:

- allocation-heavy pointer and recursion pressure
- scalar numeric kernels
- floating-point iteration and simulation
- text generation and streaming transforms
- CSV parsing and group-by aggregation
- relational join plus ordered aggregation
- hashing and string-heavy counting
- sort plus frequency aggregation

Benchmark manifests live under [benchmarks](/home/user/bnch/benchmarks). They define ordering, inputs, checks, weights, capability tags, and retention rationale.

Entry manifests live under [entries](/home/user/bnch/entries). They define canonical entries, allowed variants, required tools, and permanent optimization policy.
Experimental manifests may also declare `track = "experimental"` to stay out of the default suite until they are genuinely ready.

## Quick Start

Validate the repo:

```bash
python3 tools/validate_manifests.py
python3 -m unittest tests.test_run
```

Run the main track:

```bash
python3 run.py
```

Run a fast smoke pass:

```bash
python3 run.py --runs 1 --min-runs 1 --warmup 0
```

Run a subset:

```bash
python3 run.py --entry rust__llvm,go__gc
python3 run.py --benchmark mandelbrot,knucleotide
```

Include non-canonical variants:

```bash
python3 run.py --all-entries
```

Include experimental entries explicitly:

```bash
python3 run.py --experimental-entries
python3 run.py --experimental-entries --all-entries
```

Sarif toolchain discovery uses `BNCH_SARIF_REPO` first when set, then sibling checkouts at `~/sarif` and `~/sarif-main`, then an installed `sarifc` on `PATH`.

Single-entry experimental reports are marked non-comparative in both Markdown and JSON output. They are useful for validating one language entry end-to-end, but they do not support honest cross-language ranking claims.

Run an honest overlap comparison for one entry against the rest of the suite:

```bash
python3 run.py --experimental-entries --compare-entry-overlap sarif__stage0
python3 run.py --experimental-entries --compare-entry-overlap sarif__stage0 --benchmark revcomp
```

`--compare-entry-overlap` automatically includes the named entry and restricts the benchmark set to what that entry actually supports, which is the right way to compare a narrower experimental lane without pretending it covers the full retained suite.

Write reports elsewhere:

```bash
python3 run.py --report-path /tmp/bnch.md --json-path /tmp/bnch.json
```

## Reading The Report

Read [REPORT.md](/home/user/bnch/REPORT.md) in this order:

1. Environment
2. Entry Policies
3. Benchmark Coverage
4. Decision Profiles
5. Categories
6. Summary
7. Speed, Memory, Build, and Size views
8. Raw results

Use the benchmark coverage table to audit suite shape and weights.
Use metric views and decision profiles when the decision is narrower than the default composite.

## Toolchains

The harness only runs entries whose required tools exist on the current machine. In practice that means some or all of:

- `clang` or `gcc`
- `go`
- `rustc`
- `nim`
- `ocamlopt`
- `moon`
- `strip`

If no supported toolchains are available, `run.py` exits.

## Optimization Policy

Permanent tailored optimizations are kept when they are:

- standard for production release builds
- low maintenance
- stable across toolchain updates
- not benchmark-specific tricks

The report exposes these under `Entry Policies` so optimization policy stays reviewable instead of disappearing into build code.

## Development Standard

Any harness change should leave the repo passing:

```bash
python3 tools/validate_manifests.py
python3 -m unittest tests.test_run
python3 run.py --runs 1 --min-runs 1 --warmup 0
```

Use the full `python3 run.py` before treating a benchmark-harness change as complete.

## Repository Layout

- [run.py](/home/user/bnch/run.py): build, run, validate output, score, and report
- [benchmarks](/home/user/bnch/benchmarks): benchmark manifests
- [entries](/home/user/bnch/entries): entry manifests
- [src](/home/user/bnch/src): retained implementations
- [fixtures](/home/user/bnch/fixtures): committed inputs
- [tools](/home/user/bnch/tools): validation and fixture helpers
- [tests](/home/user/bnch/tests): harness tests
