# Benchmark Report

## Environment

| Setting                | Value                                                                                                                                                                            |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| objective              | Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking.                  |
| runs                   | 5                                                                                                                                                                                |
| min_runs               | 2                                                                                                                                                                                |
| warmup                 | 1                                                                                                                                                                                |
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
| memory_gib             | 15.02                                                                                                                                                                            |
| peak_memory_mode       | ru_maxrss                                                                                                                                                                        |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-cosmic-com.system76.CosmicAppList-2629.scope/memory.peak unavailable for reset (Read-only file system) |
| kernel                 | 7.0.6-32.stable                                                                                                                                                                  |
| gcc                    | gcc (AerynOS) 16.1.1 20260505                                                                                                                                                    |
| clang                  | clang version 22.1.5 (AerynOS)                                                                                                                                                   |
| go                     | go version go1.26.3 linux/amd64                                                                                                                                                  |
| rustc                  | rustc 1.95.0 (59807616e 2026-04-14)                                                                                                                                              |
| nim                    | Nim Compiler Version 2.2.10 [Linux: amd64]                                                                                                                                       |
| ocamlopt               | 5.4.1                                                                                                                                                                            |
| moon                   | moon 0.1.20260512 (81d40e3 2026-05-12)                                                                                                                                           |
| strip                  | GNU strip (GNU Binutils) 2.46.0                                                                                                                                                  |
| sarifc                 | sarifc 0.1.0                                                                                                                                                                     |

## Entries

| Entry                 | Compiler | Backend | Linkage | Stripped | Binary Size Sample (KiB) |
| --------------------- | -------- | ------- | ------- | -------- | ------------------------ |
| c (clang)             | clang    | native  | dynamic | yes      | 5.73                     |
| go (gc)               | go       | native  | static  | yes      | 1560.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 181.98                   |
| nim (clang)           | clang    | c       | dynamic | yes      | 26.00                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.36                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 329.48                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 8.93                     |

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
| sarif (stage0/native) | 0.8688  | 0.7391     | 0.9877      | 0.7741         | 0.9767          | 0.9799         | 0.9796         | 0.9009  |
| c (clang)             | 0.9226  | 0.3826     | 0.8600      | 0.9106         | 0.5337          | 0.5881         | 0.4640         | 0.6660  |
| rust (rustc/llvm)     | 0.8190  | 0.1930     | 0.7766      | 0.6581         | 0.6775          | 0.5807         | 0.4571         | 0.5946  |
| go (gc)               | 0.7237  | 0.2843     | 0.5209      | 0.5686         | 0.7478          | 0.5473         | 0.5279         | 0.5601  |
| nim (clang)           | 0.7636  | 0.3424     | 0.6103      | 0.6311         | 0.4005          | 0.4279         | 0.3552         | 0.5044  |
| ocaml (native)        | 0.5830  | 0.6250     | 0.3512      | 0.4700         | 0.3092          | 0.3446         | 0.2859         | 0.4241  |
| moonbit (native)      | 0.5931  | 0.8545     | 0.4104      | 0.3642         | 0.2417          | 0.2182         | 0.2507         | 0.4190  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.9009 | 0.8776 | 0.9781 | 1.0000 | 0.6964 |
| 2       | c (clang)             | 0.6660 | 0.5912 | 0.9644 | 0.3919 | 0.9926 |
| 3       | rust (rustc/llvm)     | 0.5946 | 0.6364 | 0.8920 | 0.0148 | 0.0203 |
| 4       | go (gc)               | 0.5601 | 0.5246 | 0.9511 | 0.2861 | 0.0045 |
| 5       | nim (clang)           | 0.5044 | 0.4775 | 0.8940 | 0.0336 | 0.2388 |
| 6       | ocaml (native)        | 0.4241 | 0.3212 | 0.9482 | 0.2534 | 0.0071 |
| 7       | moonbit (native)      | 0.4190 | 0.3383 | 0.9641 | 0.0428 | 0.0389 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.8776      | 0.9009          |
| 2          | rust (rustc/llvm)     | 0.6364      | 0.5946          |
| 3          | c (clang)             | 0.5912      | 0.6660          |
| 4          | go (gc)               | 0.5246      | 0.5601          |
| 5          | nim (clang)           | 0.4775      | 0.5044          |
| 6          | moonbit (native)      | 0.3383      | 0.4190          |
| 7          | ocaml (native)        | 0.3212      | 0.4241          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 0.9781       | 0.9009          |
| 2           | c (clang)             | 0.9644       | 0.6660          |
| 3           | moonbit (native)      | 0.9641       | 0.4190          |
| 4           | go (gc)               | 0.9511       | 0.5601          |
| 5           | ocaml (native)        | 0.9482       | 0.4241          |
| 6           | nim (clang)           | 0.8940       | 0.5044          |
| 7           | rust (rustc/llvm)     | 0.8920       | 0.5946          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.9009          |
| 2          | c (clang)             | 0.3919      | 0.6660          |
| 3          | go (gc)               | 0.2861      | 0.5601          |
| 4          | ocaml (native)        | 0.2534      | 0.4241          |
| 5          | moonbit (native)      | 0.0428      | 0.4190          |
| 6          | nim (clang)           | 0.0336      | 0.5044          |
| 7          | rust (rustc/llvm)     | 0.0148      | 0.5946          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 0.9926     | 0.6660          |
| 2         | sarif (stage0/native) | 0.6964     | 0.9009          |
| 3         | nim (clang)           | 0.2388     | 0.5044          |
| 4         | moonbit (native)      | 0.0389     | 0.4190          |
| 5         | rust (rustc/llvm)     | 0.0203     | 0.5946          |
| 6         | ocaml (native)        | 0.0071     | 0.4241          |
| 7         | go (gc)               | 0.0045     | 0.5601          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0866         | 7.4298       | 130.13            | 5.73              | ok     |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.2720         | 7.9742       | 131.39            | 1560.12           | ok     |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.8540         | 1.6484       | 98.22             | 181.98            | ok     |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.0921         | 4.2128       | 263.98            | 26.00             | ok     |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1689         | 2.3657       | 128.39            | 1006.36           | ok     |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.5324         | 9.3151       | 257.80            | 329.48            | ok     |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0331         | 2.6322       | 97.73             | 8.93              | ok     |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0775         | 0.0405       | 32.93             | 6.30              | ok     |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2347         | 0.0182       | 32.93             | 1584.12           | ok     |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.7571         | 0.2741       | 32.93             | 177.46            | ok     |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.9882         | 0.0519       | 32.93             | 31.62             | ok     |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1303         | 0.1173       | 32.93             | 1010.14           | ok     |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.3239         | 0.0204       | 32.93             | 345.01            | ok     |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0341         | 0.0149       | 33.18             | 11.16             | ok     |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0836         | 0.0310       | 58.35             | 7.51              | ok     |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0950         | 0.0351       | 70.46             | 1556.12           | ok     |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.8112         | 0.0650       | 72.77             | 184.27            | ok     |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.0701         | 0.0328       | 75.26             | 27.66             | ok     |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1350         | 0.0472       | 77.60             | 1015.55           | ok     |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.2200         | 0.0298       | 80.03             | 332.41            | ok     |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0331         | 0.0280       | 82.43             | 8.76              | ok     |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0995         | 0.1024       | 44.58             | 8.02              | ok     |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1100         | 0.0983       | 44.58             | 1592.12           | ok     |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.9356         | 0.7395       | 52.27             | 193.62            | ok     |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.1163         | 0.1428       | 44.58             | 40.89             | ok     |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1369         | 0.2644       | 44.58             | 1010.52           | ok     |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 2.4445         | 0.0811       | 44.58             | 362.85            | ok     |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0387         | 0.0472       | 44.58             | 13.41             | ok     |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1045         | 0.0057       | 84.78             | 9.19              | ok     |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0984         | 0.0116       | 84.78             | 1580.12           | ok     |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.8269         | 0.0162       | 84.78             | 182.34            | ok     |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.0375         | 0.0084       | 84.78             | 32.46             | ok     |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1442         | 0.0261       | 84.78             | 1065.58           | ok     |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.3660         | 0.0057       | 84.78             | 374.28            | ok     |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0357         | 0.0051       | 84.78             | 12.17             | ok     |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0777         | 0.0140       | 84.78             | 5.84              | ok     |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.0854         | 0.0188       | 84.78             | 1548.12           | ok     |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.7951         | 0.0161       | 84.78             | 179.80            | ok     |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.0130         | 0.0147       | 84.78             | 23.77             | ok     |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1281         | 0.0177       | 84.78             | 1005.30           | ok     |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.1518         | 0.0157       | 84.78             | 329.73            | ok     |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0300         | 0.0159       | 84.78             | 5.67              | ok     |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1087         | 0.1946       | 84.78             | 8.52              | ok     |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0948         | 0.3106       | 84.78             | 1560.12           | ok     |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.8436         | 0.3461       | 84.78             | 185.55            | ok     |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.0218         | 0.2877       | 84.78             | 27.09             | ok     |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1393         | 0.3356       | 84.78             | 1006.48           | ok     |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.2356         | 0.1869       | 84.78             | 356.32            | ok     |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0429         | 0.3125       | 84.78             | 14.02             | ok     |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0803         | 0.0014       | 84.78             | 6.70              | ok     |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0823         | 0.0054       | 84.78             | 1468.12           | ok     |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.6961         | 0.0125       | 84.78             | 172.59            | ok     |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.9290         | 0.0029       | 84.78             | 25.70             | ok     |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1101         | 0.0064       | 84.78             | 774.73            | ok     |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.1554         | 0.0026       | 84.78             | 332.69            | ok     |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0355         | 0.0034       | 84.78             | 7.86              | ok     |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0724         | 0.0662       | 84.78             | 5.97              | ok     |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0869         | 0.0388       | 84.78             | 1576.12           | ok     |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.7287         | 0.2529       | 84.78             | 175.27            | ok     |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.9659         | 0.0800       | 84.78             | 27.66             | ok     |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1280         | 0.1852       | 84.78             | 1005.45           | ok     |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.3269         | 0.0443       | 84.78             | 340.95            | ok     |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0315         | 0.0174       | 84.78             | 10.09             | ok     |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1356         | 1.1107       | 84.78             | 9.02              | ok     |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.0925         | 1.2440       | 84.78             | 1560.12           | ok     |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.8460         | 2.9491       | 84.78             | 184.93            | ok     |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.0428         | 1.2120       | 84.78             | 24.63             | ok     |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1384         | 3.6728       | 84.78             | 1009.98           | ok     |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.2298         | 1.1635       | 84.78             | 357.43            | ok     |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0313         | 1.1737       | 84.78             | 7.86              | ok     |
