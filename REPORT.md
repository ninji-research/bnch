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
| selected_benchmarks    | binarytrees,csvgroupby,joinagg,fasta,mandelbrot,primecount,spectralnorm,nbody,knucleotide,revcomp,sortuniq                                                      |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 7                                                                                                                                                               |
| benchmarks             | 11                                                                                                                                                              |
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
| c (clang)             | clang    | native  | dynamic | yes      | 5.73                     |
| go (gc)               | go       | native  | static  | yes      | 1560.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 302.43                   |
| nim (clang)           | clang    | c       | dynamic | yes      | 26.00                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.36                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 329.78                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 10.28                    |

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
| nim (clang)           | 11         | 579          | 16184        | 1.0000     | 1.0000     |
| go (gc)               | 11         | 884          | 18145        | 0.6550     | 0.8919     |
| ocaml (native)        | 11         | 648          | 19155        | 0.8935     | 0.8449     |
| rust (rustc/llvm)     | 11         | 819          | 22420        | 0.7070     | 0.7219     |
| c (clang)             | 11         | 1074         | 28956        | 0.5391     | 0.5589     |
| moonbit (native)      | 11         | 1247         | 31263        | 0.4643     | 0.5177     |
| sarif (stage0/native) | 11         | 989          | 35284        | 0.5854     | 0.4587     |

## Benchmark Coverage

| Benchmark    | Category        | Base Wt | Effective Wt | Capabilities                                          | Unique Coverage                             | Retained For                                                                                                          |
| ------------ | --------------- | ------- | ------------ | ----------------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| binarytrees  | Allocation      | 1.00    | 0.1429       | allocation, pointer_chasing, tree_recursion           | allocation, pointer_chasing, tree_recursion | Only benchmark centered on allocation-heavy pointer traversal and recursive tree construction.                        |
| csvgroupby   | Parse/Aggregate | 1.00    | 0.1429       | csv_parsing, aggregation, sorting                     | csv_parsing                                 | Anchors real structured-text parsing plus aggregation with lighter state than the join workload.                      |
| joinagg      | Join/Aggregate  | 1.00    | 0.1429       | parsing, join_processing, aggregation, sorting        | parsing, join_processing                    | Only retained workload that exercises join logic, multi-table data shaping, and ordered aggregation together.         |
| fasta        | Text/Streaming  | 0.75    | 0.0714       | text_generation, streaming_output, buffered_io        | text_generation, streaming_output           | Covers deterministic text generation and sustained buffered output, which parsing workloads do not.                   |
| mandelbrot   | Numeric         | 1.00    | 0.0357       | numeric_compute, tight_loops, branching               | tight_loops, branching                      | Represents scalar numeric compute with tight loop and branch behavior distinct from floating-point iterative kernels. |
| primecount   | Numeric         | 1.00    | 0.0357       | numeric_compute, integer_division, integer_modulo     | integer_division, integer_modulo            | Only benchmark centered on integer division and modulo throughput with deterministic branching.                       |
| spectralnorm | Numeric         | 1.00    | 0.0357       | numeric_compute, floating_point, vector_iteration     | vector_iteration                            | Adds floating-point iterative linear-algebra style work with stable numeric comparison rules.                         |
| nbody        | Numeric         | 1.00    | 0.0357       | numeric_compute, floating_point, simulation           | simulation                                  | Only retained simulation-style kernel, preserving long-running floating-point update behavior.                        |
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
| primecount   | trial-division prime counting                                                | O(n sqrt(n))             | O(1)                     | exact I32 count of primes below n      | No precomputed tables; each candidate trial-divided by all odd integers up to sqrt(n).                                                                                 |
| spectralnorm | power method on implicit matrix                                              | O(n^2 * iterations)      | O(n)                     | one float rounded to 9 decimals        | Correctness compares canonical 9-decimal output, not raw printer differences.                                                                                          |
| nbody        | 5-body symplectic advance and energy                                         | O(iterations * bodies^2) | O(1)                     | two floats rounded to 9 decimals       | Correctness compares canonical 9-decimal energies line-by-line.                                                                                                        |
| knucleotide  | FASTA parsing plus k-mer frequency and occurrence counting                   | O(n)                     | O(unique k-mers + input) | exact multiline text                   | Uses one committed deterministic FASTA fixture and processes only the >THREE section.                                                                                  |
| revcomp      | FASTA parsing plus reverse-complement text transformation                    | O(n)                     | O(n)                     | FASTA text with case-insensitive bases | Adds streaming-style text transformation and output reshaping with the same committed fixture family.                                                                  |
| sortuniq     | line-oriented string sort and duplicate-count aggregation                    | O(n log n)               | O(n)                     | exact word,count text                  | Uses one committed deterministic newline-word fixture, includes empty-line noise, and rewards lean sort-plus-aggregation implementations.                              |

## Excluded

| Excluded From Score | Reason       |
| ------------------- | ------------ |
| binarytrees         | mismatch, ok |

## Decision Profiles

| Profile      | Leader                | Runner-Up             | Third             | Intent                                                               |
| ------------ | --------------------- | --------------------- | ----------------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | c (clang)             | rust (rustc/llvm) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | c (clang)             | rust (rustc/llvm) | Throughput or latency matters most.                                  |
| Memory First | sarif (stage0/native) | c (clang)             | go (gc)           | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang)             | go (gc)           | Build and iteration cost matter most.                                |
| Deploy First | c (clang)             | sarif (stage0/native) | go (gc)           | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Hash/String | Text/Streaming | Parse/Aggregate | Join/Aggregate | Sort/Aggregate | Overall |
| --------------------- | ------- | ----------- | -------------- | --------------- | -------------- | -------------- | ------- |
| sarif (stage0/native) | 0.5889  | 0.9820      | 0.5436         | 0.9726          | 0.9723         | 0.9732         | 0.8388  |
| c (clang)             | 0.7600  | 0.7459      | 0.9585         | 0.4096          | 0.6878         | 0.4661         | 0.6713  |
| rust (rustc/llvm)     | 0.7228  | 0.7128      | 0.4945         | 0.6253          | 0.5434         | 0.3951         | 0.5823  |
| go (gc)               | 0.5632  | 0.4928      | 0.5895         | 0.4674          | 0.6454         | 0.5365         | 0.5491  |
| nim (clang)           | 0.5961  | 0.3218      | 0.6019         | 0.3598          | 0.2683         | 0.3498         | 0.4163  |
| ocaml (native)        | 0.4912  | 0.2220      | 0.4610         | 0.3007          | 0.2383         | 0.2802         | 0.3322  |
| moonbit (native)      | 0.5380  | 0.2338      | 0.3103         | 0.2241          | 0.1381         | 0.2489         | 0.2822  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.8388 | 0.8029 | 0.9702 | 0.9435 | 0.5702 |
| 2       | c (clang)             | 0.6713 | 0.5823 | 1.0000 | 0.4283 | 1.0000 |
| 3       | rust (rustc/llvm)     | 0.5823 | 0.5965 | 0.9611 | 0.0136 | 0.0207 |
| 4       | go (gc)               | 0.5491 | 0.4790 | 0.9802 | 0.4150 | 0.0046 |
| 5       | nim (clang)           | 0.4163 | 0.3190 | 0.9682 | 0.0322 | 0.2412 |
| 6       | ocaml (native)        | 0.3322 | 0.1745 | 0.9703 | 0.2438 | 0.0073 |
| 7       | moonbit (native)      | 0.2822 | 0.1460 | 0.9065 | 0.0479 | 0.0239 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.8029      | 0.8388          |
| 2          | rust (rustc/llvm)     | 0.5965      | 0.5823          |
| 3          | c (clang)             | 0.5823      | 0.6713          |
| 4          | go (gc)               | 0.4790      | 0.5491          |
| 5          | nim (clang)           | 0.3190      | 0.4163          |
| 6          | ocaml (native)        | 0.1745      | 0.3322          |
| 7          | moonbit (native)      | 0.1460      | 0.2822          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | c (clang)             | 1.0000       | 0.6713          |
| 2           | go (gc)               | 0.9802       | 0.5491          |
| 3           | ocaml (native)        | 0.9703       | 0.3322          |
| 4           | sarif (stage0/native) | 0.9702       | 0.8388          |
| 5           | nim (clang)           | 0.9682       | 0.4163          |
| 6           | rust (rustc/llvm)     | 0.9611       | 0.5823          |
| 7           | moonbit (native)      | 0.9065       | 0.2822          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.9435      | 0.8388          |
| 2          | c (clang)             | 0.4283      | 0.6713          |
| 3          | go (gc)               | 0.4150      | 0.5491          |
| 4          | ocaml (native)        | 0.2438      | 0.3322          |
| 5          | moonbit (native)      | 0.0479      | 0.2822          |
| 6          | nim (clang)           | 0.0322      | 0.4163          |
| 7          | rust (rustc/llvm)     | 0.0136      | 0.5823          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 1.0000     | 0.6713          |
| 2         | sarif (stage0/native) | 0.5702     | 0.8388          |
| 3         | nim (clang)           | 0.2412     | 0.4163          |
| 4         | moonbit (native)      | 0.0239     | 0.2822          |
| 5         | rust (rustc/llvm)     | 0.0207     | 0.5823          |
| 6         | ocaml (native)        | 0.0073     | 0.3322          |
| 7         | go (gc)               | 0.0046     | 0.5491          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status   |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | -------- |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1147         | 11.1764      | 130.29            | 5.73              | ok       |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 5.5801         | 10.9339      | 139.56            | 1560.12           | ok       |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.1510         | 2.3365       | 98.30             | 302.43            | ok       |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.7337         | 6.0098       | 263.77            | 26.00             | ok       |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2072         | 3.1117       | 128.47            | 1006.36           | ok       |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.8666         | 14.2541      | 258.11            | 329.78            | ok       |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21\t check: 4194303 / 1048576\t trees of depth ... | 0.2064         | 19.1451      | 7027.98           | 10.28             | mismatch |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.4722         | 0.1037       | 26.27             | 6.30              | ok       |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.9560         | 0.0551       | 26.27             | 1584.12           | ok       |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.5920         | 0.7513       | 26.27             | 301.22            | ok       |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.8733         | 0.0978       | 26.27             | 31.62             | ok       |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2917         | 0.2286       | 26.27             | 1010.14           | ok       |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 4.9408         | 0.0333       | 26.27             | 345.23            | ok       |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1133         | 0.0216       | 26.27             | 13.94             | ok       |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1999         | 0.0537       | 39.58             | 7.51              | ok       |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1737         | 0.0791       | 46.78             | 1556.12           | ok       |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.9605         | 0.2033       | 51.83             | 304.71            | ok       |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.1263         | 0.0691       | 54.13             | 27.66             | ok       |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.2456         | 0.1032       | 56.71             | 1015.55           | ok       |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 9.7137         | 0.2391       | 59.11             | 332.72            | ok       |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.2949         | 0.1493       | 61.55             | 10.49             | ok       |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1539         | 0.1891       | 29.09             | 8.02              | ok       |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1700         | 0.1790       | 30.35             | 1592.12           | ok       |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.5848         | 3.6486       | 52.23             | 314.12            | ok       |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 8.2313         | 1.0395       | 30.82             | 40.89             | ok       |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.9751         | 2.1086       | 29.91             | 1010.52           | ok       |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 13.3773        | 0.2008       | 31.21             | 363.07            | ok       |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0935         | 0.1097       | 29.09             | 17.98             | ok       |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.2080         | 0.0102       | 63.98             | 9.19              | ok       |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1574         | 0.0189       | 63.98             | 1580.12           | ok       |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.4136         | 0.1605       | 63.98             | 306.09            | ok       |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 7.7552         | 0.0444       | 63.98             | 32.46             | ok       |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.3563         | 0.2840       | 63.98             | 1065.58           | ok       |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 10.6185        | 0.0093       | 63.98             | 374.44            | ok       |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0661         | 0.0073       | 63.98             | 14.34             | ok       |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.4833         | 0.0702       | 63.98             | 5.84              | ok       |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.8859         | 0.1536       | 63.98             | 1548.12           | ok       |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 5.6864         | 0.0954       | 63.98             | 300.24            | ok       |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 3.1688         | 0.0254       | 63.98             | 23.77             | ok       |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.2120         | 0.0278       | 63.98             | 1005.30           | ok       |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 3.6536         | 0.0232       | 63.98             | 330.03            | ok       |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0628         | 0.0286       | 63.98             | 7.23              | ok       |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.6844         | 0.4638       | 63.98             | 8.52              | ok       |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.2079         | 0.4963       | 63.98             | 1560.12           | ok       |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 1.4832         | 0.6758       | 63.98             | 305.99            | ok       |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 7.1972         | 1.5323       | 63.98             | 27.09             | ok       |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 1.1871         | 0.8308       | 63.98             | 1006.48           | ok       |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 3.6480         | 0.2941       | 63.98             | 356.63            | ok       |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0716         | 0.5983       | 63.98             | 16.54             | ok       |
| primecount   | c (clang)             | 50000                            | 5133                                                                     | 0.1275         | 0.0041       | 63.98             | 5.04              | ok       |
| primecount   | go (gc)               | 50000                            | 5133                                                                     | 0.3058         | 0.0096       | 63.98             | 1548.12           | ok       |
| primecount   | moonbit (native)      | 50000                            | 5133                                                                     | 1.7237         | 0.0040       | 63.98             | 299.99            | ok       |
| primecount   | nim (clang)           | 50000                            | 5133                                                                     | 3.8133         | 0.0136       | 63.98             | 22.77             | ok       |
| primecount   | ocaml (native)        | 50000                            | 5133                                                                     | 0.7517         | 0.0194       | 63.98             | 1005.27           | ok       |
| primecount   | rust (rustc/llvm)     | 50000                            | 5133                                                                     | 13.3801        | 0.0177       | 63.98             | 329.10            | ok       |
| primecount   | sarif (stage0/native) | 50000                            | 5133                                                                     | 0.2739         | 0.0338       | 63.98             | 7.81              | ok       |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1627         | 0.0024       | 63.98             | 6.70              | ok       |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1233         | 0.0067       | 63.98             | 1468.12           | ok       |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.0129         | 0.0191       | 63.98             | 296.34            | ok       |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.6699         | 0.0049       | 63.98             | 25.70             | ok       |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1965         | 0.0104       | 63.98             | 774.73            | ok       |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 3.7176         | 0.0030       | 63.98             | 332.84            | ok       |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0491         | 0.0052       | 63.98             | 9.66              | ok       |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1083         | 0.1086       | 63.98             | 5.97              | ok       |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1328         | 0.0610       | 63.98             | 1576.12           | ok       |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.2224         | 0.4150       | 63.98             | 299.03            | ok       |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.6315         | 0.1330       | 63.98             | 27.66             | ok       |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.2200         | 0.3259       | 63.98             | 1005.45           | ok       |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 3.7927         | 0.0936       | 63.98             | 341.17            | ok       |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0540         | 0.0278       | 63.98             | 12.85             | ok       |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 1.3503         | 1.7282       | 63.98             | 9.02              | ok       |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1674         | 1.9308       | 63.98             | 1560.12           | ok       |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 1.2784         | 4.7173       | 63.98             | 305.38            | ok       |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.8120         | 1.8409       | 63.98             | 24.63             | ok       |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1972         | 6.3954       | 63.98             | 1009.98           | ok       |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 3.5229         | 1.7687       | 63.98             | 357.77            | ok       |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0585         | 7.8704       | 63.98             | 10.20             | ok       |

## Mismatches

| Benchmark   | Entry                 | Output                                                                   | Reference                                                                | Status   |
| ----------- | --------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | -------- |
| binarytrees | sarif (stage0/native) | stretch tree of depth 21\t check: 4194303 / 1048576\t trees of depth ... | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | mismatch |
