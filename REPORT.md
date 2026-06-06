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

| Profile      | Leader                | Runner-Up             | Third             | Intent                                                               |
| ------------ | --------------------- | --------------------- | ----------------- | -------------------------------------------------------------------- |
| Balanced     | c (clang)             | sarif (stage0/native) | rust (rustc/llvm) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | c (clang)             | rust (rustc/llvm)     | nim (clang)       | Throughput or latency matters most.                                  |
| Memory First | c (clang)             | sarif (stage0/native) | rust (rustc/llvm) | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang)             | go (gc)           | Build and iteration cost matter most.                                |
| Deploy First | c (clang)             | sarif (stage0/native) | nim (clang)       | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Overall |
| --------------------- | ------- | ------- |
| c (clang)             | 0.9237  | 0.9237  |
| sarif (stage0/native) | 0.8523  | 0.8523  |
| rust (rustc/llvm)     | 0.8364  | 0.8364  |
| nim (clang)           | 0.7830  | 0.7830  |
| go (gc)               | 0.6861  | 0.6861  |
| moonbit (native)      | 0.6443  | 0.6443  |
| ocaml (native)        | 0.5891  | 0.5891  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | c (clang)             | 0.9237 | 0.9714 | 1.0000 | 0.4230 | 1.0000 |
| 2       | sarif (stage0/native) | 0.8523 | 0.7948 | 1.0000 | 1.0000 | 0.7129 |
| 3       | rust (rustc/llvm)     | 0.8364 | 0.9747 | 1.0000 | 0.0186 | 0.0205 |
| 4       | nim (clang)           | 0.7830 | 0.8688 | 1.0000 | 0.0390 | 0.2868 |
| 5       | go (gc)               | 0.6861 | 0.6778 | 1.0000 | 0.4533 | 0.0046 |
| 6       | moonbit (native)      | 0.6443 | 0.6741 | 1.0000 | 0.0498 | 0.0234 |
| 7       | ocaml (native)        | 0.5891 | 0.5510 | 1.0000 | 0.3057 | 0.0071 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | rust (rustc/llvm)     | 0.9747      | 0.8364          |
| 2          | c (clang)             | 0.9714      | 0.9237          |
| 3          | nim (clang)           | 0.8688      | 0.7830          |
| 4          | sarif (stage0/native) | 0.7948      | 0.8523          |
| 5          | go (gc)               | 0.6778      | 0.6861          |
| 6          | moonbit (native)      | 0.6741      | 0.6443          |
| 7          | ocaml (native)        | 0.5510      | 0.5891          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | ocaml (native)        | 1.0000       | 0.5891          |
| 1           | c (clang)             | 1.0000       | 0.9237          |
| 1           | sarif (stage0/native) | 1.0000       | 0.8523          |
| 1           | rust (rustc/llvm)     | 1.0000       | 0.8364          |
| 1           | go (gc)               | 1.0000       | 0.6861          |
| 1           | moonbit (native)      | 1.0000       | 0.6443          |
| 1           | nim (clang)           | 1.0000       | 0.7830          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.8523          |
| 2          | go (gc)               | 0.4533      | 0.6861          |
| 3          | c (clang)             | 0.4230      | 0.9237          |
| 4          | ocaml (native)        | 0.3057      | 0.5891          |
| 5          | moonbit (native)      | 0.0498      | 0.6443          |
| 6          | nim (clang)           | 0.0390      | 0.7830          |
| 7          | rust (rustc/llvm)     | 0.0186      | 0.8364          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 1.0000     | 0.9237          |
| 2         | sarif (stage0/native) | 0.7129     | 0.8523          |
| 3         | nim (clang)           | 0.2868     | 0.7830          |
| 4         | moonbit (native)      | 0.0234     | 0.6443          |
| 5         | rust (rustc/llvm)     | 0.0205     | 0.8364          |
| 6         | ocaml (native)        | 0.0071     | 0.5891          |
| 7         | go (gc)               | 0.0046     | 0.6861          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status     |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ---------- |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1971         | 8.8007       | 129.98            | 5.73              | ok         |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 4.1591         | 9.1317       | 136.96            | 1560.12           | ok         |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.9265         | 1.8761       | 98.22             | 302.43            | ok         |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.2291         | 4.7489       | 261.60            | 26.00             | ok         |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1843         | 2.3946       | 128.35            | 1006.36           | ok         |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.3704         | 9.9019       | 257.84            | 329.78            | ok         |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21\t check: 4194303 / 1048576\t trees of depth ... | 0.0662         | 22.6750      | 4036.35           | 10.28             | mismatch   |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.3428         | 0.0527       | 40.72             | 6.30              | ok         |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.4111         | 0.0183       | 40.72             | 1584.12           | ok         |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.8719         | 0.3038       | 40.72             | 301.22            | ok         |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.1379         | 0.0589       | 40.72             | 31.62             | ok         |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1835         | 0.1283       | 40.72             | 1010.14           | ok         |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.9054         | 0.0202       | 40.72             | 345.23            | ok         |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | -                                                                        | 0.0141         | 0.0000       | 0.00              | 0.00              | build-fail |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0977         | 0.0327       | 40.72             | 7.51              | ok         |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1007         | 0.0363       | 40.72             | 1556.12           | ok         |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.8567         | 0.0680       | 40.72             | 304.71            | ok         |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.1476         | 0.0342       | 40.72             | 27.66             | ok         |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1621         | 0.0486       | 42.92             | 1015.55           | ok         |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.4023         | 0.0300       | 45.22             | 332.72            | ok         |
| fasta        | sarif (stage0/native) | 250000                           | -                                                                        | 0.0114         | 0.0000       | 0.00              | 0.00              | build-fail |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0992         | 0.1068       | 40.72             | 8.02              | ok         |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1261         | 0.1007       | 40.72             | 1592.12           | ok         |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.9463         | 0.7463       | 52.26             | 314.12            | ok         |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.1581         | 0.1555       | 40.72             | 40.89             | ok         |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1416         | 0.2675       | 40.72             | 1010.52           | ok         |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 2.4951         | 0.0873       | 40.72             | 363.07            | ok         |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | -                                                                        | 0.0113         | 0.0000       | 0.00              | 0.00              | build-fail |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1124         | 0.0062       | 47.64             | 9.19              | ok         |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0991         | 0.0117       | 47.64             | 1580.12           | ok         |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.9003         | 0.0207       | 47.64             | 306.09            | ok         |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1118         | 0.0080       | 47.64             | 32.46             | ok         |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1761         | 0.0291       | 47.64             | 1065.58           | ok         |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.5437         | 0.0061       | 47.64             | 374.44            | ok         |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | -                                                                        | 0.0118         | 0.0000       | 0.00              | 0.00              | build-fail |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0819         | 0.0142       | 47.64             | 5.84              | ok         |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.0833         | 0.0181       | 47.64             | 1548.12           | ok         |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.8088         | 0.0158       | 47.64             | 300.24            | ok         |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.0594         | 0.0144       | 47.64             | 23.77             | ok         |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1280         | 0.0175       | 47.64             | 1005.30           | ok         |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.2325         | 0.0152       | 47.64             | 330.03            | ok         |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0523         | 0.0162       | 47.64             | 7.23              | ok         |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1260         | 0.1970       | 47.64             | 8.52              | ok         |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1130         | 0.3338       | 47.64             | 1560.12           | ok         |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.8569         | 0.3829       | 47.64             | 305.99            | ok         |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.0645         | 0.2915       | 47.64             | 27.09             | ok         |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1488         | 0.3413       | 47.64             | 1006.48           | ok         |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.2643         | 0.1837       | 47.64             | 356.63            | ok         |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0430         | 0.3211       | 47.64             | 16.54             | ok         |
| primecount   | c (clang)             | 50000                            | 5133                                                                     | 0.0727         | 0.0024       | 47.64             | 5.04              | ok         |
| primecount   | go (gc)               | 50000                            | 5133                                                                     | 0.0821         | 0.0049       | 47.64             | 1548.12           | ok         |
| primecount   | moonbit (native)      | 50000                            | 5133                                                                     | 0.8339         | 0.0025       | 47.64             | 299.99            | ok         |
| primecount   | nim (clang)           | 50000                            | 5133                                                                     | 1.0534         | 0.0025       | 47.64             | 22.77             | ok         |
| primecount   | ocaml (native)        | 50000                            | 5133                                                                     | 0.1409         | 0.0042       | 47.64             | 1005.27           | ok         |
| primecount   | rust (rustc/llvm)     | 50000                            | 5133                                                                     | 2.2208         | 0.0023       | 47.64             | 329.10            | ok         |
| primecount   | sarif (stage0/native) | 50000                            | 5133                                                                     | 0.0318         | 0.0027       | 47.64             | 7.81              | ok         |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0951         | 0.0016       | 47.64             | 6.70              | ok         |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0807         | 0.0048       | 47.64             | 1468.12           | ok         |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.7216         | 0.0115       | 47.64             | 296.34            | ok         |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.0049         | 0.0030       | 47.64             | 25.70             | ok         |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1173         | 0.0057       | 47.64             | 774.73            | ok         |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.1796         | 0.0027       | 47.64             | 332.84            | ok         |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | -                                                                        | 0.0076         | 0.0000       | 0.00              | 0.00              | build-fail |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0752         | 0.0644       | 47.64             | 5.97              | ok         |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0928         | 0.0376       | 47.64             | 1576.12           | ok         |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.7510         | 0.2851       | 47.64             | 299.03            | ok         |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0254         | 0.0804       | 47.64             | 27.66             | ok         |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1258         | 0.1698       | 47.64             | 1005.45           | ok         |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.2481         | 0.0420       | 47.64             | 341.17            | ok         |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | -                                                                        | 0.0086         | 0.0000       | 0.00              | 0.00              | build-fail |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1452         | 1.1768       | 47.64             | 9.02              | ok         |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.0957         | 1.3072       | 47.64             | 1560.12           | ok         |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.8630         | 3.0981       | 47.64             | 305.38            | ok         |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.1125         | 1.2589       | 47.64             | 24.63             | ok         |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1333         | 3.9732       | 47.64             | 1009.98           | ok         |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.2703         | 1.2134       | 47.64             | 357.77            | ok         |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0400         | 1.3664       | 47.64             | 10.20             | ok         |

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
