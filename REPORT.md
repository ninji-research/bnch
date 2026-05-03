# Benchmark Report

## Environment

| Setting                | Value                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| objective              | Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking. |
| runs                   | 3                                                                                                                                                               |
| min_runs               | 2                                                                                                                                                               |
| warmup                 | 1                                                                                                                                                               |
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
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 8.89                     |

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

## Excluded

| Excluded From Score | Reason       |
| ------------------- | ------------ |
| binarytrees         | ok, run-fail |

## Decision Profiles

| Profile      | Leader                | Runner-Up         | Third             | Intent                                                               |
| ------------ | --------------------- | ----------------- | ----------------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | c (clang)         | rust (rustc/llvm) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | rust (rustc/llvm) | c (clang)         | Throughput or latency matters most.                                  |
| Memory First | sarif (stage0/native) | c (clang)         | go (gc)           | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang)         | go (gc)           | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | c (clang)         | go (gc)           | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Hash/String | Text/Streaming | Parse/Aggregate | Join/Aggregate | Sort/Aggregate | Overall |
| --------------------- | ------- | ----------- | -------------- | --------------- | -------------- | -------------- | ------- |
| sarif (stage0/native) | 0.8656  | 0.9892      | 0.7325         | 0.9784          | 0.9796         | 0.9798         | 0.9209  |
| c (clang)             | 0.9278  | 0.8618      | 0.9299         | 0.4930          | 0.6324         | 0.4790         | 0.7207  |
| rust (rustc/llvm)     | 0.8152  | 0.7650      | 0.6285         | 0.7760          | 0.5979         | 0.4651         | 0.6746  |
| go (gc)               | 0.7271  | 0.5128      | 0.5782         | 0.8519          | 0.5944         | 0.5623         | 0.6378  |
| nim (clang)           | 0.7843  | 0.6226      | 0.6273         | 0.4401          | 0.4225         | 0.3650         | 0.5436  |
| ocaml (native)        | 0.5944  | 0.3526      | 0.4787         | 0.3252          | 0.3531         | 0.2956         | 0.3999  |
| moonbit (native)      | 0.2695  | 0.2610      | 0.2417         | 0.2234          | 0.1410         | 0.2210         | 0.2263  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.9209 | 0.9154 | 0.9722 | 0.9575 | 0.7132 |
| 2       | c (clang)             | 0.7207 | 0.6660 | 1.0000 | 0.3837 | 0.9876 |
| 3       | rust (rustc/llvm)     | 0.6746 | 0.7358 | 0.9671 | 0.0186 | 0.0208 |
| 4       | go (gc)               | 0.6378 | 0.6208 | 0.9867 | 0.3665 | 0.0047 |
| 5       | nim (clang)           | 0.5436 | 0.5166 | 0.9581 | 0.0424 | 0.2395 |
| 6       | ocaml (native)        | 0.3999 | 0.2694 | 0.9684 | 0.3079 | 0.0073 |
| 7       | moonbit (native)      | 0.2263 | 0.0512 | 0.9167 | 0.0769 | 0.0398 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.9154      | 0.9209          |
| 2          | rust (rustc/llvm)     | 0.7358      | 0.6746          |
| 3          | c (clang)             | 0.6660      | 0.7207          |
| 4          | go (gc)               | 0.6208      | 0.6378          |
| 5          | nim (clang)           | 0.5166      | 0.5436          |
| 6          | ocaml (native)        | 0.2694      | 0.3999          |
| 7          | moonbit (native)      | 0.0512      | 0.2263          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | c (clang)             | 1.0000       | 0.7207          |
| 2           | go (gc)               | 0.9867       | 0.6378          |
| 3           | sarif (stage0/native) | 0.9722       | 0.9209          |
| 4           | ocaml (native)        | 0.9684       | 0.3999          |
| 5           | rust (rustc/llvm)     | 0.9671       | 0.6746          |
| 6           | nim (clang)           | 0.9581       | 0.5436          |
| 7           | moonbit (native)      | 0.9167       | 0.2263          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.9575      | 0.9209          |
| 2          | c (clang)             | 0.3837      | 0.7207          |
| 3          | go (gc)               | 0.3665      | 0.6378          |
| 4          | ocaml (native)        | 0.3079      | 0.3999          |
| 5          | moonbit (native)      | 0.0769      | 0.2263          |
| 6          | nim (clang)           | 0.0424      | 0.5436          |
| 7          | rust (rustc/llvm)     | 0.0186      | 0.6746          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 0.9876     | 0.7207          |
| 2         | sarif (stage0/native) | 0.7132     | 0.9209          |
| 3         | nim (clang)           | 0.2395     | 0.5436          |
| 4         | moonbit (native)      | 0.0398     | 0.2263          |
| 5         | rust (rustc/llvm)     | 0.0208     | 0.6746          |
| 6         | ocaml (native)        | 0.0073     | 0.3999          |
| 7         | go (gc)               | 0.0047     | 0.6378          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status   |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | -------- |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1001         | 7.9671       | 130.18            | 5.75              | ok       |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.5702         | 8.6297       | 133.30            | 1556.12           | ok       |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.6575         | 3.8336       | 97.98             | 187.83            | ok       |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.1620         | 4.8814       | 262.17            | 26.11             | ok       |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1796         | 2.5599       | 128.29            | 1006.39           | ok       |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.6422         | 9.7630       | 257.60            | 329.52            | ok       |
| binarytrees  | sarif (stage0/native) | 20                               | -                                                                        | 0.0431         | 0.0000       | 0.00              | 8.89              | run-fail |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.4046         | 0.0543       | 25.44             | 6.33              | ok       |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.4763         | 0.0194       | 25.44             | 1584.12           | ok       |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.6388         | 0.9969       | 25.44             | 174.68            | ok       |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.1163         | 0.0552       | 25.44             | 32.06             | ok       |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1951         | 0.1308       | 25.44             | 1010.17           | ok       |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.8638         | 0.0217       | 25.44             | 345.04            | ok       |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0584         | 0.0191       | 25.44             | 11.15             | ok       |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0921         | 0.0313       | 38.79             | 7.53              | ok       |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1082         | 0.0362       | 46.14             | 1552.12           | ok       |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.6077         | 0.2218       | 48.37             | 189.80            | ok       |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.0944         | 0.0330       | 48.50             | 27.71             | ok       |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1414         | 0.0475       | 53.40             | 1015.58           | ok       |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.2908         | 0.0315       | 55.74             | 332.44            | ok       |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1881         | 0.0276       | 58.20             | 8.73              | ok       |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1092         | 0.1115       | 28.18             | 8.05              | ok       |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1089         | 0.1079       | 28.18             | 1592.12           | ok       |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.6139         | 2.9734       | 47.04             | 200.77            | ok       |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.1593         | 0.1618       | 33.21             | 41.70             | ok       |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1474         | 0.2818       | 29.75             | 1010.55           | ok       |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 2.5238         | 0.0960       | 29.52             | 362.88            | ok       |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0375         | 0.0597       | 28.18             | 13.59             | ok       |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1189         | 0.0058       | 60.61             | 9.21              | ok       |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1074         | 0.0123       | 60.61             | 1580.12           | ok       |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.5979         | 0.0651       | 60.61             | 181.43            | ok       |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1264         | 0.0081       | 60.61             | 32.49             | ok       |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1511         | 0.0272       | 60.61             | 1065.61           | ok       |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.5135         | 0.0059       | 60.61             | 374.31            | ok       |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0470         | 0.0051       | 60.61             | 11.75             | ok       |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0876         | 0.0141       | 60.61             | 5.86              | ok       |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.0993         | 0.0190       | 60.61             | 1548.12           | ok       |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.5863         | 0.0943       | 60.61             | 187.33            | ok       |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.0872         | 0.0143       | 60.61             | 23.90             | ok       |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1378         | 0.0172       | 60.61             | 1005.33           | ok       |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.3268         | 0.0159       | 60.61             | 329.77            | ok       |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0342         | 0.0163       | 60.61             | 5.63              | ok       |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1113         | 0.1967       | 60.61             | 8.55              | ok       |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1056         | 0.3224       | 60.61             | 1560.12           | ok       |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.5899         | 3.1201       | 60.61             | 194.40            | ok       |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.0820         | 0.2773       | 60.61             | 27.73             | ok       |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1421         | 0.3370       | 60.61             | 1006.52           | ok       |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.4651         | 0.1930       | 60.61             | 356.35            | ok       |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0431         | 0.3164       | 60.61             | 13.45             | ok       |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0937         | 0.0014       | 60.61             | 6.72              | ok       |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0991         | 0.0052       | 60.61             | 1468.12           | ok       |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.5781         | 0.0519       | 60.61             | 169.93            | ok       |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.9805         | 0.0028       | 60.61             | 25.79             | ok       |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1357         | 0.0062       | 60.61             | 774.77            | ok       |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.3353         | 0.0026       | 60.61             | 332.72            | ok       |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0338         | 0.0036       | 60.61             | 7.82              | ok       |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0859         | 0.0728       | 60.61             | 5.99              | ok       |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1042         | 0.0420       | 60.61             | 1576.12           | ok       |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.5820         | 1.0185       | 60.61             | 173.37            | ok       |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0308         | 0.0919       | 60.61             | 27.80             | ok       |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1361         | 0.1952       | 60.61             | 1005.48           | ok       |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.4666         | 0.0528       | 60.61             | 340.98            | ok       |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0330         | 0.0213       | 60.61             | 10.05             | ok       |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1499         | 1.1283       | 60.61             | 9.04              | ok       |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1098         | 1.2319       | 60.61             | 1556.12           | ok       |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.5828         | 16.2195      | 60.61             | 191.59            | ok       |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.0844         | 1.2067       | 60.61             | 24.55             | ok       |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1349         | 3.8582       | 60.61             | 1010.02           | ok       |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.3199         | 1.1970       | 60.61             | 357.46            | ok       |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0431         | 1.2086       | 60.61             | 7.38              | ok       |

## Mismatches

| Benchmark   | Entry                 | Output | Reference                                                                | Status   |
| ----------- | --------------------- | ------ | ------------------------------------------------------------------------ | -------- |
| binarytrees | sarif (stage0/native) | -      | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | run-fail |
