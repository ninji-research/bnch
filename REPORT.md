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
| experimental_entries   | no                                                                                                                                                              |
| selected_benchmarks    | mandelbrot                                                                                                                                                      |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 1                                                                                                                                                               |
| benchmarks             | 1                                                                                                                                                               |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.02                                                                                                                                                           |
| peak_memory_mode       | cgroupv2-memory.peak                                                                                                                                            |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-cosmic-com.system76.CosmicAppList-2629.scope/memory.peak                              |
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
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 5.67                     |

## Entry Policies

| Entry                 | Build Profile | Low-Burden Optimizations                                                                                                                                  |
| --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sarif (stage0/native) | stage0-native | native executable emitted through sarifc build; stdout result mode for benchmark output parity; retained benchmark inputs declared in per-benchmark specs |

## Source Concision

| Entry                 | Benchmarks | Source Lines | Source Chars | Norm Lines | Norm Chars |
| --------------------- | ---------- | ------------ | ------------ | ---------- | ---------- |
| sarif (stage0/native) | 1          | 42           | 1124         | 1.0000     | 1.0000     |

## Benchmark Coverage

| Benchmark  | Category | Base Wt | Effective Wt | Capabilities                            | Unique Coverage                         | Retained For                                                                                                          |
| ---------- | -------- | ------- | ------------ | --------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| mandelbrot | Numeric  | 1.00    | 1.0000       | numeric_compute, tight_loops, branching | numeric_compute, tight_loops, branching | Represents scalar numeric compute with tight loop and branch behavior distinct from floating-point iterative kernels. |

## Benchmarks

| Benchmark  | Algorithm                                     | Time             | Space | Output Contract        | Fairness Notes                                                                     |
| ---------- | --------------------------------------------- | ---------------- | ----- | ---------------------- | ---------------------------------------------------------------------------------- |
| mandelbrot | scalar Mandelbrot escape-time bitmap checksum | O(size^2 * iter) | O(1)  | exact integer checksum | Input size is set to 512 because all retained implementations agree there exactly. |

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

| Benchmark  | Entry                 | Input | Output                  | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ---------- | --------------------- | ----- | ----------------------- | -------------- | ------------ | ----------------- | ----------------- | ------ |
| mandelbrot | sarif (stage0/native) | 512   | sha256:e41a9386e912a316 | 0.0367         | 0.0196       | 27.41             | 5.67              | ok     |
