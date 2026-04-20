# Benchmark Report

## Environment

| Setting                | Value                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| objective              | Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking. |
| runs                   | 5                                                                                                                                                               |
| min_runs               | 2                                                                                                                                                               |
| warmup                 | 1                                                                                                                                                               |
| runtime_target_s       | 0.35                                                                                                                                                            |
| max_relative_spread    | 0.03                                                                                                                                                            |
| build_jobs             | 16                                                                                                                                                              |
| canonical_entries_only | yes                                                                                                                                                             |
| experimental_entries   | no                                                                                                                                                              |
| selected_benchmarks    | binarytrees                                                                                                                                                     |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 7                                                                                                                                                               |
| benchmarks             | 1                                                                                                                                                               |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.03                                                                                                                                                           |
| peak_memory_mode       | ru_maxrss                                                                                                                                                       |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/session-3.scope/memory.peak unavailable for reset (Permission denied)                                                 |
| kernel                 | 6.18.22-1.stable                                                                                                                                                |
| gcc                    | gcc (AerynOS) 15.2.1 20260319                                                                                                                                   |
| clang                  | clang version 22.1.3 (AerynOS)                                                                                                                                  |
| go                     | go version go1.26.2 linux/amd64                                                                                                                                 |
| rustc                  | rustc 1.95.0 (59807616e 2026-04-14)                                                                                                                             |
| nim                    | Nim Compiler Version 2.2.8 [Linux: amd64]                                                                                                                       |
| ocamlopt               | 5.4.1                                                                                                                                                           |
| moon                   | moon 0.1.20260409 (a87440e 2026-04-09)                                                                                                                          |
| strip                  | GNU strip (GNU Binutils) 2.46.0                                                                                                                                 |
| sarifc                 | sarifc 0.1.0                                                                                                                                                    |

## Entries

| Entry                 | Compiler | Backend | Linkage | Stripped | Binary Size Sample (KiB) |
| --------------------- | -------- | ------- | ------- | -------- | ------------------------ |
| c (clang)             | clang    | native  | dynamic | yes      | 5.73                     |
| go (gc)               | go       | native  | static  | yes      | 1556.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 187.80                   |
| nim (clang)           | clang    | c       | dynamic | yes      | 26.08                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.36                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 329.48                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 8.80                     |

## Entry Policies

| Entry                 | Build Profile      | Low-Burden Optimizations                                                                                                                                                        |
| --------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| c (clang)             | native-lto-release | O3 plus LTO for whole-program release builds; native CPU tuning; frame-pointer omission and low-cost math errno cleanup; lld when available, otherwise toolchain default linker |
| go (gc)               | trimpath-release   | optimized default Go compiler pipeline; trimpath and buildvcs disabled for cleaner reproducible artifacts; linker stripping and empty buildid for lean release binaries         |
| moonbit (native)      | native-release     | native target release build; toolchain-managed stripping; frozen dependency graph for reproducible builds                                                                       |
| nim (clang)           | native-lto-danger  | danger mode plus speed optimization; ORC memory manager; C compiler native tuning with LTO; lld when available, otherwise toolchain default linker                              |
| ocaml (native)        | native-release     | native-code release build with unsafe and nodynlink; C backend native tuning flags passed through ccopt; separate stripping step after build                                    |
| rust (rustc/llvm)     | native-thin-lto    | target-cpu=native; thin LTO and single codegen unit; panic abort and symbol stripping for release binaries                                                                      |
| sarif (stage0/native) | stage0-native      | native executable emitted through sarifc build; stdout result mode for benchmark output parity; retained benchmark inputs declared in per-benchmark specs                       |

## Source Concision

| Entry                 | Benchmarks | Source Lines | Source Chars | Norm Lines | Norm Chars |
| --------------------- | ---------- | ------------ | ------------ | ---------- | ---------- |
| ocaml (native)        | 1          | 30           | 986          | 1.0000     | 1.0000     |
| nim (clang)           | 1          | 39           | 1103         | 0.7692     | 0.8939     |
| go (gc)               | 1          | 60           | 1201         | 0.5000     | 0.8210     |
| moonbit (native)      | 1          | 52           | 1401         | 0.5769     | 0.7038     |
| rust (rustc/llvm)     | 1          | 60           | 1465         | 0.5000     | 0.6730     |
| c (clang)             | 1          | 75           | 1894         | 0.4000     | 0.5206     |
| sarif (stage0/native) | 1          | 84           | 2322         | 0.3571     | 0.4246     |

## Benchmark Coverage

| Benchmark   | Category   | Base Wt | Effective Wt | Capabilities                                | Unique Coverage                             | Retained For                                                                                   |
| ----------- | ---------- | ------- | ------------ | ------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| binarytrees | Allocation | 1.00    | 1.0000       | allocation, pointer_chasing, tree_recursion | allocation, pointer_chasing, tree_recursion | Only benchmark centered on allocation-heavy pointer traversal and recursive tree construction. |

## Benchmarks

| Benchmark   | Algorithm                                       | Time           | Space            | Output Contract      | Fairness Notes                                                            |
| ----------- | ----------------------------------------------- | -------------- | ---------------- | -------------------- | ------------------------------------------------------------------------- |
| binarytrees | bottom-up binary tree construction and checksum | O(nodes built) | O(max tree size) | exact multiline text | Same tree/check workload; memory-management costs remain language-native. |

## Decision Profiles

| Profile      | Leader                | Runner-Up             | Third            | Intent                                                               |
| ------------ | --------------------- | --------------------- | ---------------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | ocaml (native)        | moonbit (native) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | ocaml (native)        | sarif (stage0/native) | moonbit (native) | Throughput or latency matters most.                                  |
| Memory First | sarif (stage0/native) | moonbit (native)      | ocaml (native)   | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang)             | ocaml (native)   | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | c (clang)             | ocaml (native)   | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Allocation | Overall |
| --------------------- | ---------- | ------- |
| sarif (stage0/native) | 1.0000     | 1.0000  |
| ocaml (native)        | 0.8885     | 0.8885  |
| moonbit (native)      | 0.8034     | 0.8034  |
| nim (clang)           | 0.5251     | 0.5251  |
| c (clang)             | 0.4942     | 0.4942  |
| go (gc)               | 0.3790     | 0.3790  |
| rust (rustc/llvm)     | 0.2571     | 0.2571  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 1.0000 | 0.9276 | 1.0000 | 1.0000 | 0.6510 |
| 2       | ocaml (native)        | 0.8885 | 1.0000 | 0.7610 | 0.2871 | 0.0057 |
| 3       | moonbit (native)      | 0.8034 | 0.8340 | 0.9971 | 0.0854 | 0.0305 |
| 4       | nim (clang)           | 0.5251 | 0.6165 | 0.3730 | 0.0490 | 0.2196 |
| 5       | c (clang)             | 0.4942 | 0.3268 | 0.7514 | 0.4965 | 1.0000 |
| 6       | go (gc)               | 0.3790 | 0.3205 | 0.7223 | 0.0159 | 0.0037 |
| 7       | rust (rustc/llvm)     | 0.2571 | 0.2488 | 0.3793 | 0.0206 | 0.0174 |

_Displayed scores use median runtime, equal category weighting with benchmark normalization inside each category, then scale each view so its leader is 1.0000. The composite ranks fixed-host production tradeoffs; use metric views and decision profiles for narrower decisions._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | ocaml (native)        | 1.0000      | 0.8885          |
| 2          | sarif (stage0/native) | 0.9276      | 1.0000          |
| 3          | moonbit (native)      | 0.8340      | 0.8034          |
| 4          | nim (clang)           | 0.6165      | 0.5251          |
| 5          | c (clang)             | 0.3268      | 0.4942          |
| 6          | go (gc)               | 0.3205      | 0.3790          |
| 7          | rust (rustc/llvm)     | 0.2488      | 0.2571          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 1.0000       | 1.0000          |
| 2           | moonbit (native)      | 0.9971       | 0.8034          |
| 3           | ocaml (native)        | 0.7610       | 0.8885          |
| 4           | c (clang)             | 0.7514       | 0.4942          |
| 5           | go (gc)               | 0.7223       | 0.3790          |
| 6           | rust (rustc/llvm)     | 0.3793       | 0.2571          |
| 7           | nim (clang)           | 0.3730       | 0.5251          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 1.0000          |
| 2          | c (clang)             | 0.4965      | 0.4942          |
| 3          | ocaml (native)        | 0.2871      | 0.8885          |
| 4          | moonbit (native)      | 0.0854      | 0.8034          |
| 5          | nim (clang)           | 0.0490      | 0.5251          |
| 6          | rust (rustc/llvm)     | 0.0206      | 0.2571          |
| 7          | go (gc)               | 0.0159      | 0.3790          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 1.0000     | 0.4942          |
| 2         | sarif (stage0/native) | 0.6510     | 1.0000          |
| 3         | nim (clang)           | 0.2196     | 0.5251          |
| 4         | moonbit (native)      | 0.0305     | 0.8034          |
| 5         | rust (rustc/llvm)     | 0.0174     | 0.2571          |
| 6         | ocaml (native)        | 0.0057     | 0.8885          |
| 7         | go (gc)               | 0.0037     | 0.3790          |

## Results

| Benchmark   | Entry                 | Input | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ----------- | --------------------- | ----- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees | c (clang)             | 20    | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1293         | 8.6209       | 130.06            | 5.73              | ok     |
| binarytrees | go (gc)               | 20    | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 4.0440         | 8.7906       | 135.31            | 1556.12           | ok     |
| binarytrees | moonbit (native)      | 20    | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.7521         | 3.3781       | 98.02             | 187.80            | ok     |
| binarytrees | nim (clang)           | 20    | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.3093         | 4.5700       | 262.02            | 26.08             | ok     |
| binarytrees | ocaml (native)        | 20    | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2236         | 2.8174       | 128.42            | 1006.36           | ok     |
| binarytrees | rust (rustc/llvm)     | 20    | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.1237         | 11.3240      | 257.70            | 329.48            | ok     |
| binarytrees | sarif (stage0/native) | 20    | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0642         | 3.0373       | 97.73             | 8.80              | ok     |
