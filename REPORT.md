# Benchmark Report

## Environment

| Setting                | Value                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| objective              | Build the strongest fixed-host benchmark harness for canonical, production-ready native-language implementations, with correctness enforced before any ranking. |
| runs                   | 5                                                                                                                                                               |
| min_runs               | 2                                                                                                                                                               |
| warmup                 | 1                                                                                                                                                               |
| runtime_target_s       | 0.35                                                                                                                                                            |
| max_relative_spread    | 0.03                                                                                                                                                            |
| build_jobs             | 16                                                                                                                                                              |
| canonical_entries_only | no                                                                                                                                                              |
| experimental_entries   | no                                                                                                                                                              |
| selected_benchmarks    | binarytrees,csvgroupby,joinagg,fasta,mandelbrot,spectralnorm,nbody,knucleotide,revcomp,sortuniq                                                                 |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 9                                                                                                                                                               |
| benchmarks             | 10                                                                                                                                                              |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.02                                                                                                                                                           |
| peak_memory_mode       | cgroupv2-memory.peak                                                                                                                                            |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-cosmic-com.system76.CosmicTerm-99918.scope/memory.peak                                |
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
| c (gcc)               | gcc      | native  | dynamic | yes      | 18.20                    |
| c (clang)             | clang    | native  | dynamic | yes      | 5.75                     |
| go (gc)               | go       | native  | static  | yes      | 1556.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 187.83                   |
| nim (gcc)             | gcc      | c       | dynamic | yes      | 38.55                    |
| nim (clang)           | clang    | c       | dynamic | yes      | 26.11                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.39                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 329.52                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 8.98                     |

## Entry Policies

| Entry                 | Build Profile      | Low-Burden Optimizations                                                                                                                                                        |
| --------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| c (gcc)               | native-lto-release | O3 plus LTO for whole-program release builds; native CPU tuning; frame-pointer omission and low-cost math errno cleanup; lld when available, otherwise toolchain default linker |
| c (clang)             | native-lto-release | O3 plus LTO for whole-program release builds; native CPU tuning; frame-pointer omission and low-cost math errno cleanup; lld when available, otherwise toolchain default linker |
| go (gc)               | trimpath-release   | optimized default Go compiler pipeline; trimpath and buildvcs disabled for cleaner reproducible artifacts; linker stripping and empty buildid for lean release binaries         |
| moonbit (native)      | native-release     | native target release build; toolchain-managed stripping; frozen dependency graph for reproducible builds                                                                       |
| nim (gcc)             | native-lto-danger  | danger mode plus speed optimization; ORC memory manager; C compiler native tuning with LTO; lld when available, otherwise toolchain default linker                              |
| nim (clang)           | native-lto-danger  | danger mode plus speed optimization; ORC memory manager; C compiler native tuning with LTO; lld when available, otherwise toolchain default linker                              |
| ocaml (native)        | native-release     | native-code release build with unsafe and nodynlink; C backend native tuning flags passed through ccopt; separate stripping step after build                                    |
| rust (rustc/llvm)     | native-thin-lto    | target-cpu=native; thin LTO and single codegen unit; panic abort and symbol stripping for release binaries                                                                      |
| sarif (stage0/native) | stage0-native      | native executable emitted through sarifc build; stdout result mode for benchmark output parity; retained benchmark inputs declared in per-benchmark specs                       |

## Source Concision

| Entry                 | Benchmarks | Source Lines | Source Chars | Norm Lines | Norm Chars |
| --------------------- | ---------- | ------------ | ------------ | ---------- | ---------- |
| nim (clang)           | 10         | 560          | 15821        | 1.0000     | 1.0000     |
| nim (gcc)             | 10         | 560          | 15821        | 1.0000     | 1.0000     |
| go (gc)               | 10         | 846          | 17701        | 0.6619     | 0.8938     |
| ocaml (native)        | 10         | 628          | 18714        | 0.8917     | 0.8454     |
| rust (rustc/llvm)     | 10         | 789          | 21904        | 0.7098     | 0.7223     |
| c (clang)             | 10         | 1052         | 28478        | 0.5323     | 0.5556     |
| c (gcc)               | 10         | 1052         | 28478        | 0.5323     | 0.5556     |
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

| Excluded From Score | Reason         |
| ------------------- | -------------- |
| joinagg             | build-fail, ok |
| fasta               | build-fail, ok |
| revcomp             | build-fail, ok |

## Decision Profiles

| Profile      | Leader                | Runner-Up         | Third     | Intent                                                               |
| ------------ | --------------------- | ----------------- | --------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | c (clang)         | c (gcc)   | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | rust (rustc/llvm) | c (clang) | Throughput or latency matters most.                                  |
| Memory First | sarif (stage0/native) | c (clang)         | c (gcc)   | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang)         | c (gcc)   | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | c (clang)         | c (gcc)   | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Allocation | Hash/String | Parse/Aggregate | Sort/Aggregate | Overall |
| --------------------- | ------- | ---------- | ----------- | --------------- | -------------- | ------- |
| sarif (stage0/native) | 0.7904  | 0.9641     | 0.9895      | 0.9684          | 0.9799         | 0.9385  |
| c (clang)             | 0.8415  | 0.4679     | 0.8533      | 0.5549          | 0.4686         | 0.6372  |
| c (gcc)               | 0.8446  | 0.4250     | 0.8106      | 0.5397          | 0.4111         | 0.6062  |
| rust (rustc/llvm)     | 0.7380  | 0.2523     | 0.7673      | 0.7561          | 0.4752         | 0.5978  |
| go (gc)               | 0.6462  | 0.3420     | 0.5173      | 0.8647          | 0.5567         | 0.5854  |
| nim (gcc)             | 0.7053  | 0.4546     | 0.6963      | 0.3886          | 0.3336         | 0.5157  |
| nim (clang)           | 0.7132  | 0.4422     | 0.6083      | 0.4184          | 0.3385         | 0.5041  |
| ocaml (native)        | 0.5450  | 0.8290     | 0.3470      | 0.3216          | 0.2919         | 0.4669  |
| moonbit (native)      | 0.2554  | 0.6397     | 0.2576      | 0.2192          | 0.2210         | 0.3186  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.9385 | 0.9289 | 0.9993 | 1.0000 | 0.6962 |
| 2       | c (clang)             | 0.6372 | 0.5458 | 0.9501 | 0.4319 | 0.9848 |
| 3       | c (gcc)               | 0.6062 | 0.5551 | 0.9500 | 0.3209 | 0.4657 |
| 4       | rust (rustc/llvm)     | 0.5978 | 0.6465 | 0.8751 | 0.0154 | 0.0197 |
| 5       | go (gc)               | 0.5854 | 0.5719 | 0.9460 | 0.2423 | 0.0044 |
| 6       | nim (gcc)             | 0.5157 | 0.5070 | 0.8738 | 0.0274 | 0.1729 |
| 7       | nim (clang)           | 0.5041 | 0.4829 | 0.8738 | 0.0350 | 0.2395 |
| 8       | ocaml (native)        | 0.4669 | 0.3843 | 0.9513 | 0.2647 | 0.0067 |
| 9       | moonbit (native)      | 0.3186 | 0.1705 | 0.9987 | 0.0610 | 0.0379 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.9289      | 0.9385          |
| 2          | rust (rustc/llvm)     | 0.6465      | 0.5978          |
| 3          | go (gc)               | 0.5719      | 0.5854          |
| 4          | c (gcc)               | 0.5551      | 0.6062          |
| 5          | c (clang)             | 0.5458      | 0.6372          |
| 6          | nim (gcc)             | 0.5070      | 0.5157          |
| 7          | nim (clang)           | 0.4829      | 0.5041          |
| 8          | ocaml (native)        | 0.3843      | 0.4669          |
| 9          | moonbit (native)      | 0.1705      | 0.3186          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 0.9993       | 0.9385          |
| 2           | moonbit (native)      | 0.9987       | 0.3186          |
| 3           | ocaml (native)        | 0.9513       | 0.4669          |
| 4           | c (clang)             | 0.9501       | 0.6372          |
| 5           | c (gcc)               | 0.9500       | 0.6062          |
| 6           | go (gc)               | 0.9460       | 0.5854          |
| 7           | rust (rustc/llvm)     | 0.8751       | 0.5978          |
| 8           | nim (clang)           | 0.8738       | 0.5041          |
| 9           | nim (gcc)             | 0.8738       | 0.5157          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.9385          |
| 2          | c (clang)             | 0.4319      | 0.6372          |
| 3          | c (gcc)               | 0.3209      | 0.6062          |
| 4          | ocaml (native)        | 0.2647      | 0.4669          |
| 5          | go (gc)               | 0.2423      | 0.5854          |
| 6          | moonbit (native)      | 0.0610      | 0.3186          |
| 7          | nim (clang)           | 0.0350      | 0.5041          |
| 8          | nim (gcc)             | 0.0274      | 0.5157          |
| 9          | rust (rustc/llvm)     | 0.0154      | 0.5978          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 0.9848     | 0.6372          |
| 2         | sarif (stage0/native) | 0.6962     | 0.9385          |
| 3         | c (gcc)               | 0.4657     | 0.6062          |
| 4         | nim (clang)           | 0.2395     | 0.5041          |
| 5         | nim (gcc)             | 0.1729     | 0.5157          |
| 6         | moonbit (native)      | 0.0379     | 0.3186          |
| 7         | rust (rustc/llvm)     | 0.0197     | 0.5978          |
| 8         | ocaml (native)        | 0.0067     | 0.4669          |
| 9         | go (gc)               | 0.0044     | 0.5854          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status     |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ---------- |
| binarytrees  | c (gcc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2394         | 8.2476       | 130.19            | 18.20             | ok         |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0901         | 9.1037       | 130.15            | 5.75              | ok         |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 4.1036         | 10.2174      | 133.09            | 1556.12           | ok         |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.7264         | 4.5811       | 97.93             | 187.83            | ok         |
| binarytrees  | nim (gcc)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.6355         | 5.3575       | 261.96            | 38.55             | ok         |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.2444         | 5.6141       | 261.90            | 26.11             | ok         |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1701         | 3.0484       | 128.43            | 1006.39           | ok         |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.8058         | 11.3879      | 257.51            | 329.52            | ok         |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0452         | 3.1347       | 97.66             | 8.98              | ok         |
| csvgroupby   | c (gcc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1144         | 0.0501       | 33.35             | 14.24             | ok         |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0900         | 0.0546       | 33.35             | 6.33              | ok         |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2938         | 0.0214       | 33.47             | 1584.12           | ok         |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.7386         | 1.1571       | 33.47             | 174.68            | ok         |
| csvgroupby   | nim (gcc)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.5831         | 0.0775       | 33.47             | 46.59             | ok         |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.2899         | 0.0677       | 33.47             | 32.06             | ok         |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1543         | 0.1499       | 33.47             | 1010.17           | ok         |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.8105         | 0.0251       | 33.47             | 345.04            | ok         |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0449         | 0.0217       | 33.47             | 11.03             | ok         |
| fasta        | c (gcc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1130         | 0.0340       | 58.78             | 14.20             | ok         |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1059         | 0.0343       | 70.89             | 7.53              | ok         |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1302         | 0.0412       | 73.15             | 1552.12           | ok         |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.7340         | 0.2823       | 80.36             | 189.80            | ok         |
| fasta        | nim (gcc)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.8378         | 0.0441       | 80.36             | 42.55             | ok         |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.4276         | 0.0391       | 82.84             | 27.71             | ok         |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1747         | 0.0583       | 87.60             | 1015.58           | ok         |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 3.0925         | 0.0378       | 89.79             | 332.44            | ok         |
| fasta        | sarif (stage0/native) | 250000                           | -                                                                        | 0.3184         | 0.0000       | 0.00              | 0.00              | build-fail |
| joinagg      | c (gcc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1583         | 0.1290       | 44.85             | 14.26             | ok         |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1194         | 0.1524       | 44.85             | 8.05              | ok         |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1419         | 0.1788       | 44.85             | 1592.12           | ok         |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.8770         | 3.3128       | 47.67             | 200.77            | ok         |
| joinagg      | nim (gcc)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 2.0257         | 0.2296       | 44.85             | 54.59             | ok         |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.5684         | 0.2283       | 44.85             | 41.70             | ok         |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1917         | 0.3986       | 44.85             | 1010.55           | ok         |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 3.1174         | 0.1252       | 44.85             | 362.88            | ok         |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | -                                                                        | 0.1591         | 0.0000       | 0.00              | 0.00              | build-fail |
| knucleotide  | c (gcc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1375         | 0.0069       | 92.33             | 14.36             | ok         |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1272         | 0.0066       | 92.33             | 9.21              | ok         |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1292         | 0.0134       | 92.33             | 1580.12           | ok         |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.7104         | 0.0779       | 92.33             | 181.43            | ok         |
| knucleotide  | nim (gcc)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.7450         | 0.0077       | 92.33             | 46.52             | ok         |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.2766         | 0.0095       | 92.33             | 32.49             | ok         |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1858         | 0.0313       | 92.33             | 1065.61           | ok         |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.9955         | 0.0066       | 92.33             | 374.31            | ok         |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0517         | 0.0057       | 92.33             | 11.65             | ok         |
| mandelbrot   | c (gcc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.0988         | 0.0160       | 92.33             | 14.16             | ok         |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0901         | 0.0155       | 92.33             | 5.86              | ok         |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1088         | 0.0203       | 92.33             | 1548.12           | ok         |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.7185         | 0.1285       | 92.33             | 187.33            | ok         |
| mandelbrot   | nim (gcc)             | 512                              | sha256:e41a9386e912a316                                                  | 1.7394         | 0.0155       | 92.33             | 34.49             | ok         |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.4524         | 0.0151       | 92.33             | 23.90             | ok         |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1622         | 0.0211       | 92.33             | 1005.33           | ok         |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.9731         | 0.0175       | 92.33             | 329.77            | ok         |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0345         | 0.0182       | 92.33             | 5.62              | ok         |
| nbody        | c (gcc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1272         | 0.2741       | 92.33             | 14.17             | ok         |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1165         | 0.2108       | 92.33             | 8.55              | ok         |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1152         | 0.3426       | 92.33             | 1560.12           | ok         |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.6944         | 3.4615       | 92.33             | 194.40            | ok         |
| nbody        | nim (gcc)             | 5000000                          | -0.169075164 / -0.169083134                                              | 1.5331         | 0.3017       | 92.33             | 34.49             | ok         |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.2495         | 0.2963       | 92.33             | 27.73             | ok         |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1579         | 0.3702       | 92.33             | 1006.52           | ok         |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.7291         | 0.2129       | 92.33             | 356.35            | ok         |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0485         | 0.3378       | 92.33             | 13.44             | ok         |
| revcomp      | c (gcc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1321         | 0.0018       | 92.33             | 14.21             | ok         |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1545         | 0.0022       | 92.33             | 6.72              | ok         |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1187         | 0.0063       | 92.33             | 1468.12           | ok         |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.8071         | 0.0590       | 92.33             | 169.93            | ok         |
| revcomp      | nim (gcc)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.4776         | 0.0036       | 92.33             | 34.52             | ok         |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.2382         | 0.0037       | 92.33             | 25.79             | ok         |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1586         | 0.0077       | 92.33             | 774.77            | ok         |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.9822         | 0.0032       | 92.33             | 332.72            | ok         |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | -                                                                        | 0.1130         | 0.0000       | 0.00              | 0.00              | build-fail |
| sortuniq     | c (gcc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1123         | 0.1071       | 92.33             | 14.23             | ok         |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0930         | 0.0942       | 92.33             | 5.99              | ok         |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1235         | 0.0513       | 92.33             | 1576.12           | ok         |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.7110         | 1.2082       | 92.33             | 173.37            | ok         |
| sortuniq     | nim (gcc)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.4825         | 0.1365       | 92.33             | 34.52             | ok         |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.1675         | 0.1341       | 92.33             | 27.80             | ok         |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1621         | 0.2460       | 92.33             | 1005.48           | ok         |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.8615         | 0.0611       | 92.33             | 340.98            | ok         |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0385         | 0.0257       | 92.33             | 10.02             | ok         |
| spectralnorm | c (gcc)               | 5000                             | 1.274224153                                                              | 0.1985         | 0.8005       | 92.33             | 14.19             | ok         |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1684         | 1.2962       | 92.33             | 9.04              | ok         |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1347         | 1.4718       | 92.33             | 1556.12           | ok         |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.7584         | 18.5963      | 92.33             | 191.59            | ok         |
| spectralnorm | nim (gcc)             | 5000                             | 1.274224153                                                              | 1.4766         | 1.3370       | 92.33             | 34.49             | ok         |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.2726         | 1.3847       | 92.33             | 24.55             | ok         |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1562         | 4.2677       | 92.33             | 1010.02           | ok         |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.7596         | 1.2947       | 92.33             | 357.46            | ok         |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0364         | 1.3248       | 92.33             | 7.35              | ok         |

## Mismatches

| Benchmark | Entry                 | Output | Reference               | Status     |
| --------- | --------------------- | ------ | ----------------------- | ---------- |
| joinagg   | sarif (stage0/native) | -      | sha256:37c7ac2d5630fe43 | build-fail |
| fasta     | sarif (stage0/native) | -      | sha256:dfd37a44ede2e23f | build-fail |
| revcomp   | sarif (stage0/native) | -      | sha256:14899a73679b1d83 | build-fail |
