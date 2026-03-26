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
| entries                | 6                                                                                                                                                               |
| benchmarks             | 10                                                                                                                                                              |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.03                                                                                                                                                           |
| peak_memory_mode       | ru_maxrss                                                                                                                                                       |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/session-3.scope/memory.peak unavailable for reset (Read-only file system)                                             |
| kernel                 | 6.18.16-133.desktop                                                                                                                                             |
| gcc                    | gcc (AerynOS) 15.2.1 20260227                                                                                                                                   |
| clang                  | clang version 21.1.8 (AerynOS)                                                                                                                                  |
| go                     | go version go1.26.1 linux/amd64                                                                                                                                 |
| rustc                  | rustc 1.94.0 (4a4ef493e 2026-03-02)                                                                                                                             |
| nim                    | Nim Compiler Version 2.2.8 [Linux: amd64]                                                                                                                       |
| ocamlopt               | 5.4.1                                                                                                                                                           |
| moon                   | moon 0.1.20260309 (f21b520 2026-03-09)                                                                                                                          |
| strip                  | GNU strip (GNU Binutils) 2.46.0                                                                                                                                 |

## Entries

| Entry             | Compiler | Backend | Linkage | Stripped | Binary Size Sample (KiB) |
| ----------------- | -------- | ------- | ------- | -------- | ------------------------ |
| c (clang)         | clang    | native  | dynamic | yes      | 5.73                     |
| go (gc)           | go       | native  | static  | yes      | 1556.12                  |
| moonbit (native)  | moon     | native  | dynamic | yes      | 201.15                   |
| nim (clang)       | clang    | c       | dynamic | yes      | 26.39                    |
| ocaml (native)    | ocamlopt | native  | dynamic | yes      | 1006.36                  |
| rust (rustc/llvm) | rustc    | llvm    | dynamic | yes      | 304.27                   |

## Entry Policies

| Entry             | Build Profile      | Low-Burden Optimizations                                                                                                                                                        |
| ----------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| c (clang)         | native-lto-release | O3 plus LTO for whole-program release builds; native CPU tuning; frame-pointer omission and low-cost math errno cleanup; lld when available, otherwise toolchain default linker |
| go (gc)           | trimpath-release   | optimized default Go compiler pipeline; trimpath and buildvcs disabled for cleaner reproducible artifacts; linker stripping and empty buildid for lean release binaries         |
| moonbit (native)  | native-release     | native target release build; toolchain-managed stripping; frozen dependency graph for reproducible builds                                                                       |
| nim (clang)       | native-lto-danger  | danger mode plus speed optimization; ORC memory manager; C compiler native tuning with LTO; lld when available, otherwise toolchain default linker                              |
| ocaml (native)    | native-release     | native-code release build with unsafe and nodynlink; C backend native tuning flags passed through ccopt; separate stripping step after build                                    |
| rust (rustc/llvm) | native-fat-lto     | target-cpu=native; fat LTO and single codegen unit; panic abort and symbol stripping for release binaries                                                                       |

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

| Profile      | Leader    | Runner-Up         | Third             | Intent                                                               |
| ------------ | --------- | ----------------- | ----------------- | -------------------------------------------------------------------- |
| Balanced     | c (clang) | go (gc)           | rust (rustc/llvm) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | go (gc)   | rust (rustc/llvm) | c (clang)         | Throughput or latency matters most.                                  |
| Memory First | c (clang) | go (gc)           | rust (rustc/llvm) | RAM pressure matters most.                                           |
| Build First  | c (clang) | go (gc)           | ocaml (native)    | Build and iteration cost matter most.                                |
| Deploy First | c (clang) | go (gc)           | nim (clang)       | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry             | Numeric | Allocation | Hash/String | Text/Streaming | Parse/Aggregate | Join/Aggregate | Sort/Aggregate | Overall |
| ----------------- | ------- | ---------- | ----------- | -------------- | --------------- | -------------- | -------------- | ------- |
| c (clang)         | 1.0000  | 0.6110     | 1.0000      | 1.0000         | 0.6566          | 0.9719         | 0.7537         | 1.0000  |
| go (gc)           | 0.7888  | 0.4203     | 0.7284      | 0.6619         | 1.0000          | 1.0000         | 1.0000         | 0.9299  |
| rust (rustc/llvm) | 0.9791  | 0.2577     | 0.8938      | 0.5635         | 0.8061          | 0.8868         | 0.7617         | 0.8551  |
| nim (clang)       | 0.9444  | 0.5871     | 0.6756      | 0.5161         | 0.4402          | 0.7292         | 0.5301         | 0.7307  |
| ocaml (native)    | 0.7474  | 1.0000     | 0.4352      | 0.4207         | 0.3924          | 0.5612         | 0.4127         | 0.6498  |
| moonbit (native)  | 0.3164  | 0.8981     | 0.2821      | 0.2242         | 0.2546          | 0.2249         | 0.2558         | 0.3999  |

## Summary

| Overall | Entry             | Score  | Speed  | Memory | Build  | Size   |
| ------- | ----------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | c (clang)         | 1.0000 | 0.9120 | 1.0000 | 1.0000 | 1.0000 |
| 2       | go (gc)           | 0.9299 | 0.9695 | 0.9878 | 0.6769 | 0.0046 |
| 3       | rust (rustc/llvm) | 0.8551 | 1.0000 | 0.9220 | 0.0357 | 0.0220 |
| 4       | nim (clang)       | 0.7307 | 0.7659 | 0.9255 | 0.0931 | 0.2385 |
| 5       | ocaml (native)    | 0.6498 | 0.5229 | 0.9777 | 0.6828 | 0.0072 |
| 6       | moonbit (native)  | 0.3999 | 0.2130 | 0.9986 | 0.1653 | 0.0364 |

_Displayed scores use median runtime, equal category weighting with benchmark normalization inside each category, then scale each view so its leader is 1.0000. The composite ranks fixed-host production tradeoffs; use metric views and decision profiles for narrower decisions._

## Speed View

| Speed Rank | Entry             | Speed Score | Composite Score |
| ---------- | ----------------- | ----------- | --------------- |
| 1          | rust (rustc/llvm) | 1.0000      | 0.8551          |
| 2          | go (gc)           | 0.9695      | 0.9299          |
| 3          | c (clang)         | 0.9120      | 1.0000          |
| 4          | nim (clang)       | 0.7659      | 0.7307          |
| 5          | ocaml (native)    | 0.5229      | 0.6498          |
| 6          | moonbit (native)  | 0.2130      | 0.3999          |

## Memory View

| Memory Rank | Entry             | Memory Score | Composite Score |
| ----------- | ----------------- | ------------ | --------------- |
| 1           | c (clang)         | 1.0000       | 1.0000          |
| 2           | moonbit (native)  | 0.9986       | 0.3999          |
| 3           | go (gc)           | 0.9878       | 0.9299          |
| 4           | ocaml (native)    | 0.9777       | 0.6498          |
| 5           | nim (clang)       | 0.9255       | 0.7307          |
| 6           | rust (rustc/llvm) | 0.9220       | 0.8551          |

## Build View

| Build Rank | Entry             | Build Score | Composite Score |
| ---------- | ----------------- | ----------- | --------------- |
| 1          | c (clang)         | 1.0000      | 1.0000          |
| 2          | ocaml (native)    | 0.6828      | 0.6498          |
| 3          | go (gc)           | 0.6769      | 0.9299          |
| 4          | moonbit (native)  | 0.1653      | 0.3999          |
| 5          | nim (clang)       | 0.0931      | 0.7307          |
| 6          | rust (rustc/llvm) | 0.0357      | 0.8551          |

## Size View

| Size Rank | Entry             | Size Score | Composite Score |
| --------- | ----------------- | ---------- | --------------- |
| 1         | c (clang)         | 1.0000     | 1.0000          |
| 2         | nim (clang)       | 0.2385     | 0.7307          |
| 3         | moonbit (native)  | 0.0364     | 0.3999          |
| 4         | rust (rustc/llvm) | 0.0220     | 0.8551          |
| 5         | ocaml (native)    | 0.0072     | 0.6498          |
| 6         | go (gc)           | 0.0046     | 0.9299          |

## Results

| Benchmark    | Entry             | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (clang)         | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0853         | 7.7270       | 129.98            | 5.73              | ok     |
| binarytrees  | go (gc)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.5235         | 8.1949       | 133.22            | 1556.12           | ok     |
| binarytrees  | moonbit (native)  | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.5720         | 3.1200       | 98.02             | 201.15            | ok     |
| binarytrees  | nim (clang)       | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.0472         | 4.2179       | 262.65            | 26.39             | ok     |
| binarytrees  | ocaml (native)    | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1399         | 2.6671       | 132.18            | 1006.36           | ok     |
| binarytrees  | rust (rustc/llvm) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.4831         | 12.2848      | 257.80            | 304.27            | ok     |
| csvgroupby   | c (clang)         | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1025         | 0.0570       | 30.84             | 6.30              | ok     |
| csvgroupby   | go (gc)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2993         | 0.0202       | 30.99             | 1584.12           | ok     |
| csvgroupby   | moonbit (native)  | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.7083         | 1.3394       | 30.99             | 186.44            | ok     |
| csvgroupby   | nim (clang)       | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.3012         | 0.0762       | 30.99             | 32.31             | ok     |
| csvgroupby   | ocaml (native)    | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1756         | 0.1474       | 30.99             | 1010.14           | ok     |
| csvgroupby   | rust (rustc/llvm) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 3.5063         | 0.0258       | 30.99             | 323.48            | ok     |
| fasta        | c (clang)         | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1072         | 0.0358       | 42.40             | 7.46              | ok     |
| fasta        | go (gc)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1370         | 0.0369       | 48.10             | 1552.12           | ok     |
| fasta        | moonbit (native)  | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.2844         | 0.6270       | 50.52             | 203.12            | ok     |
| fasta        | nim (clang)       | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.2210         | 0.0574       | 55.43             | 28.01             | ok     |
| fasta        | ocaml (native)    | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.3176         | 0.0857       | 57.82             | 1015.55           | ok     |
| fasta        | rust (rustc/llvm) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 5.4526         | 0.0515       | 60.25             | 311.83            | ok     |
| joinagg      | c (clang)         | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1351         | 0.1295       | 42.40             | 8.02              | ok     |
| joinagg      | go (gc)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1536         | 0.1119       | 42.40             | 1592.12           | ok     |
| joinagg      | moonbit (native)  | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.6764         | 3.1350       | 51.09             | 215.72            | ok     |
| joinagg      | nim (clang)       | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.2973         | 0.1567       | 42.40             | 41.42             | ok     |
| joinagg      | ocaml (native)    | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1620         | 0.2997       | 42.40             | 1010.52           | ok     |
| joinagg      | rust (rustc/llvm) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 3.3971         | 0.1160       | 42.40             | 342.34            | ok     |
| knucleotide  | c (clang)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1262         | 0.0056       | 62.68             | 9.19              | ok     |
| knucleotide  | go (gc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1227         | 0.0087       | 62.68             | 1580.12           | ok     |
| knucleotide  | moonbit (native)  | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.5718         | 0.0746       | 62.68             | 193.38            | ok     |
| knucleotide  | nim (clang)       | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1019         | 0.0082       | 62.68             | 32.41             | ok     |
| knucleotide  | ocaml (native)    | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1710         | 0.0239       | 62.68             | 1065.58           | ok     |
| knucleotide  | rust (rustc/llvm) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 3.0045         | 0.0053       | 62.68             | 347.73            | ok     |
| mandelbrot   | c (clang)         | 512                              | sha256:e41a9386e912a316                                                  | 0.1758         | 0.0258       | 62.68             | 5.82              | ok     |
| mandelbrot   | go (gc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.2006         | 0.0296       | 62.68             | 1548.12           | ok     |
| mandelbrot   | moonbit (native)  | 512                              | sha256:e41a9386e912a316                                                  | 1.2452         | 0.1911       | 62.68             | 200.52            | ok     |
| mandelbrot   | nim (clang)       | 512                              | sha256:e41a9386e912a316                                                  | 2.3525         | 0.0259       | 62.68             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512                              | sha256:e41a9386e912a316                                                  | 0.3128         | 0.0323       | 62.68             | 1005.30           | ok     |
| mandelbrot   | rust (rustc/llvm) | 512                              | sha256:e41a9386e912a316                                                  | 5.4759         | 0.0270       | 62.68             | 304.67            | ok     |
| nbody        | c (clang)         | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1142         | 0.2141       | 62.68             | 8.79              | ok     |
| nbody        | go (gc)           | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1124         | 0.3186       | 62.68             | 1560.12           | ok     |
| nbody        | moonbit (native)  | 5000000                          | -0.169075164 / -0.169083134                                              | 0.5868         | 3.2262       | 62.68             | 208.28            | ok     |
| nbody        | nim (clang)       | 5000000                          | -0.169075164 / -0.169083134                                              | 1.0871         | 0.2648       | 62.68             | 28.05             | ok     |
| nbody        | ocaml (native)    | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1503         | 0.3256       | 62.68             | 1006.48           | ok     |
| nbody        | rust (rustc/llvm) | 5000000                          | -0.169075164 / -0.169083134                                              | 2.7243         | 0.1821       | 62.68             | 329.12            | ok     |
| revcomp      | c (clang)         | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0980         | 0.0012       | 62.68             | 6.70              | ok     |
| revcomp      | go (gc)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1080         | 0.0052       | 62.68             | 1468.12           | ok     |
| revcomp      | moonbit (native)  | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.5567         | 0.0550       | 62.68             | 180.62            | ok     |
| revcomp      | nim (clang)       | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.9590         | 0.0033       | 62.68             | 26.02             | ok     |
| revcomp      | ocaml (native)    | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1278         | 0.0068       | 62.68             | 774.73            | ok     |
| revcomp      | rust (rustc/llvm) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.6124         | 0.0023       | 62.68             | 312.20            | ok     |
| sortuniq     | c (clang)         | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0798         | 0.0685       | 62.68             | 5.97              | ok     |
| sortuniq     | go (gc)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1192         | 0.0359       | 62.68             | 1576.12           | ok     |
| sortuniq     | moonbit (native)  | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.5842         | 1.2069       | 62.68             | 184.94            | ok     |
| sortuniq     | nim (clang)       | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0155         | 0.0873       | 62.68             | 28.07             | ok     |
| sortuniq     | ocaml (native)    | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1394         | 0.1931       | 62.68             | 1005.45           | ok     |
| sortuniq     | rust (rustc/llvm) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.8335         | 0.0472       | 62.68             | 321.23            | ok     |
| spectralnorm | c (clang)         | 5000                             | 1.274224153                                                              | 0.2986         | 2.1570       | 62.68             | 9.00              | ok     |
| spectralnorm | go (gc)           | 5000                             | 1.274224153                                                              | 0.2265         | 3.3818       | 62.68             | 1556.12           | ok     |
| spectralnorm | moonbit (native)  | 5000                             | 1.274224153                                                              | 1.2789         | 21.6028      | 62.68             | 205.59            | ok     |
| spectralnorm | nim (clang)       | 5000                             | 1.274224153                                                              | 1.1009         | 1.2068       | 62.68             | 24.82             | ok     |
| spectralnorm | ocaml (native)    | 5000                             | 1.274224153                                                              | 0.1447         | 3.8901       | 62.68             | 1009.98           | ok     |
| spectralnorm | rust (rustc/llvm) | 5000                             | 1.274224153                                                              | 2.7805         | 1.2585       | 62.68             | 329.27            | ok     |
