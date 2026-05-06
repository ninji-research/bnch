# Benchmark Report

## Environment

| Setting                | Value                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| objective              | Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking. |
| runs                   | 3                                                                                                                                                               |
| min_runs               | 3                                                                                                                                                               |
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

| Profile      | Leader                | Runner-Up         | Third             | Intent                                                               |
| ------------ | --------------------- | ----------------- | ----------------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | c (clang)         | rust (rustc/llvm) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | rust (rustc/llvm) | c (clang)         | Throughput or latency matters most.                                  |
| Memory First | sarif (stage0/native) | c (clang)         | go (gc)           | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang)         | go (gc)           | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | c (clang)         | nim (clang)       | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Allocation | Hash/String | Text/Streaming | Parse/Aggregate | Join/Aggregate | Sort/Aggregate | Overall |
| --------------------- | ------- | ---------- | ----------- | -------------- | --------------- | -------------- | -------------- | ------- |
| sarif (stage0/native) | 0.8542  | 0.9415     | 0.9890      | 0.7633         | 0.9783          | 0.9795         | 0.9797         | 0.9265  |
| c (clang)             | 0.9250  | 0.4469     | 0.8140      | 0.8892         | 0.5508          | 0.6394         | 0.4960         | 0.6802  |
| rust (rustc/llvm)     | 0.8174  | 0.2451     | 0.7601      | 0.6327         | 0.7694          | 0.6042         | 0.4517         | 0.6115  |
| go (gc)               | 0.7139  | 0.3392     | 0.4956      | 0.5442         | 0.8338          | 0.5743         | 0.5681         | 0.5813  |
| nim (clang)           | 0.7813  | 0.4382     | 0.5711      | 0.6310         | 0.4421          | 0.4628         | 0.3885         | 0.5307  |
| ocaml (native)        | 0.5712  | 0.8227     | 0.3396      | 0.4580         | 0.3148          | 0.3648         | 0.3039         | 0.4536  |
| moonbit (native)      | 0.2646  | 0.6672     | 0.2567      | 0.2339         | 0.2196          | 0.2064         | 0.2216         | 0.2957  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.9265 | 0.9164 | 0.9789 | 1.0000 | 0.7005 |
| 2       | c (clang)             | 0.6802 | 0.6165 | 0.9643 | 0.3716 | 0.9894 |
| 3       | rust (rustc/llvm)     | 0.6115 | 0.6628 | 0.8918 | 0.0135 | 0.0203 |
| 4       | go (gc)               | 0.5813 | 0.5624 | 0.9524 | 0.2506 | 0.0045 |
| 5       | nim (clang)           | 0.5307 | 0.5184 | 0.8947 | 0.0301 | 0.2367 |
| 6       | ocaml (native)        | 0.4536 | 0.3697 | 0.9481 | 0.2329 | 0.0071 |
| 7       | moonbit (native)      | 0.2957 | 0.1433 | 0.9753 | 0.0558 | 0.0385 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.9164      | 0.9265          |
| 2          | rust (rustc/llvm)     | 0.6628      | 0.6115          |
| 3          | c (clang)             | 0.6165      | 0.6802          |
| 4          | go (gc)               | 0.5624      | 0.5813          |
| 5          | nim (clang)           | 0.5184      | 0.5307          |
| 6          | ocaml (native)        | 0.3697      | 0.4536          |
| 7          | moonbit (native)      | 0.1433      | 0.2957          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 0.9789       | 0.9265          |
| 2           | moonbit (native)      | 0.9753       | 0.2957          |
| 3           | c (clang)             | 0.9643       | 0.6802          |
| 4           | go (gc)               | 0.9524       | 0.5813          |
| 5           | ocaml (native)        | 0.9481       | 0.4536          |
| 6           | nim (clang)           | 0.8947       | 0.5307          |
| 7           | rust (rustc/llvm)     | 0.8918       | 0.6115          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.9265          |
| 2          | c (clang)             | 0.3716      | 0.6802          |
| 3          | go (gc)               | 0.2506      | 0.5813          |
| 4          | ocaml (native)        | 0.2329      | 0.4536          |
| 5          | moonbit (native)      | 0.0558      | 0.2957          |
| 6          | nim (clang)           | 0.0301      | 0.5307          |
| 7          | rust (rustc/llvm)     | 0.0135      | 0.6115          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 0.9894     | 0.6802          |
| 2         | sarif (stage0/native) | 0.7005     | 0.9265          |
| 3         | nim (clang)           | 0.2367     | 0.5307          |
| 4         | moonbit (native)      | 0.0385     | 0.2957          |
| 5         | rust (rustc/llvm)     | 0.0203     | 0.6115          |
| 6         | ocaml (native)        | 0.0071     | 0.4536          |
| 7         | go (gc)               | 0.0045     | 0.5813          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0793         | 8.7004       | 130.17            | 5.75              | ok     |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.5058         | 9.3321       | 134.09            | 1556.12           | ok     |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.6359         | 3.8966       | 97.89             | 187.83            | ok     |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.1856         | 5.1348       | 262.14            | 26.11             | ok     |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1566         | 2.7648       | 128.43            | 1006.39           | ok     |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.5287         | 10.7466      | 257.90            | 329.52            | ok     |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0320         | 2.9482       | 97.60             | 9.02              | ok     |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0806         | 0.0503       | 33.02             | 6.33              | ok     |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2642         | 0.0207       | 33.02             | 1584.12           | ok     |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.6135         | 1.0897       | 33.02             | 174.68            | ok     |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.1412         | 0.0560       | 33.02             | 32.06             | ok     |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1612         | 0.1401       | 33.02             | 1010.17           | ok     |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.6199         | 0.0226       | 33.02             | 345.04            | ok     |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0369         | 0.0197       | 33.02             | 11.20             | ok     |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0940         | 0.0336       | 52.96             | 7.53              | ok     |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1109         | 0.0399       | 60.35             | 1552.12           | ok     |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.6554         | 0.2564       | 65.18             | 189.80            | ok     |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.2180         | 0.0351       | 67.81             | 27.71             | ok     |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1505         | 0.0526       | 70.27             | 1015.58           | ok     |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.5433         | 0.0335       | 72.69             | 332.44            | ok     |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0350         | 0.0289       | 75.10             | 8.78              | ok     |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1057         | 0.1190       | 44.40             | 8.05              | ok     |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1211         | 0.1227       | 44.40             | 1592.12           | ok     |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.6499         | 3.0549       | 48.07             | 200.77            | ok     |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.3020         | 0.1680       | 44.40             | 41.70             | ok     |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1526         | 0.3016       | 44.40             | 1010.55           | ok     |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 2.7461         | 0.1046       | 44.40             | 362.88            | ok     |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0383         | 0.0647       | 44.40             | 13.63             | ok     |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1272         | 0.0063       | 77.63             | 9.21              | ok     |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1145         | 0.0129       | 77.63             | 1580.12           | ok     |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.6467         | 0.0700       | 77.63             | 181.43            | ok     |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1835         | 0.0095       | 77.63             | 32.49             | ok     |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1585         | 0.0295       | 77.63             | 1065.61           | ok     |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.7751         | 0.0060       | 77.63             | 374.31            | ok     |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0410         | 0.0051       | 77.63             | 11.80             | ok     |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0825         | 0.0143       | 77.63             | 5.86              | ok     |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1019         | 0.0200       | 77.63             | 1548.12           | ok     |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.6342         | 0.1073       | 77.63             | 187.33            | ok     |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.1944         | 0.0149       | 77.63             | 23.90             | ok     |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1509         | 0.0190       | 77.63             | 1005.33           | ok     |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.5145         | 0.0168       | 77.63             | 329.77            | ok     |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0307         | 0.0179       | 77.63             | 5.63              | ok     |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1173         | 0.2060       | 77.63             | 8.55              | ok     |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1087         | 0.3484       | 77.63             | 1560.12           | ok     |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.6632         | 3.2629       | 77.63             | 194.40            | ok     |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.2029         | 0.2908       | 77.63             | 27.73             | ok     |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1511         | 0.3675       | 77.63             | 1006.52           | ok     |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.5668         | 0.2037       | 77.63             | 356.35            | ok     |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0390         | 0.3389       | 77.63             | 13.45             | ok     |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0991         | 0.0015       | 77.63             | 6.72              | ok     |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1051         | 0.0055       | 77.63             | 1468.12           | ok     |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.6281         | 0.0557       | 77.63             | 169.93            | ok     |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.0698         | 0.0029       | 77.63             | 25.79             | ok     |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1319         | 0.0062       | 77.63             | 774.77            | ok     |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.5781         | 0.0028       | 77.63             | 332.72            | ok     |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0303         | 0.0040       | 77.63             | 7.84              | ok     |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0776         | 0.0754       | 77.63             | 5.99              | ok     |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1082         | 0.0457       | 77.63             | 1576.12           | ok     |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.5991         | 1.0591       | 77.63             | 173.37            | ok     |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0719         | 0.0887       | 77.63             | 27.80             | ok     |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1409         | 0.1907       | 77.63             | 1005.48           | ok     |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.5831         | 0.0621       | 77.63             | 340.98            | ok     |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0314         | 0.0238       | 77.63             | 10.09             | ok     |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1597         | 1.2316       | 77.63             | 9.04              | ok     |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1008         | 1.3500       | 77.63             | 1556.12           | ok     |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.6450         | 17.9678      | 77.63             | 191.59            | ok     |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.1728         | 1.3030       | 77.63             | 24.55             | ok     |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1515         | 4.1720       | 77.63             | 1010.02           | ok     |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.5636         | 1.2512       | 77.63             | 357.46            | ok     |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0361         | 1.2884       | 77.63             | 7.38              | ok     |
