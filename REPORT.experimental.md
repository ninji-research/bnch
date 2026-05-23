# Benchmark Report

## Environment

| Setting                | Value                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| objective              | Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking. |
| runs                   | 1                                                                                                                                                               |
| min_runs               | 1                                                                                                                                                               |
| warmup                 | 0                                                                                                                                                               |
| runtime_target_s       | 0.35                                                                                                                                                            |
| max_relative_spread    | 0.03                                                                                                                                                            |
| build_jobs             | 16                                                                                                                                                              |
| canonical_entries_only | yes                                                                                                                                                             |
| experimental_entries   | yes                                                                                                                                                             |
| selected_benchmarks    | primecount                                                                                                                                                      |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 1                                                                                                                                                               |
| benchmarks             | 1                                                                                                                                                               |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.02                                                                                                                                                           |
| peak_memory_mode       | ru_maxrss                                                                                                                                                       |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/session-3.scope/memory.peak unavailable for reset (Permission denied)                                                 |
| kernel                 | 7.0.6-32.stable                                                                                                                                                 |
| gcc                    | gcc (AerynOS) 16.1.1 20260505                                                                                                                                   |
| clang                  | clang version 22.1.5 (AerynOS)                                                                                                                                  |
| go                     | go version go1.26.3 linux/amd64                                                                                                                                 |
| rustc                  | rustc 1.95.0 (59807616e 2026-04-14)                                                                                                                             |
| nim                    | Nim Compiler Version 2.2.10 [Linux: amd64]                                                                                                                      |
| ocamlopt               | 5.4.1                                                                                                                                                           |
| moon                   | moon 0.1.20260512 (81d40e3 2026-05-12)                                                                                                                          |
| strip                  | GNU strip (GNU Binutils) 2.46.0                                                                                                                                 |
| sarifc                 | sarifc 0.1.0                                                                                                                                                    |

## Entries

| Entry                 | Compiler | Backend | Linkage | Stripped | Binary Size Sample (KiB) |
| --------------------- | -------- | ------- | ------- | -------- | ------------------------ |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 6.56                     |

## Entry Policies

| Entry                 | Build Profile | Low-Burden Optimizations                                                                                                                                  |
| --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sarif (stage0/native) | stage0-native | native executable emitted through sarifc build; stdout result mode for benchmark output parity; retained benchmark inputs declared in per-benchmark specs |

## Source Concision

| Entry                 | Benchmarks | Source Lines | Source Chars | Norm Lines | Norm Chars |
| --------------------- | ---------- | ------------ | ------------ | ---------- | ---------- |
| sarif (stage0/native) | 1          | 32           | 571          | 1.0000     | 1.0000     |

## Benchmark Coverage

| Benchmark  | Category | Base Wt | Effective Wt | Capabilities                                      | Unique Coverage                                   | Retained For                                                                                    |
| ---------- | -------- | ------- | ------------ | ------------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| primecount | Numeric  | 1.00    | 1.0000       | numeric_compute, integer_division, integer_modulo | numeric_compute, integer_division, integer_modulo | Only benchmark centered on integer division and modulo throughput with deterministic branching. |

## Benchmarks

| Benchmark  | Algorithm                     | Time         | Space | Output Contract                   | Fairness Notes                                                                         |
| ---------- | ----------------------------- | ------------ | ----- | --------------------------------- | -------------------------------------------------------------------------------------- |
| primecount | trial-division prime counting | O(n sqrt(n)) | O(1)  | exact I32 count of primes below n | No precomputed tables; each candidate trial-divided by all odd integers up to sqrt(n). |

## Interpretation

This report is non-comparative: only one scored entry is present, so ranks and normalized scores are placeholders rather than cross-language conclusions.

## Decision Profiles

| Profile      | Leader                | Runner-Up | Third | Intent                                                               |
| ------------ | --------------------- | --------- | ----- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | -         | -     | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | -         | -     | Throughput or latency matters most.                                  |
| Memory First | sarif (stage0/native) | -         | -     | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | -         | -     | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | -         | -     | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Overall |
| --------------------- | ------- | ------- |
| sarif (stage0/native) | 1.0000  | 1.0000  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 1.0000          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 1.0000       | 1.0000          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 1.0000          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | sarif (stage0/native) | 1.0000     | 1.0000          |

## Results

| Benchmark  | Entry                 | Input | Output | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ---------- | --------------------- | ----- | ------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| primecount | sarif (stage0/native) | 50000 | 5133   | 0.0386         | 0.0028       | 39.52             | 6.56              | ok     |
