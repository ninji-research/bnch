# Benchmark Report

## Environment

| Setting                | Value                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| objective              | Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking. |
| runs                   | 1                                                                                                                                                               |
| min_runs               | 1                                                                                                                                                               |
| warmup                 | 1                                                                                                                                                               |
| runtime_target_s       | 0.35                                                                                                                                                            |
| max_relative_spread    | 0.03                                                                                                                                                            |
| build_jobs             | 16                                                                                                                                                              |
| canonical_entries_only | yes                                                                                                                                                             |
| experimental_entries   | no                                                                                                                                                              |
| selected_benchmarks    | csvgroupby,mandelbrot,knucleotide                                                                                                                               |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 7                                                                                                                                                               |
| benchmarks             | 3                                                                                                                                                               |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.02                                                                                                                                                           |
| peak_memory_mode       | ru_maxrss                                                                                                                                                       |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/session-3.scope/memory.peak unavailable for reset (Permission denied)                                                 |
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
| c (clang)             | clang    | native  | dynamic | yes      | 6.30                     |
| go (gc)               | go       | native  | static  | yes      | 1584.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 301.22                   |
| nim (clang)           | clang    | c       | dynamic | yes      | 31.62                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1010.14                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 345.23                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 13.81                    |

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
| nim (clang)           | 3          | 162          | 4048         | 1.0000     | 1.0000     |
| go (gc)               | 3          | 243          | 4447         | 0.6667     | 0.9103     |
| rust (rustc/llvm)     | 3          | 195          | 5200         | 0.8308     | 0.7785     |
| ocaml (native)        | 3          | 200          | 5557         | 0.8100     | 0.7285     |
| c (clang)             | 3          | 303          | 7683         | 0.5347     | 0.5269     |
| moonbit (native)      | 3          | 378          | 8906         | 0.4286     | 0.4545     |
| sarif (stage0/native) | 3          | 296          | 10475        | 0.5473     | 0.3864     |

## Benchmark Coverage

| Benchmark   | Category        | Base Wt | Effective Wt | Capabilities                                          | Unique Coverage                          | Retained For                                                                                                          |
| ----------- | --------------- | ------- | ------------ | ----------------------------------------------------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| csvgroupby  | Parse/Aggregate | 1.00    | 0.3333       | csv_parsing, aggregation, sorting                     | csv_parsing, sorting                     | Anchors real structured-text parsing plus aggregation with lighter state than the join workload.                      |
| mandelbrot  | Numeric         | 1.00    | 0.3333       | numeric_compute, tight_loops, branching               | numeric_compute, tight_loops, branching  | Represents scalar numeric compute with tight loop and branch behavior distinct from floating-point iterative kernels. |
| knucleotide | Hash/String     | 1.00    | 0.3333       | text_parsing, hashing, string_processing, aggregation | text_parsing, hashing, string_processing | Primary hash-heavy and string-heavy benchmark; no other workload stresses this mix as directly.                       |

## Benchmarks

| Benchmark   | Algorithm                                                  | Time             | Space                    | Output Contract        | Fairness Notes                                                                                     |
| ----------- | ---------------------------------------------------------- | ---------------- | ------------------------ | ---------------------- | -------------------------------------------------------------------------------------------------- |
| csvgroupby  | CSV parse plus per-customer group-by aggregation           | O(n log k)       | O(k)                     | exact CSV summary text | Uses a committed deterministic CSV fixture with clean unquoted fields and sorted aggregate output. |
| mandelbrot  | scalar Mandelbrot escape-time bitmap checksum              | O(size^2 * iter) | O(1)                     | exact integer checksum | Input size is set to 512 because all retained implementations agree there exactly.                 |
| knucleotide | FASTA parsing plus k-mer frequency and occurrence counting | O(n)             | O(unique k-mers + input) | exact multiline text   | Uses one committed deterministic FASTA fixture and processes only the >THREE section.              |

## Excluded

| Excluded From Score | Reason         |
| ------------------- | -------------- |
| knucleotide         | build-fail, ok |

## Decision Profiles

| Profile      | Leader                | Runner-Up | Third             | Intent                                                               |
| ------------ | --------------------- | --------- | ----------------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | go (gc)   | rust (rustc/llvm) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | go (gc)   | rust (rustc/llvm) | Throughput or latency matters most.                                  |
| Memory First | sarif (stage0/native) | c (clang) | go (gc)           | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang) | go (gc)           | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | c (clang) | go (gc)           | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Parse/Aggregate | Overall |
| --------------------- | ------- | --------------- | ------- |
| sarif (stage0/native) | 0.9077  | 0.9481          | 0.9279  |
| go (gc)               | 0.7667  | 0.7589          | 0.7628  |
| rust (rustc/llvm)     | 0.8286  | 0.6396          | 0.7341  |
| c (clang)             | 0.8880  | 0.4875          | 0.6878  |
| nim (clang)           | 0.8647  | 0.3385          | 0.6016  |
| moonbit (native)      | 0.8121  | 0.2404          | 0.5262  |
| ocaml (native)        | 0.7300  | 0.2953          | 0.5127  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.9279 | 0.9362 | 0.9382 | 1.0000 | 0.6355 |
| 2       | go (gc)               | 0.7628 | 0.8417 | 1.0000 | 0.1553 | 0.0039 |
| 3       | rust (rustc/llvm)     | 0.7341 | 0.8183 | 1.0000 | 0.0131 | 0.0180 |
| 4       | c (clang)             | 0.6878 | 0.6324 | 1.0000 | 0.2672 | 1.0000 |
| 5       | nim (clang)           | 0.6016 | 0.5961 | 1.0000 | 0.0303 | 0.2224 |
| 6       | moonbit (native)      | 0.5262 | 0.4939 | 1.0000 | 0.0416 | 0.0202 |
| 7       | ocaml (native)        | 0.5127 | 0.4467 | 1.0000 | 0.2199 | 0.0060 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.9362      | 0.9279          |
| 2          | go (gc)               | 0.8417      | 0.7628          |
| 3          | rust (rustc/llvm)     | 0.8183      | 0.7341          |
| 4          | c (clang)             | 0.6324      | 0.6878          |
| 5          | nim (clang)           | 0.5961      | 0.6016          |
| 6          | moonbit (native)      | 0.4939      | 0.5262          |
| 7          | ocaml (native)        | 0.4467      | 0.5127          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | nim (clang)           | 1.0000       | 0.6016          |
| 1           | go (gc)               | 1.0000       | 0.7628          |
| 1           | moonbit (native)      | 1.0000       | 0.5262          |
| 1           | c (clang)             | 1.0000       | 0.6878          |
| 1           | rust (rustc/llvm)     | 1.0000       | 0.7341          |
| 1           | ocaml (native)        | 1.0000       | 0.5127          |
| 7           | sarif (stage0/native) | 0.9382       | 0.9279          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.9279          |
| 2          | c (clang)             | 0.2672      | 0.6878          |
| 3          | ocaml (native)        | 0.2199      | 0.5127          |
| 4          | go (gc)               | 0.1553      | 0.7628          |
| 5          | moonbit (native)      | 0.0416      | 0.5262          |
| 6          | nim (clang)           | 0.0303      | 0.6016          |
| 7          | rust (rustc/llvm)     | 0.0131      | 0.7341          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 1.0000     | 0.6878          |
| 2         | sarif (stage0/native) | 0.6355     | 0.9279          |
| 3         | nim (clang)           | 0.2224     | 0.6016          |
| 4         | moonbit (native)      | 0.0202     | 0.5262          |
| 5         | rust (rustc/llvm)     | 0.0180     | 0.7341          |
| 6         | ocaml (native)        | 0.0060     | 0.5127          |
| 7         | go (gc)               | 0.0039     | 0.7628          |

## Results

| Benchmark   | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status     |
| ----------- | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ---------- |
| csvgroupby  | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.3695         | 0.0675       | 38.17             | 6.30              | ok         |
| csvgroupby  | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 5.6194         | 0.0266       | 38.17             | 1584.12           | ok         |
| csvgroupby  | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.2608         | 0.4337       | 38.17             | 301.22            | ok         |
| csvgroupby  | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.7680         | 0.1189       | 38.17             | 31.62             | ok         |
| csvgroupby  | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2682         | 0.2088       | 38.17             | 1010.14           | ok         |
| csvgroupby  | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 4.2202         | 0.0340       | 38.17             | 345.23            | ok         |
| csvgroupby  | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0641         | 0.0229       | 43.55             | 13.81             | ok         |
| knucleotide | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1680         | 0.0087       | 43.55             | 9.19              | ok         |
| knucleotide | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1585         | 0.0161       | 43.55             | 1580.12           | ok         |
| knucleotide | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.3275         | 0.0269       | 43.55             | 306.09            | ok         |
| knucleotide | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.7762         | 0.0111       | 43.55             | 32.46             | ok         |
| knucleotide | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.2135         | 0.0414       | 43.55             | 1065.58           | ok         |
| knucleotide | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 3.9977         | 0.0080       | 43.55             | 374.44            | ok         |
| knucleotide | sarif (stage0/native) | fixture:knucleotide-250000.fasta | -                                                                        | 0.0483         | 0.0000       | 0.00              | 0.00              | build-fail |
| mandelbrot  | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.1117         | 0.0217       | 43.55             | 5.84              | ok         |
| mandelbrot  | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1348         | 0.0244       | 43.55             | 1548.12           | ok         |
| mandelbrot  | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 1.2441         | 0.0215       | 43.55             | 300.24            | ok         |
| mandelbrot  | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.6527         | 0.0201       | 43.55             | 23.77             | ok         |
| mandelbrot  | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.2007         | 0.0256       | 43.55             | 1005.30           | ok         |
| mandelbrot  | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 3.6781         | 0.0209       | 43.55             | 330.03            | ok         |
| mandelbrot  | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0403         | 0.0230       | 43.55             | 7.16              | ok         |

## Mismatches

| Benchmark   | Entry                 | Output | Reference                                                                | Status     |
| ----------- | --------------------- | ------ | ------------------------------------------------------------------------ | ---------- |
| knucleotide | sarif (stage0/native) | -      | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | build-fail |
