# Benchmark Report

## Environment

| Setting                | Value                                                                                                                                                                            |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| objective              | Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking.                  |
| runs                   | 1                                                                                                                                                                                |
| min_runs               | 1                                                                                                                                                                                |
| warmup                 | 0                                                                                                                                                                                |
| runtime_target_s       | 0.35                                                                                                                                                                             |
| max_relative_spread    | 0.03                                                                                                                                                                             |
| build_jobs             | 16                                                                                                                                                                               |
| canonical_entries_only | yes                                                                                                                                                                              |
| experimental_entries   | no                                                                                                                                                                               |
| selected_benchmarks    | binarytrees,csvgroupby,joinagg,fasta,mandelbrot,spectralnorm,nbody,knucleotide,revcomp,sortuniq                                                                                  |
| cpu_affinity           | -                                                                                                                                                                                |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                                              |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                                               |
| entries                | 7                                                                                                                                                                                |
| benchmarks             | 10                                                                                                                                                                               |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                                          |
| logical_cores          | 16                                                                                                                                                                               |
| memory_gib             | 15.03                                                                                                                                                                            |
| peak_memory_mode       | ru_maxrss                                                                                                                                                                        |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-cosmic-com.system76.CosmicAppList-3489.scope/memory.peak unavailable for reset (Read-only file system) |
| kernel                 | 6.18.21-138.desktop                                                                                                                                                              |
| gcc                    | gcc (AerynOS) 15.2.1 20260319                                                                                                                                                    |
| clang                  | clang version 22.1.2 (AerynOS)                                                                                                                                                   |
| go                     | go version go1.26.1 linux/amd64                                                                                                                                                  |
| rustc                  | rustc 1.94.1 (e408947bf 2026-03-25)                                                                                                                                              |
| nim                    | Nim Compiler Version 2.2.8 [Linux: amd64]                                                                                                                                        |
| ocamlopt               | 5.4.1                                                                                                                                                                            |
| moon                   | moon 0.1.20260309 (f21b520 2026-03-09)                                                                                                                                           |
| strip                  | GNU strip (GNU Binutils) 2.46.0                                                                                                                                                  |
| sarifc                 | sarifc 0.1.0                                                                                                                                                                     |

## Entries

| Entry                 | Compiler | Backend | Linkage | Stripped | Binary Size Sample (KiB) |
| --------------------- | -------- | ------- | ------- | -------- | ------------------------ |
| c (clang)             | clang    | native  | dynamic | yes      | 5.73                     |
| go (gc)               | go       | native  | static  | yes      | 1556.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 201.02                   |
| nim (clang)           | clang    | c       | dynamic | yes      | 26.08                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.36                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 304.27                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 17.30                    |

## Entry Policies

| Entry                 | Build Profile      | Low-Burden Optimizations                                                                                                                                                        |
| --------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| c (clang)             | native-lto-release | O3 plus LTO for whole-program release builds; native CPU tuning; frame-pointer omission and low-cost math errno cleanup; lld when available, otherwise toolchain default linker |
| go (gc)               | trimpath-release   | optimized default Go compiler pipeline; trimpath and buildvcs disabled for cleaner reproducible artifacts; linker stripping and empty buildid for lean release binaries         |
| moonbit (native)      | native-release     | native target release build; toolchain-managed stripping; frozen dependency graph for reproducible builds                                                                       |
| nim (clang)           | native-lto-danger  | danger mode plus speed optimization; ORC memory manager; C compiler native tuning with LTO; lld when available, otherwise toolchain default linker                              |
| ocaml (native)        | native-release     | native-code release build with unsafe and nodynlink; C backend native tuning flags passed through ccopt; separate stripping step after build                                    |
| rust (rustc/llvm)     | native-fat-lto     | target-cpu=native; fat LTO and single codegen unit; panic abort and symbol stripping for release binaries                                                                       |
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
| sarif (stage0/native) | 10         | 1174         | 39973        | 0.4770     | 0.3958     |

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

| Profile      | Leader                | Runner-Up             | Third          | Intent                                                               |
| ------------ | --------------------- | --------------------- | -------------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | c (clang)             | go (gc)        | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | rust (rustc/llvm)     | go (gc)        | Throughput or latency matters most.                                  |
| Memory First | c (clang)             | sarif (stage0/native) | go (gc)        | RAM pressure matters most.                                           |
| Build First  | c (clang)             | go (gc)               | ocaml (native) | Build and iteration cost matter most.                                |
| Deploy First | c (clang)             | sarif (stage0/native) | go (gc)        | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Allocation | Hash/String | Text/Streaming | Parse/Aggregate | Join/Aggregate | Sort/Aggregate | Overall |
| --------------------- | ------- | ---------- | ----------- | -------------- | --------------- | -------------- | -------------- | ------- |
| sarif (stage0/native) | 0.7780  | 0.8277     | 1.0000      | 0.6373         | 0.8515          | 1.0000         | 1.0000         | 1.0000  |
| c (clang)             | 1.0000  | 0.6109     | 0.9407      | 1.0000         | 0.6769          | 0.8076         | 0.5705         | 0.9317  |
| go (gc)               | 0.8215  | 0.4143     | 0.6841      | 0.8425         | 1.0000          | 0.7405         | 0.7260         | 0.8652  |
| rust (rustc/llvm)     | 0.8302  | 0.3004     | 0.9003      | 0.7894         | 0.7355          | 0.6935         | 0.5346         | 0.7953  |
| nim (clang)           | 0.8076  | 0.5764     | 0.6881      | 0.6745         | 0.4489          | 0.5280         | 0.4304         | 0.6889  |
| ocaml (native)        | 0.6631  | 1.0000     | 0.4458      | 0.5418         | 0.3829          | 0.4668         | 0.3716         | 0.6349  |
| moonbit (native)      | 0.2842  | 0.7946     | 0.2793      | 0.2538         | 0.2557          | 0.2337         | 0.2522         | 0.3813  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 1.0000 | 1.0000 | 1.0000 | 0.4427 | 0.4039 |
| 2       | c (clang)             | 0.9317 | 0.7480 | 0.9861 | 1.0000 | 1.0000 |
| 3       | go (gc)               | 0.8652 | 0.8006 | 0.9725 | 0.7018 | 0.0046 |
| 4       | rust (rustc/llvm)     | 0.7953 | 0.8380 | 0.9113 | 0.0372 | 0.0220 |
| 5       | nim (clang)           | 0.6889 | 0.6493 | 0.9147 | 0.0934 | 0.2399 |
| 6       | ocaml (native)        | 0.6349 | 0.4608 | 0.9658 | 0.7092 | 0.0072 |
| 7       | moonbit (native)      | 0.3813 | 0.1694 | 0.9965 | 0.1722 | 0.0363 |

_Displayed scores use median runtime, equal category weighting with benchmark normalization inside each category, then scale each view so its leader is 1.0000. The composite ranks fixed-host production tradeoffs; use metric views and decision profiles for narrower decisions._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 1.0000          |
| 2          | rust (rustc/llvm)     | 0.8380      | 0.7953          |
| 3          | go (gc)               | 0.8006      | 0.8652          |
| 4          | c (clang)             | 0.7480      | 0.9317          |
| 5          | nim (clang)           | 0.6493      | 0.6889          |
| 6          | ocaml (native)        | 0.4608      | 0.6349          |
| 7          | moonbit (native)      | 0.1694      | 0.3813          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 1.0000       | 1.0000          |
| 2           | moonbit (native)      | 0.9965       | 0.3813          |
| 3           | c (clang)             | 0.9861       | 0.9317          |
| 4           | go (gc)               | 0.9725       | 0.8652          |
| 5           | ocaml (native)        | 0.9658       | 0.6349          |
| 6           | nim (clang)           | 0.9147       | 0.6889          |
| 7           | rust (rustc/llvm)     | 0.9113       | 0.7953          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | c (clang)             | 1.0000      | 0.9317          |
| 2          | ocaml (native)        | 0.7092      | 0.6349          |
| 3          | go (gc)               | 0.7018      | 0.8652          |
| 4          | sarif (stage0/native) | 0.4427      | 1.0000          |
| 5          | moonbit (native)      | 0.1722      | 0.3813          |
| 6          | nim (clang)           | 0.0934      | 0.6889          |
| 7          | rust (rustc/llvm)     | 0.0372      | 0.7953          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 1.0000     | 0.9317          |
| 2         | sarif (stage0/native) | 0.4039     | 1.0000          |
| 3         | nim (clang)           | 0.2399     | 0.6889          |
| 4         | moonbit (native)      | 0.0363     | 0.3813          |
| 5         | rust (rustc/llvm)     | 0.0220     | 0.7953          |
| 6         | ocaml (native)        | 0.0072     | 0.6349          |
| 7         | go (gc)               | 0.0046     | 0.8652          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0846         | 8.2562       | 129.93            | 5.73              | ok     |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.7693         | 8.7414       | 137.43            | 1556.12           | ok     |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.6072         | 3.9444       | 97.95             | 201.02            | ok     |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.1210         | 4.5813       | 262.82            | 26.08             | ok     |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1475         | 2.8200       | 132.43            | 1006.36           | ok     |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.5483         | 10.3704      | 257.56            | 304.27            | ok     |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2217         | 4.0446       | 97.72             | 17.30             | ok     |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0874         | 0.0408       | 34.03             | 6.30              | ok     |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2957         | 0.0154       | 34.03             | 1584.12           | ok     |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.5855         | 1.1770       | 34.06             | 186.38            | ok     |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.0939         | 0.0565       | 34.06             | 32.03             | ok     |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1560         | 0.1241       | 34.06             | 1010.14           | ok     |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.8042         | 0.0226       | 34.06             | 323.48            | ok     |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2259         | 0.0204       | 34.06             | 17.23             | ok     |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1090         | 0.0318       | 45.42             | 7.51              | ok     |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1326         | 0.0344       | 50.67             | 1552.12           | ok     |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.6203         | 0.2619       | 52.97             | 203.00            | ok     |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.1372         | 0.0333       | 57.84             | 27.68             | ok     |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1492         | 0.0512       | 60.37             | 1015.55           | ok     |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.6178         | 0.0319       | 62.79             | 311.83            | ok     |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.2702         | 0.0358       | 65.20             | 17.52             | ok     |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1196         | 0.1099       | 45.42             | 8.02              | ok     |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1280         | 0.1114       | 45.42             | 1592.12           | ok     |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.6311         | 2.9821       | 50.59             | 215.59            | ok     |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.2322         | 0.1620       | 45.42             | 41.67             | ok     |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1501         | 0.2893       | 45.42             | 1010.52           | ok     |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 3.1057         | 0.0997       | 45.42             | 342.34            | ok     |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.2453         | 0.0663       | 45.42             | 19.42             | ok     |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1252         | 0.0063       | 67.64             | 9.19              | ok     |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1204         | 0.0100       | 67.64             | 1580.12           | ok     |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.6201         | 0.0910       | 67.64             | 193.31            | ok     |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1571         | 0.0081       | 67.64             | 32.46             | ok     |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1524         | 0.0250       | 67.64             | 1065.58           | ok     |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 3.0696         | 0.0053       | 67.64             | 347.73            | ok     |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.2372         | 0.0051       | 67.64             | 19.31             | ok     |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0934         | 0.0149       | 67.64             | 5.84              | ok     |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1065         | 0.0159       | 67.64             | 1548.12           | ok     |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.6043         | 0.0975       | 67.64             | 200.40            | ok     |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.1185         | 0.0143       | 67.64             | 23.87             | ok     |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1410         | 0.0162       | 67.64             | 1005.30           | ok     |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.5593         | 0.0155       | 67.64             | 304.67            | ok     |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.2200         | 0.0160       | 67.64             | 15.55             | ok     |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1116         | 0.1919       | 67.64             | 8.52              | ok     |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1147         | 0.3276       | 67.64             | 1560.12           | ok     |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.6246         | 3.3709       | 67.64             | 208.16            | ok     |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.1454         | 0.2787       | 67.64             | 27.70             | ok     |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1467         | 0.3439       | 67.64             | 1006.48           | ok     |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.8295         | 0.1845       | 67.64             | 329.12            | ok     |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.2201         | 0.4049       | 67.64             | 18.70             | ok     |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1053         | 0.0017       | 67.64             | 6.70              | ok     |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1050         | 0.0021       | 67.64             | 1468.12           | ok     |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.5767         | 0.0630       | 67.64             | 180.50            | ok     |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.9839         | 0.0034       | 67.64             | 25.76             | ok     |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1268         | 0.0064       | 67.64             | 774.73            | ok     |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.6340         | 0.0019       | 67.64             | 312.20            | ok     |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.3106         | 0.0046       | 67.64             | 16.66             | ok     |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0938         | 0.0867       | 67.64             | 5.97              | ok     |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1322         | 0.0377       | 67.64             | 1576.12           | ok     |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.5994         | 1.1801       | 67.64             | 184.81            | ok     |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0623         | 0.0853       | 67.64             | 27.77             | ok     |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1504         | 0.1942       | 67.64             | 1005.45           | ok     |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.7884         | 0.0520       | 67.64             | 321.23            | ok     |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.2200         | 0.0226       | 67.64             | 16.48             | ok     |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1593         | 1.1514       | 67.64             | 9.02              | ok     |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1170         | 1.3250       | 67.64             | 1556.12           | ok     |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.6052         | 18.1739      | 67.64             | 205.47            | ok     |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.0903         | 1.2375       | 67.64             | 24.52             | ok     |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1413         | 3.9530       | 67.64             | 1009.98           | ok     |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.7828         | 1.3370       | 67.64             | 329.27            | ok     |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.2276         | 1.2865       | 67.64             | 16.05             | ok     |
