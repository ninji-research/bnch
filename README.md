# Benchmarks

`bnch` is a fixed-host benchmark harness for canonical, production-ready native-language implementations.

Objective:

> Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking.

## What It Optimizes For

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
- Sarif
- Nim
- OCaml
- MoonBit

The suite is single-threaded and uses release-style builds.

## Quick Start

Validate the harness:

```bash
python3 tools/validate_manifests.py
python3 -m unittest tests.test_run
```

Run the default main track:

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

Include non-canonical or experimental lanes explicitly:

```bash
python3 run.py --all-entries
python3 run.py --experimental-entries
python3 run.py --experimental-entries --all-entries
```

Write reports elsewhere:

```bash
python3 run.py --report-path /tmp/bnch.md --json-path /tmp/bnch.json
```

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

## Sarif Lane

Sarif discovery is explicit and deterministic:

- use `BNCH_SARIF_REPO` first when set
- otherwise try sibling checkouts at `~/sarif` and `~/sarif-main`
- otherwise use `sarifc` on `PATH`

For narrower experimental Sarif lanes, use honest overlap comparisons instead of pretending full-suite coverage:

```bash
python3 run.py --experimental-entries --compare-entry-overlap sarif__stage0
python3 run.py --experimental-entries --compare-entry-overlap sarif__stage0 --benchmark revcomp
```

Single-entry experimental reports are marked non-comparative in both Markdown and JSON output.

## Reading The Report

Read `REPORT.md` in this order:

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

## Retained Workloads

The current retained suite spans:
- allocation-heavy pointer and recursion pressure
- scalar numeric kernels
- floating-point iteration and simulation
- text generation and streaming transforms
- CSV parsing and group-by aggregation
- relational join plus ordered aggregation
- hashing and string-heavy counting
- sort plus frequency aggregation

Benchmark manifests live under `benchmarks/`. They define ordering, fixtures, checks, weights, capability tags, and retention rationale.

Entry manifests live under `entries/`. They define canonical entries, allowed variants, required tools, and permanent optimization policy. Experimental entries stay outside the default suite until they are genuinely ready.

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

- `run.py`: build, run, validate output, score, and report
- `benchmarks/`: benchmark manifests
- `entries/`: entry manifests
- `src/`: retained implementations
- `fixtures/`: committed inputs
- `tools/`: validation and fixture helpers
- `tests/`: harness tests

## Legal

Source code, including but not limited to implementation files, scripts, and configurations, is licensed under the [MPL-2.0](LICENSE.md) license. Documentation and informational content, such as but not limited to specifications, guides, and reports, are licensed under the [CC-BY-4.0](LICENSE-CONTENT.md) license.

Brand identity, including but not limited to the NINJI name, logos, graphics, and visual assets, is strictly proprietary. All rights are reserved. Usage, modification, or distribution of these assets is prohibited without prior written consent.

See [NOTICE.md](NOTICE.md) for full attribution details.
