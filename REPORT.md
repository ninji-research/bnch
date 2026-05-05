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
| selected_benchmarks    | binarytrees,csvgroupby,joinagg,fasta,mandelbrot,spectralnorm,nbody,knucleotide,revcomp,sortuniq                                                                 |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 7                                                                                                                                                               |
| benchmarks             | 10                                                                                                                                                              |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.02                                                                                                                                                           |
| peak_memory_mode       | ru_maxrss                                                                                                                                                       |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/session-3.scope/memory.peak unavailable for reset (Permission denied)                                                 |
| kernel                 | 7.0.3-6.stable                                                                                                                                                  |
| gcc                    | gcc (AerynOS) 15.2.1 20260421                                                                                                                                   |
| clang                  | clang version 22.1.4 (AerynOS)                                                                                                                                  |
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
| c (clang)             | clang    | native  | dynamic | yes      | 5.75                     |
| go (gc)               | go       | native  | static  | yes      | 1556.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 187.83                   |
| nim (clang)           | clang    | c       | dynamic | yes      | 26.11                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.39                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 329.52                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 9.02                     |

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
| nim (clang)           | 10         | 560          | 15821        | 1.0000     | 1.0000     |
| go (gc)               | 10         | 846          | 17701        | 0.6619     | 0.8938     |
| ocaml (native)        | 10         | 628          | 18714        | 0.8917     | 0.8454     |
| rust (rustc/llvm)     | 10         | 789          | 21904        | 0.7098     | 0.7223     |
| c (clang)             | 10         | 1052         | 28478        | 0.5323     | 0.5556     |
| moonbit (native)      | 10         | 1212         | 30708        | 0.4620     | 0.5152     |
| sarif (stage0/native) | 10         | 947          | 34869        | 0.5913     | 0.4537     |

## Benchmark Coverage

| Benchmark    | Category        | Base Wt | Effective Wt | Capabilities                                          | Unique Coverage                             | Retained For                                                                                                          |
| ------------ | --------------- | ------- | ------------ | ----------------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| binarytrees  | Allocation      | 1.00    | 0.1429       | allocation, pointer_chasing, tree_recursion           | allocation, pointer_chasing, tree_recursion | Only benchmark centered on allocation-heavy pointer traversal and recursive tree construction.                        |
| csvgroupby   | Parse/Aggregate | 1.00    | 0.1429       | csv_parsing, aggregation, sorting                     | csv_parsing                                 | Anchors real structured-text parsing plus aggregation with lighter state than the join workload.                      |
| joinagg      | Join/Aggregate  | 1.00    | 0.1429       | parsing, join_processing, aggregation, sorting        | parsing, join_processing                    | Only retained workload that exercises join logic, multi-table data shaping, and ordered aggregation together.         |
| fasta        | Text/Streaming  | 0.75    | 0.0714       | text_generation, streaming_output, buffered_io        | text_generation, streaming_output           | Covers deterministic text generation and sustained buffered output, which parsing workloads do not.                   |
| mandelbrot   | Numeric         | 1.00    | 0.0476       | numeric_compute, tight_loops, branching               | tight_loops, branching                      | Represents scalar numeric compute with tight loop and branch behavior distinct from floating-point iterative kernels. |
| spectralnorm | Numeric         | 1.00    | 0.0476       | numeric_compute, floating_point, vector_iteration     | vector_iteration                            | Adds floating-point iterative linear-algebra style work with stable numeric comparison rules.                         |
| nbody        | Numeric         | 1.00    | 0.0476       | numeric_compute, floating_point, simulation           | simulation                                  | Only retained simulation-style kernel, preserving long-running floating-point update behavior.                        |
| knucleotide  | Hash/String     | 1.00    | 0.1429       | text_parsing, hashing, string_processing, aggregation | hashing                                     | Primary hash-heavy and string-heavy benchmark; no other workload stresses this mix as directly.                       |
| revcomp      | Text/Streaming  | 0.75    | 0.0714       | text_parsing, streaming_transform, buffered_io        | streaming_transform                         | Keeps a transformation-oriented streaming workload in the suite instead of only generators and aggregators.           |
| sortuniq     | Sort/Aggregate  | 1.00    | 0.1429       | sorting, aggregation, string_processing               | -                                           | Captures global ordering cost and frequency aggregation without parser-heavy setup or join complexity.                |

## Benchmarks

| Benchmark    | Algorithm                                                                    | Time                     | Space                    | Output Contract                        | Fairness Notes                                                                                                                                                         |
| ------------ | ---------------------------------------------------------------------------- | ------------------------ | ------------------------ | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| binarytrees  | bottom-up binary tree construction and checksum                              | O(nodes built)           | O(max tree size)         | exact multiline text                   | Same tree/check workload; memory-management costs remain language-native.                                                                                              |
| csvgroupby   | CSV parse plus per-customer group-by aggregation                             | O(n log k)               | O(k)                     | exact CSV summary text                 | Uses a committed deterministic CSV fixture with clean unquoted fields and sorted aggregate output.                                                                     |
| joinagg      | sectioned CSV parse plus active-user sort-merge join and ordered aggregation | O((u + e) log (u + e))   | O(u + e)                 | exact region,tier aggregate text       | Uses one deterministic two-section fixture, keeps the join key and aggregate contract fixed, and adds a realistic relational join workload without external libraries. |
| fasta        | deterministic FASTA generation with buffered text emission                   | O(n)                     | O(1)                     | exact FASTA text                       | Adds text generation and formatting without turning the suite into a library benchmark.                                                                                |
| mandelbrot   | scalar Mandelbrot escape-time bitmap checksum                                | O(size^2 * iter)         | O(1)                     | exact integer checksum                 | Input size is set to 512 because all retained implementations agree there exactly.                                                                                     |
| spectralnorm | power method on implicit matrix                                              | O(n^2 * iterations)      | O(n)                     | one float rounded to 9 decimals        | Correctness compares canonical 9-decimal output, not raw printer differences.                                                                                          |
| nbody        | 5-body symplectic advance and energy                                         | O(iterations * bodies^2) | O(1)                     | two floats rounded to 9 decimals       | Correctness compares canonical 9-decimal energies line-by-line.                                                                                                        |
| knucleotide  | FASTA parsing plus k-mer frequency and occurrence counting                   | O(n)                     | O(unique k-mers + input) | exact multiline text                   | Uses one committed deterministic FASTA fixture and processes only the >THREE section.                                                                                  |
| revcomp      | FASTA parsing plus reverse-complement text transformation                    | O(n)                     | O(n)                     | FASTA text with case-insensitive bases | Adds streaming-style text transformation and output reshaping with the same committed fixture family.                                                                  |
| sortuniq     | line-oriented string sort and duplicate-count aggregation                    | O(n log n)               | O(n)                     | exact word,count text                  | Uses one committed deterministic newline-word fixture, includes empty-line noise, and rewards lean sort-plus-aggregation implementations.                              |

## Decision Profiles

| Profile      | Leader                | Runner-Up | Third             | Intent                                                               |
| ------------ | --------------------- | --------- | ----------------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | c (clang) | rust (rustc/llvm) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | c (clang) | rust (rustc/llvm) | Throughput or latency matters most.                                  |
| Memory First | sarif (stage0/native) | c (clang) | go (gc)           | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang) | ocaml (native)    | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | c (clang) | nim (clang)       | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Allocation | Hash/String | Text/Streaming | Parse/Aggregate | Join/Aggregate | Sort/Aggregate | Overall |
| --------------------- | ------- | ---------- | ----------- | -------------- | --------------- | -------------- | -------------- | ------- |
| sarif (stage0/native) | 0.8668  | 0.9019     | 0.9890      | 0.7595         | 0.9783          | 0.9795         | 0.9797         | 0.9221  |
| c (clang)             | 0.8998  | 0.3959     | 0.8479      | 0.8731         | 0.5651          | 0.6524         | 0.4775         | 0.6731  |
| rust (rustc/llvm)     | 0.7882  | 0.2216     | 0.6821      | 0.6382         | 0.7455          | 0.6822         | 0.4002         | 0.5940  |
| go (gc)               | 0.7090  | 0.3168     | 0.4638      | 0.5527         | 0.7845          | 0.5671         | 0.5584         | 0.5646  |
| nim (clang)           | 0.7745  | 0.4132     | 0.5412      | 0.6536         | 0.4286          | 0.5002         | 0.3686         | 0.5257  |
| ocaml (native)        | 0.5895  | 0.8257     | 0.3510      | 0.4563         | 0.3199          | 0.3663         | 0.2949         | 0.4577  |
| moonbit (native)      | 0.2680  | 0.6135     | 0.2583      | 0.2375         | 0.2189          | 0.1477         | 0.2197         | 0.2805  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.9221 | 0.9111 | 0.9743 | 1.0000 | 0.7005 |
| 2       | c (clang)             | 0.6731 | 0.6095 | 0.9642 | 0.3462 | 0.9894 |
| 3       | rust (rustc/llvm)     | 0.5940 | 0.6378 | 0.8842 | 0.0157 | 0.0203 |
| 4       | go (gc)               | 0.5646 | 0.5443 | 0.9520 | 0.2018 | 0.0045 |
| 5       | nim (clang)           | 0.5257 | 0.5127 | 0.8848 | 0.0366 | 0.2367 |
| 6       | ocaml (native)        | 0.4577 | 0.3767 | 0.9415 | 0.2415 | 0.0071 |
| 7       | moonbit (native)      | 0.2805 | 0.1323 | 0.9325 | 0.0613 | 0.0385 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.9111      | 0.9221          |
| 2          | rust (rustc/llvm)     | 0.6378      | 0.5940          |
| 3          | c (clang)             | 0.6095      | 0.6731          |
| 4          | go (gc)               | 0.5443      | 0.5646          |
| 5          | nim (clang)           | 0.5127      | 0.5257          |
| 6          | ocaml (native)        | 0.3767      | 0.4577          |
| 7          | moonbit (native)      | 0.1323      | 0.2805          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 0.9743       | 0.9221          |
| 2           | c (clang)             | 0.9642       | 0.6731          |
| 3           | go (gc)               | 0.9520       | 0.5646          |
| 4           | ocaml (native)        | 0.9415       | 0.4577          |
| 5           | moonbit (native)      | 0.9325       | 0.2805          |
| 6           | nim (clang)           | 0.8848       | 0.5257          |
| 7           | rust (rustc/llvm)     | 0.8842       | 0.5940          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.9221          |
| 2          | c (clang)             | 0.3462      | 0.6731          |
| 3          | ocaml (native)        | 0.2415      | 0.4577          |
| 4          | go (gc)               | 0.2018      | 0.5646          |
| 5          | moonbit (native)      | 0.0613      | 0.2805          |
| 6          | nim (clang)           | 0.0366      | 0.5257          |
| 7          | rust (rustc/llvm)     | 0.0157      | 0.5940          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 0.9894     | 0.6731          |
| 2         | sarif (stage0/native) | 0.7005     | 0.9221          |
| 3         | nim (clang)           | 0.2367     | 0.5257          |
| 4         | moonbit (native)      | 0.0385     | 0.2805          |
| 5         | rust (rustc/llvm)     | 0.0203     | 0.5940          |
| 6         | ocaml (native)        | 0.0071     | 0.4577          |
| 7         | go (gc)               | 0.0045     | 0.5646          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1790         | 9.0770       | 130.09            | 5.75              | ok     |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 4.1793         | 8.7523       | 134.15            | 1556.12           | ok     |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.8672         | 3.6635       | 97.77             | 187.83            | ok     |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.1594         | 4.6060       | 261.95            | 26.11             | ok     |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2458         | 2.2877       | 128.27            | 1006.39           | ok     |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.7917         | 10.3896      | 257.99            | 329.52            | ok     |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0576         | 2.6086       | 97.47             | 9.02              | ok     |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1026         | 0.0410       | 27.24             | 6.33              | ok     |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.4063         | 0.0202       | 27.24             | 1584.12           | ok     |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.5901         | 0.9838       | 27.24             | 174.68            | ok     |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.1553         | 0.0540       | 27.24             | 32.06             | ok     |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1909         | 0.1129       | 27.24             | 1010.17           | ok     |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.6220         | 0.0215       | 27.24             | 345.04            | ok     |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0311         | 0.0179       | 27.24             | 11.20             | ok     |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1004         | 0.0312       | 28.76             | 7.53              | ok     |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1247         | 0.0350       | 32.89             | 1552.12           | ok     |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.6213         | 0.2260       | 35.25             | 189.80            | ok     |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.1575         | 0.0313       | 37.66             | 27.71             | ok     |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1465         | 0.0483       | 40.08             | 1015.58           | ok     |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.4493         | 0.0299       | 42.50             | 332.44            | ok     |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0363         | 0.0249       | 44.93             | 8.78              | ok     |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1257         | 0.1155       | 28.76             | 8.05              | ok     |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1203         | 0.1282       | 28.76             | 1592.12           | ok     |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.6782         | 2.7190       | 46.21             | 200.77            | ok     |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.1799         | 0.1440       | 30.61             | 41.70             | ok     |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1432         | 0.2951       | 29.59             | 1010.55           | ok     |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 2.7353         | 0.0889       | 29.55             | 362.88            | ok     |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0363         | 0.0664       | 28.76             | 13.63             | ok     |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1290         | 0.0054       | 47.41             | 9.21              | ok     |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1906         | 0.0127       | 47.41             | 1580.12           | ok     |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.6293         | 0.0630       | 47.41             | 181.43            | ok     |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1411         | 0.0093       | 47.41             | 32.49             | ok     |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1900         | 0.0242       | 47.41             | 1065.61           | ok     |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.5164         | 0.0063       | 47.41             | 374.31            | ok     |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0501         | 0.0046       | 47.41             | 11.80             | ok     |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0787         | 0.0136       | 47.41             | 5.86              | ok     |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1549         | 0.0184       | 47.41             | 1548.12           | ok     |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.5995         | 0.0940       | 47.41             | 187.33            | ok     |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.1319         | 0.0139       | 47.41             | 23.90             | ok     |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1460         | 0.0174       | 47.41             | 1005.33           | ok     |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.7494         | 0.0188       | 47.41             | 329.77            | ok     |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0427         | 0.0173       | 47.41             | 5.63              | ok     |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1551         | 0.2131       | 47.41             | 8.55              | ok     |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1945         | 0.3443       | 47.41             | 1560.12           | ok     |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.7920         | 3.0437       | 47.41             | 194.40            | ok     |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.2148         | 0.2999       | 47.41             | 27.73             | ok     |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1525         | 0.3198       | 47.41             | 1006.52           | ok     |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.7727         | 0.1873       | 47.41             | 356.35            | ok     |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0480         | 0.2975       | 47.41             | 13.45             | ok     |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0988         | 0.0017       | 47.41             | 6.72              | ok     |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1506         | 0.0053       | 47.41             | 1468.12           | ok     |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.5474         | 0.0487       | 47.41             | 169.93            | ok     |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.9511         | 0.0028       | 47.41             | 25.79             | ok     |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1261         | 0.0064       | 47.41             | 774.77            | ok     |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.3866         | 0.0028       | 47.41             | 332.72            | ok     |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0404         | 0.0044       | 47.41             | 7.84              | ok     |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0810         | 0.0717       | 47.41             | 5.99              | ok     |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1407         | 0.0404       | 47.41             | 1576.12           | ok     |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.6672         | 1.0152       | 47.41             | 173.37            | ok     |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0347         | 0.0878       | 47.41             | 27.80             | ok     |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1499         | 0.1835       | 47.41             | 1005.48           | ok     |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.5069         | 0.0687       | 47.41             | 340.98            | ok     |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0307         | 0.0209       | 47.41             | 10.09             | ok     |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1818         | 1.2036       | 47.41             | 9.04              | ok     |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1567         | 1.2341       | 47.41             | 1556.12           | ok     |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.6503         | 16.8415      | 47.41             | 191.59            | ok     |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.0915         | 1.2119       | 47.41             | 24.55             | ok     |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1572         | 3.9444       | 47.41             | 1010.02           | ok     |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.5506         | 1.1933       | 47.41             | 357.46            | ok     |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0402         | 1.1698       | 47.41             | 7.38              | ok     |
