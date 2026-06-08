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
| selected_benchmarks    | fasta                                                                                                                                                           |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 7                                                                                                                                                               |
| benchmarks             | 1                                                                                                                                                               |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.02                                                                                                                                                           |
| peak_memory_mode       | cgroupv2-memory.peak                                                                                                                                            |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-cosmic-com.system76.CosmicAppList-583438.scope/memory.peak                            |
| kernel                 | 7.0.10-35.stable                                                                                                                                                |
| gcc                    | gcc (AerynOS) 16.1.1 20260505                                                                                                                                   |
| clang                  | clang version 22.1.6 (AerynOS)                                                                                                                                  |
| go                     | go version go1.26.3 linux/amd64                                                                                                                                 |
| rustc                  | rustc 1.96.0 (ac68faa20 2026-05-25)                                                                                                                             |
| nim                    | Nim Compiler Version 2.2.10 [Linux: amd64]                                                                                                                      |
| ocamlopt               | 5.4.1                                                                                                                                                           |
| moon                   | moon 0.1.20260522 (4a0c52f 2026-05-22)                                                                                                                          |
| strip                  | GNU strip (GNU Binutils) 2.46.0                                                                                                                                 |
| sarifc                 | sarifc 0.1.0                                                                                                                                                    |

## Entries

| Entry                 | Compiler | Backend | Linkage | Stripped | Binary Size Sample (KiB) |
| --------------------- | -------- | ------- | ------- | -------- | ------------------------ |
| c (clang)             | clang    | native  | dynamic | yes      | 7.51                     |
| go (gc)               | go       | native  | static  | yes      | 1556.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 304.71                   |
| nim (clang)           | clang    | c       | dynamic | yes      | 27.66                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1015.55                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 332.72                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 11.01                    |

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
| nim (clang)           | 1          | 87           | 2480         | 0.9310     | 1.0000     |
| ocaml (native)        | 1          | 81           | 2503         | 1.0000     | 0.9908     |
| go (gc)               | 1          | 121          | 2600         | 0.6694     | 0.9538     |
| c (clang)             | 1          | 105          | 3165         | 0.7714     | 0.7836     |
| moonbit (native)      | 1          | 118          | 3406         | 0.6864     | 0.7281     |
| rust (rustc/llvm)     | 1          | 137          | 3549         | 0.5912     | 0.6988     |
| sarif (stage0/native) | 1          | 107          | 3968         | 0.7570     | 0.6250     |

## Benchmark Coverage

| Benchmark | Category       | Base Wt | Effective Wt | Capabilities                                   | Unique Coverage                                | Retained For                                                                                        |
| --------- | -------------- | ------- | ------------ | ---------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| fasta     | Text/Streaming | 0.75    | 1.0000       | text_generation, streaming_output, buffered_io | text_generation, streaming_output, buffered_io | Covers deterministic text generation and sustained buffered output, which parsing workloads do not. |

## Benchmarks

| Benchmark | Algorithm                                                  | Time | Space | Output Contract  | Fairness Notes                                                                          |
| --------- | ---------------------------------------------------------- | ---- | ----- | ---------------- | --------------------------------------------------------------------------------------- |
| fasta     | deterministic FASTA generation with buffered text emission | O(n) | O(1)  | exact FASTA text | Adds text generation and formatting without turning the suite into a library benchmark. |

## Decision Profiles

| Profile      | Leader                | Runner-Up             | Third                 | Intent                                                               |
| ------------ | --------------------- | --------------------- | --------------------- | -------------------------------------------------------------------- |
| Balanced     | c (clang)             | sarif (stage0/native) | nim (clang)           | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | c (clang)             | rust (rustc/llvm)     | Throughput or latency matters most.                                  |
| Memory First | c (clang)             | go (gc)               | sarif (stage0/native) | RAM pressure matters most.                                           |
| Build First  | c (clang)             | ocaml (native)        | sarif (stage0/native) | Build and iteration cost matter most.                                |
| Deploy First | c (clang)             | sarif (stage0/native) | nim (clang)           | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Text/Streaming | Overall |
| --------------------- | -------------- | ------- |
| c (clang)             | 0.9445         | 0.9445  |
| sarif (stage0/native) | 0.8295         | 0.8295  |
| nim (clang)           | 0.7285         | 0.7285  |
| rust (rustc/llvm)     | 0.7230         | 0.7230  |
| go (gc)               | 0.6788         | 0.6788  |
| ocaml (native)        | 0.5937         | 0.5937  |
| moonbit (native)      | 0.4365         | 0.4365  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | c (clang)             | 0.9445 | 0.9147 | 1.0000 | 1.0000 | 1.0000 |
| 2       | sarif (stage0/native) | 0.8295 | 1.0000 | 0.6026 | 0.2484 | 0.6820 |
| 3       | nim (clang)           | 0.7285 | 0.8817 | 0.6629 | 0.0919 | 0.2714 |
| 4       | rust (rustc/llvm)     | 0.7230 | 0.9133 | 0.6205 | 0.0411 | 0.0226 |
| 5       | go (gc)               | 0.6788 | 0.8035 | 0.7655 | 0.0319 | 0.0048 |
| 6       | ocaml (native)        | 0.5937 | 0.6262 | 0.6417 | 0.5794 | 0.0074 |
| 7       | moonbit (native)      | 0.4365 | 0.4246 | 0.7373 | 0.1174 | 0.0246 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.8295          |
| 2          | c (clang)             | 0.9147      | 0.9445          |
| 3          | rust (rustc/llvm)     | 0.9133      | 0.7230          |
| 4          | nim (clang)           | 0.8817      | 0.7285          |
| 5          | go (gc)               | 0.8035      | 0.6788          |
| 6          | ocaml (native)        | 0.6262      | 0.5937          |
| 7          | moonbit (native)      | 0.4246      | 0.4365          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | c (clang)             | 1.0000       | 0.9445          |
| 2           | go (gc)               | 0.7655       | 0.6788          |
| 3           | moonbit (native)      | 0.7373       | 0.4365          |
| 4           | nim (clang)           | 0.6629       | 0.7285          |
| 5           | ocaml (native)        | 0.6417       | 0.5937          |
| 6           | rust (rustc/llvm)     | 0.6205       | 0.7230          |
| 7           | sarif (stage0/native) | 0.6026       | 0.8295          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | c (clang)             | 1.0000      | 0.9445          |
| 2          | ocaml (native)        | 0.5794      | 0.5937          |
| 3          | sarif (stage0/native) | 0.2484      | 0.8295          |
| 4          | moonbit (native)      | 0.1174      | 0.4365          |
| 5          | nim (clang)           | 0.0919      | 0.7285          |
| 6          | rust (rustc/llvm)     | 0.0411      | 0.7230          |
| 7          | go (gc)               | 0.0319      | 0.6788          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 1.0000     | 0.9445          |
| 2         | sarif (stage0/native) | 0.6820     | 0.8295          |
| 3         | nim (clang)           | 0.2714     | 0.7285          |
| 4         | moonbit (native)      | 0.0246     | 0.4365          |
| 5         | rust (rustc/llvm)     | 0.0226     | 0.7230          |
| 6         | ocaml (native)        | 0.0074     | 0.5937          |
| 7         | go (gc)               | 0.0048     | 0.6788          |

## Results

| Benchmark | Entry                 | Input  | Output                  | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| --------- | --------------------- | ------ | ----------------------- | -------------- | ------------ | ----------------- | ----------------- | ------ |
| fasta     | c (clang)             | 250000 | sha256:dfd37a44ede2e23f | 0.1305         | 0.0378       | 47.70             | 7.51              | ok     |
| fasta     | go (gc)               | 250000 | sha256:dfd37a44ede2e23f | 4.0979         | 0.0430       | 62.32             | 1556.12           | ok     |
| fasta     | moonbit (native)      | 250000 | sha256:dfd37a44ede2e23f | 1.1116         | 0.0814       | 64.70             | 304.71            | ok     |
| fasta     | nim (clang)           | 250000 | sha256:dfd37a44ede2e23f | 1.4212         | 0.0392       | 71.96             | 27.66             | ok     |
| fasta     | ocaml (native)        | 250000 | sha256:dfd37a44ede2e23f | 0.2253         | 0.0552       | 74.34             | 1015.55           | ok     |
| fasta     | rust (rustc/llvm)     | 250000 | sha256:dfd37a44ede2e23f | 3.1794         | 0.0379       | 76.88             | 332.72            | ok     |
| fasta     | sarif (stage0/native) | 250000 | sha256:dfd37a44ede2e23f | 0.5255         | 0.0346       | 79.16             | 11.01             | ok     |
