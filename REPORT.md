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
| sarif (stage0/native) | 11         | 984          | 34928        | 0.5884     | 0.4634     |

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

| Excluded From Score | Reason         |
| ------------------- | -------------- |
| binarytrees         | mismatch, ok   |
| csvgroupby          | build-fail, ok |
| joinagg             | build-fail, ok |
| fasta               | build-fail, ok |
| knucleotide         | build-fail, ok |
| revcomp             | build-fail, ok |
| sortuniq            | build-fail, ok |

## Decision Profiles

| Profile      | Leader                | Runner-Up             | Third                 | Intent                                                               |
| ------------ | --------------------- | --------------------- | --------------------- | -------------------------------------------------------------------- |
| Balanced     | c (clang)             | sarif (stage0/native) | nim (clang)           | Default composite across speed, memory, build time, and binary size. |
| Speed First  | c (clang)             | nim (clang)           | sarif (stage0/native) | Throughput or latency matters most.                                  |
| Memory First | c (clang)             | sarif (stage0/native) | nim (clang)           | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang)             | go (gc)               | Build and iteration cost matter most.                                |
| Deploy First | c (clang)             | sarif (stage0/native) | nim (clang)           | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Overall |
| --------------------- | ------- | ------- |
| c (clang)             | 0.8466  | 0.8466  |
| sarif (stage0/native) | 0.8071  | 0.8071  |
| nim (clang)           | 0.7860  | 0.7860  |
| rust (rustc/llvm)     | 0.6864  | 0.6864  |
| moonbit (native)      | 0.6120  | 0.6120  |
| go (gc)               | 0.5759  | 0.5759  |
| ocaml (native)        | 0.5679  | 0.5679  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | c (clang)             | 0.8466 | 0.8438 | 1.0000 | 0.4810 | 1.0000 |
| 2       | sarif (stage0/native) | 0.8071 | 0.7254 | 1.0000 | 1.0000 | 0.7129 |
| 3       | nim (clang)           | 0.7860 | 0.8729 | 1.0000 | 0.0433 | 0.2868 |
| 4       | rust (rustc/llvm)     | 0.6864 | 0.7436 | 1.0000 | 0.0196 | 0.0205 |
| 5       | moonbit (native)      | 0.6120 | 0.6244 | 1.0000 | 0.0497 | 0.0234 |
| 6       | go (gc)               | 0.5759 | 0.5045 | 1.0000 | 0.4773 | 0.0046 |
| 7       | ocaml (native)        | 0.5679 | 0.5111 | 1.0000 | 0.3536 | 0.0071 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | nim (clang)           | 0.8729      | 0.7860          |
| 2          | c (clang)             | 0.8438      | 0.8466          |
| 3          | rust (rustc/llvm)     | 0.7436      | 0.6864          |
| 4          | sarif (stage0/native) | 0.7254      | 0.8071          |
| 5          | moonbit (native)      | 0.6244      | 0.6120          |
| 6          | ocaml (native)        | 0.5111      | 0.5679          |
| 7          | go (gc)               | 0.5045      | 0.5759          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | ocaml (native)        | 1.0000       | 0.5679          |
| 1           | go (gc)               | 1.0000       | 0.5759          |
| 1           | c (clang)             | 1.0000       | 0.8466          |
| 1           | sarif (stage0/native) | 1.0000       | 0.8071          |
| 1           | rust (rustc/llvm)     | 1.0000       | 0.6864          |
| 1           | nim (clang)           | 1.0000       | 0.7860          |
| 1           | moonbit (native)      | 1.0000       | 0.6120          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.8071          |
| 2          | c (clang)             | 0.4810      | 0.8466          |
| 3          | go (gc)               | 0.4773      | 0.5759          |
| 4          | ocaml (native)        | 0.3536      | 0.5679          |
| 5          | moonbit (native)      | 0.0497      | 0.6120          |
| 6          | nim (clang)           | 0.0433      | 0.7860          |
| 7          | rust (rustc/llvm)     | 0.0196      | 0.6864          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 1.0000     | 0.8466          |
| 2         | sarif (stage0/native) | 0.7129     | 0.8071          |
| 3         | nim (clang)           | 0.2868     | 0.7860          |
| 4         | moonbit (native)      | 0.0234     | 0.6120          |
| 5         | rust (rustc/llvm)     | 0.0205     | 0.6864          |
| 6         | ocaml (native)        | 0.0071     | 0.5679          |
| 7         | go (gc)               | 0.0046     | 0.5759          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status     |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ---------- |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0995         | 8.4593       | 130.27            | 5.73              | ok         |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.5551         | 9.2064       | 137.85            | 1560.12           | ok         |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.8840         | 1.8837       | 98.18             | 302.43            | ok         |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.1772         | 4.8918       | 262.08            | 26.00             | ok         |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1781         | 2.6307       | 128.24            | 1006.36           | ok         |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.4271         | 10.7551      | 258.03            | 329.78            | ok         |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21\t check: 4194303 / 1048576\t trees of depth ... | 0.0424         | 18.4950      | 3936.73           | 10.28             | mismatch   |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1171         | 0.0450       | 40.84             | 6.30              | ok         |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2674         | 0.0204       | 40.84             | 1584.12           | ok         |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.9463         | 0.3142       | 40.84             | 301.22            | ok         |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.2087         | 0.0803       | 40.84             | 31.62             | ok         |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2490         | 0.2219       | 40.84             | 1010.14           | ok         |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.7921         | 0.0206       | 40.84             | 345.23            | ok         |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | -                                                                        | 0.0097         | 0.0000       | 0.00              | 0.00              | build-fail |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1071         | 0.0341       | 40.84             | 7.51              | ok         |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1030         | 0.0354       | 40.84             | 1556.12           | ok         |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.0959         | 0.0711       | 40.84             | 304.71            | ok         |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.2124         | 0.0345       | 42.92             | 27.66             | ok         |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1626         | 0.0566       | 45.44             | 1015.55           | ok         |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.9989         | 0.0336       | 47.89             | 332.72            | ok         |
| fasta        | sarif (stage0/native) | 250000                           | -                                                                        | 0.0127         | 0.0000       | 0.00              | 0.00              | build-fail |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1191         | 0.1390       | 40.84             | 8.02              | ok         |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1584         | 0.1450       | 40.84             | 1592.12           | ok         |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.1857         | 0.8158       | 52.27             | 314.12            | ok         |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.3269         | 0.1794       | 40.84             | 40.89             | ok         |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1934         | 0.2925       | 40.84             | 1010.52           | ok         |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 2.8119         | 0.1104       | 40.84             | 363.07            | ok         |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | -                                                                        | 0.0100         | 0.0000       | 0.00              | 0.00              | build-fail |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1265         | 0.0059       | 50.30             | 9.19              | ok         |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1033         | 0.0117       | 50.30             | 1580.12           | ok         |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.9212         | 0.0159       | 50.30             | 306.09            | ok         |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1240         | 0.0090       | 50.30             | 32.46             | ok         |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1644         | 0.0262       | 50.30             | 1065.58           | ok         |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.6095         | 0.0064       | 50.30             | 374.44            | ok         |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | -                                                                        | 0.0126         | 0.0000       | 0.00              | 0.00              | build-fail |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.1166         | 0.0204       | 50.30             | 5.84              | ok         |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1157         | 0.0229       | 50.30             | 1548.12           | ok         |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 1.0094         | 0.0181       | 50.30             | 300.24            | ok         |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.2599         | 0.0143       | 50.30             | 23.77             | ok         |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1570         | 0.0219       | 50.30             | 1005.30           | ok         |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.9779         | 0.0189       | 50.30             | 330.03            | ok         |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0452         | 0.0195       | 50.30             | 7.23              | ok         |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1081         | 0.2066       | 50.30             | 8.52              | ok         |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0983         | 0.3457       | 50.30             | 1560.12           | ok         |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.9019         | 0.3900       | 50.30             | 305.99            | ok         |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.1498         | 0.3032       | 50.30             | 27.09             | ok         |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1655         | 0.3625       | 50.30             | 1006.48           | ok         |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.4029         | 0.2019       | 50.30             | 356.63            | ok         |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0453         | 0.3280       | 50.30             | 16.54             | ok         |
| primecount   | c (clang)             | 50000                            | 5133                                                                     | 0.0891         | 0.0028       | 50.30             | 5.04              | ok         |
| primecount   | go (gc)               | 50000                            | 5133                                                                     | 0.1113         | 0.0063       | 50.30             | 1548.12           | ok         |
| primecount   | moonbit (native)      | 50000                            | 5133                                                                     | 0.9516         | 0.0024       | 50.30             | 299.99            | ok         |
| primecount   | nim (clang)           | 50000                            | 5133                                                                     | 1.2592         | 0.0026       | 50.30             | 22.77             | ok         |
| primecount   | ocaml (native)        | 50000                            | 5133                                                                     | 0.1435         | 0.0044       | 50.30             | 1005.27           | ok         |
| primecount   | rust (rustc/llvm)     | 50000                            | 5133                                                                     | 3.1150         | 0.0110       | 50.30             | 329.10            | ok         |
| primecount   | sarif (stage0/native) | 50000                            | 5133                                                                     | 0.0872         | 0.0040       | 50.30             | 7.81              | ok         |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0980         | 0.0015       | 50.30             | 6.70              | ok         |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0945         | 0.0052       | 50.30             | 1468.12           | ok         |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.7887         | 0.0119       | 50.30             | 296.34            | ok         |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.0386         | 0.0029       | 50.30             | 25.70             | ok         |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1191         | 0.0062       | 50.30             | 774.73            | ok         |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.4794         | 0.0033       | 50.30             | 332.84            | ok         |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | -                                                                        | 0.0077         | 0.0000       | 0.00              | 0.00              | build-fail |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0968         | 0.0757       | 50.30             | 5.97              | ok         |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0933         | 0.0425       | 50.30             | 1576.12           | ok         |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.7891         | 0.2910       | 50.30             | 299.03            | ok         |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0616         | 0.0823       | 50.30             | 27.66             | ok         |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1403         | 0.2364       | 50.30             | 1005.45           | ok         |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.6447         | 0.0513       | 50.30             | 341.17            | ok         |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | -                                                                        | 0.0079         | 0.0000       | 0.00              | 0.00              | build-fail |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.2903         | 1.5711       | 50.30             | 9.02              | ok         |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1468         | 3.0345       | 50.30             | 1560.12           | ok         |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 3.3525         | 6.6995       | 50.30             | 305.38            | ok         |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.4020         | 1.4244       | 50.30             | 24.63             | ok         |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1644         | 4.4187       | 50.30             | 1009.98           | ok         |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.4429         | 1.2872       | 50.30             | 357.77            | ok         |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0403         | 1.3627       | 50.30             | 10.20             | ok         |

## Mismatches

| Benchmark   | Entry                 | Output                                                                   | Reference                                                                | Status     |
| ----------- | --------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ---------- |
| binarytrees | sarif (stage0/native) | stretch tree of depth 21\t check: 4194303 / 1048576\t trees of depth ... | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | mismatch   |
| csvgroupby  | sarif (stage0/native) | -                                                                        | sha256:b7ce6bd0a0cc01ea                                                  | build-fail |
| joinagg     | sarif (stage0/native) | -                                                                        | sha256:37c7ac2d5630fe43                                                  | build-fail |
| fasta       | sarif (stage0/native) | -                                                                        | sha256:dfd37a44ede2e23f                                                  | build-fail |
| knucleotide | sarif (stage0/native) | -                                                                        | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | build-fail |
| revcomp     | sarif (stage0/native) | -                                                                        | sha256:14899a73679b1d83                                                  | build-fail |
| sortuniq    | sarif (stage0/native) | -                                                                        | sha256:6b28b0e803b80ff3                                                  | build-fail |
