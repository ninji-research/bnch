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
| peak_memory_mode       | cgroupv2-memory.peak                                                                                                                                            |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-cosmic-com.system76.CosmicAppList-43625.scope/memory.peak                             |
| kernel                 | 7.0.3-6.stable                                                                                                                                                  |
| gcc                    | gcc (AerynOS) 15.2.1 20260421                                                                                                                                   |
| clang                  | clang version 22.1.4 (AerynOS)                                                                                                                                  |
| go                     | go version go1.26.2 linux/amd64                                                                                                                                 |
| rustc                  | rustc 1.95.0 (59807616e 2026-04-14)                                                                                                                             |
| nim                    | Nim Compiler Version 2.2.10 [Linux: amd64]                                                                                                                      |
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
| nim (clang)           | clang    | c       | dynamic | yes      | 26.03                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.39                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 329.52                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 8.99                     |

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
| Build First  | sarif (stage0/native) | c (clang) | go (gc)           | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | c (clang) | nim (clang)       | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Allocation | Hash/String | Text/Streaming | Parse/Aggregate | Join/Aggregate | Sort/Aggregate | Overall |
| --------------------- | ------- | ---------- | ----------- | -------------- | --------------- | -------------- | -------------- | ------- |
| sarif (stage0/native) | 0.8670  | 0.9347     | 0.9877      | 0.7601         | 0.9783          | 0.9795         | 0.9797         | 0.9267  |
| c (clang)             | 0.8698  | 0.4056     | 0.8269      | 0.9224         | 0.5494          | 0.6320         | 0.4896         | 0.6708  |
| rust (rustc/llvm)     | 0.8323  | 0.2315     | 0.7105      | 0.6355         | 0.7336          | 0.5580         | 0.4666         | 0.5954  |
| go (gc)               | 0.6925  | 0.3191     | 0.4886      | 0.5617         | 0.7657          | 0.5733         | 0.5469         | 0.5640  |
| nim (clang)           | 0.7773  | 0.4126     | 0.5694      | 0.6226         | 0.3572          | 0.4608         | 0.3506         | 0.5072  |
| ocaml (native)        | 0.5630  | 0.8420     | 0.3407      | 0.4574         | 0.3068          | 0.3650         | 0.2902         | 0.4522  |
| moonbit (native)      | 0.2667  | 0.5803     | 0.2565      | 0.2324         | 0.2179          | 0.1766         | 0.2209         | 0.2788  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.9267 | 0.9189 | 0.9730 | 1.0000 | 0.6962 |
| 2       | c (clang)             | 0.6708 | 0.6014 | 0.9643 | 0.3746 | 0.9917 |
| 3       | rust (rustc/llvm)     | 0.5954 | 0.6393 | 0.8852 | 0.0180 | 0.0204 |
| 4       | go (gc)               | 0.5640 | 0.5329 | 0.9456 | 0.2823 | 0.0045 |
| 5       | nim (clang)           | 0.5072 | 0.4829 | 0.8875 | 0.0389 | 0.2390 |
| 6       | ocaml (native)        | 0.4522 | 0.3607 | 0.9414 | 0.2903 | 0.0071 |
| 7       | moonbit (native)      | 0.2788 | 0.1232 | 0.9491 | 0.0692 | 0.0386 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.9189      | 0.9267          |
| 2          | rust (rustc/llvm)     | 0.6393      | 0.5954          |
| 3          | c (clang)             | 0.6014      | 0.6708          |
| 4          | go (gc)               | 0.5329      | 0.5640          |
| 5          | nim (clang)           | 0.4829      | 0.5072          |
| 6          | ocaml (native)        | 0.3607      | 0.4522          |
| 7          | moonbit (native)      | 0.1232      | 0.2788          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 0.9730       | 0.9267          |
| 2           | c (clang)             | 0.9643       | 0.6708          |
| 3           | moonbit (native)      | 0.9491       | 0.2788          |
| 4           | go (gc)               | 0.9456       | 0.5640          |
| 5           | ocaml (native)        | 0.9414       | 0.4522          |
| 6           | nim (clang)           | 0.8875       | 0.5072          |
| 7           | rust (rustc/llvm)     | 0.8852       | 0.5954          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.9267          |
| 2          | c (clang)             | 0.3746      | 0.6708          |
| 3          | ocaml (native)        | 0.2903      | 0.4522          |
| 4          | go (gc)               | 0.2823      | 0.5640          |
| 5          | moonbit (native)      | 0.0692      | 0.2788          |
| 6          | nim (clang)           | 0.0389      | 0.5072          |
| 7          | rust (rustc/llvm)     | 0.0180      | 0.5954          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 0.9917     | 0.6708          |
| 2         | sarif (stage0/native) | 0.6962     | 0.9267          |
| 3         | nim (clang)           | 0.2390     | 0.5072          |
| 4         | moonbit (native)      | 0.0386     | 0.2788          |
| 5         | rust (rustc/llvm)     | 0.0204     | 0.5954          |
| 6         | ocaml (native)        | 0.0071     | 0.4522          |
| 7         | go (gc)               | 0.0045     | 0.5640          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.3541         | 10.9823      | 130.05            | 5.75              | ok     |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 4.6905         | 11.4826      | 135.03            | 1556.12           | ok     |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.0498         | 5.3366       | 97.98             | 187.83            | ok     |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.6376         | 6.1581       | 262.03            | 26.03             | ok     |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2259         | 3.0466       | 128.24            | 1006.39           | ok     |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.1773         | 13.0239      | 257.79            | 329.52            | ok     |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0892         | 3.2857       | 97.60             | 8.99              | ok     |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1202         | 0.0514       | 31.75             | 6.33              | ok     |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.3962         | 0.0243       | 31.75             | 1584.12           | ok     |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.7664         | 1.3188       | 31.75             | 174.68            | ok     |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.3021         | 0.0938       | 31.75             | 31.66             | ok     |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2011         | 0.1600       | 31.75             | 1010.17           | ok     |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 3.0687         | 0.0254       | 31.75             | 345.04            | ok     |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0446         | 0.0207       | 31.75             | 11.18             | ok     |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1214         | 0.0375       | 46.47             | 7.53              | ok     |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1294         | 0.0447       | 58.58             | 1552.12           | ok     |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.7577         | 0.2968       | 61.05             | 189.80            | ok     |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.4743         | 0.0415       | 68.32             | 27.70             | ok     |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1973         | 0.0598       | 70.66             | 1015.58           | ok     |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 3.1590         | 0.0398       | 73.10             | 332.44            | ok     |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0503         | 0.0354       | 74.69             | 8.78              | ok     |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1298         | 0.1400       | 36.21             | 8.05              | ok     |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1326         | 0.1434       | 36.21             | 1592.12           | ok     |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.7543         | 3.4070       | 47.21             | 200.77            | ok     |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.4996         | 0.1922       | 36.21             | 40.92             | ok     |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1864         | 0.3521       | 36.21             | 1010.55           | ok     |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 3.3877         | 0.1338       | 36.21             | 362.88            | ok     |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0552         | 0.0731       | 36.21             | 13.62             | ok     |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1204         | 0.0054       | 77.41             | 9.21              | ok     |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1055         | 0.0118       | 77.41             | 1580.12           | ok     |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.5529         | 0.0633       | 77.41             | 181.43            | ok     |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.0647         | 0.0083       | 77.41             | 32.49             | ok     |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1432         | 0.0267       | 77.41             | 1065.61           | ok     |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.3628         | 0.0057       | 77.41             | 374.31            | ok     |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0450         | 0.0045       | 77.41             | 12.21             | ok     |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.1382         | 0.0181       | 77.41             | 5.86              | ok     |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1495         | 0.0215       | 77.41             | 1548.12           | ok     |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.8088         | 0.1199       | 77.41             | 187.33            | ok     |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.4078         | 0.0172       | 77.41             | 23.80             | ok     |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1989         | 0.0252       | 77.41             | 1005.33           | ok     |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 3.0190         | 0.0188       | 77.41             | 329.77            | ok     |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0433         | 0.0202       | 77.41             | 5.63              | ok     |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1075         | 0.1986       | 77.41             | 8.55              | ok     |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1196         | 0.3203       | 77.41             | 1560.12           | ok     |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 0.5887         | 3.0520       | 77.41             | 194.40            | ok     |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.0684         | 0.2854       | 77.41             | 27.12             | ok     |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1377         | 0.3303       | 77.41             | 1006.52           | ok     |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.1837         | 0.1842       | 77.41             | 356.35            | ok     |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0507         | 0.3250       | 77.41             | 13.96             | ok     |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0844         | 0.0014       | 77.41             | 6.72              | ok     |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1018         | 0.0051       | 77.41             | 1468.12           | ok     |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.5625         | 0.0497       | 77.41             | 169.93            | ok     |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.9628         | 0.0028       | 77.41             | 25.73             | ok     |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1108         | 0.0065       | 77.41             | 774.77            | ok     |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.2280         | 0.0025       | 77.41             | 332.72            | ok     |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0337         | 0.0035       | 77.41             | 7.84              | ok     |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0737         | 0.0678       | 77.41             | 5.99              | ok     |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1071         | 0.0418       | 77.41             | 1576.12           | ok     |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.5499         | 1.0023       | 77.41             | 173.37            | ok     |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0295         | 0.0966       | 77.41             | 27.70             | ok     |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1398         | 0.1997       | 77.41             | 1005.48           | ok     |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.3192         | 0.0499       | 77.41             | 340.98            | ok     |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0333         | 0.0203       | 77.41             | 10.08             | ok     |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1721         | 1.4103       | 77.41             | 9.04              | ok     |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1480         | 1.5880       | 77.41             | 1556.12           | ok     |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.8248         | 17.8803      | 77.41             | 191.59            | ok     |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.1588         | 1.2685       | 77.41             | 24.66             | ok     |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1483         | 3.9313       | 77.41             | 1010.02           | ok     |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.2815         | 1.1965       | 77.41             | 357.46            | ok     |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0408         | 1.1861       | 77.41             | 7.80              | ok     |
