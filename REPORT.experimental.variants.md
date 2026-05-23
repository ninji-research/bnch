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
| experimental_entries   | yes                                                                                                                                                             |
| selected_benchmarks    | binarytrees,csvgroupby,joinagg,fasta,mandelbrot,primecount,spectralnorm,nbody,knucleotide,revcomp,sortuniq                                                      |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 11                                                                                                                                                              |
| benchmarks             | 11                                                                                                                                                              |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.02                                                                                                                                                           |
| peak_memory_mode       | ru_maxrss                                                                                                                                                       |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/session-3.scope/memory.peak unavailable for reset (Permission denied)                                                 |
| kernel                 | 7.0.6-32.stable                                                                                                                                                 |
| gcc                    | gcc (AerynOS) 16.1.1 20260505                                                                                                                                   |
| clang                  | clang version 22.1.5 (AerynOS)                                                                                                                                  |
| go                     | go version go1.26.3 linux/amd64                                                                                                                                 |
| rustc                  | rustc 1.95.0 (59807616e 2026-04-14)                                                                                                                             |
| nim                    | Nim Compiler Version 2.2.10 [Linux: amd64]                                                                                                                      |
| ocamlopt               | 5.4.1                                                                                                                                                           |
| moon                   | moon 0.1.20260512 (81d40e3 2026-05-12)                                                                                                                          |
| strip                  | GNU strip (GNU Binutils) 2.46.0                                                                                                                                 |
| sarifc                 | sarifc 0.1.0                                                                                                                                                    |

## Entries

| Entry                 | Compiler | Backend | Linkage | Stripped | Binary Size Sample (KiB) |
| --------------------- | -------- | ------- | ------- | -------- | ------------------------ |
| c (gcc)               | gcc      | native  | dynamic | yes      | 18.17                    |
| c (clang)             | clang    | native  | dynamic | yes      | 5.73                     |
| go (gc)               | go       | native  | static  | yes      | 1560.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 181.98                   |
| nim (gcc)             | gcc      | c       | dynamic | yes      | 42.52                    |
| nim (clang)           | clang    | c       | dynamic | yes      | 26.00                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.36                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 329.48                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 8.79                     |
| sarif (c/gcc)         | sarifc   | c       | -       | -        | 0.00                     |
| sarif (wasm/node)     | sarifc   | wasm    | -       | -        | 0.14                     |

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
| sarif (c/gcc)         | stage0-native      | native executable emitted through sarifc build; stdout result mode for benchmark output parity; retained benchmark inputs declared in per-benchmark specs                       |
| sarif (wasm/node)     | stage0-native      | native executable emitted through sarifc build; stdout result mode for benchmark output parity; retained benchmark inputs declared in per-benchmark specs                       |

## Source Concision

| Entry                 | Benchmarks | Source Lines | Source Chars | Norm Lines | Norm Chars |
| --------------------- | ---------- | ------------ | ------------ | ---------- | ---------- |
| nim (clang)           | 11         | 579          | 16184        | 1.0000     | 1.0000     |
| nim (gcc)             | 11         | 579          | 16184        | 1.0000     | 1.0000     |
| go (gc)               | 11         | 884          | 18145        | 0.6550     | 0.8919     |
| ocaml (native)        | 11         | 648          | 19155        | 0.8935     | 0.8449     |
| rust (rustc/llvm)     | 11         | 819          | 22420        | 0.7070     | 0.7219     |
| c (clang)             | 11         | 1074         | 28956        | 0.5391     | 0.5589     |
| c (gcc)               | 11         | 1074         | 28956        | 0.5391     | 0.5589     |
| moonbit (native)      | 11         | 1246         | 31241        | 0.4647     | 0.5180     |
| sarif (c/gcc)         | 11         | 979          | 35428        | 0.5914     | 0.4568     |
| sarif (stage0/native) | 11         | 979          | 35428        | 0.5914     | 0.4568     |
| sarif (wasm/node)     | 11         | 979          | 35428        | 0.5914     | 0.4568     |

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

| Excluded From Score | Reason                             |
| ------------------- | ---------------------------------- |
| binarytrees         | build-fail, mismatch, ok, run-fail |
| csvgroupby          | build-fail, ok, run-fail           |
| joinagg             | build-fail, mismatch, ok           |
| fasta               | build-fail, ok                     |
| mandelbrot          | build-fail, ok                     |
| primecount          | build-fail, ok                     |
| spectralnorm        | build-fail, ok                     |
| nbody               | build-fail, ok, run-fail           |
| knucleotide         | build-fail, ok, run-fail           |
| revcomp             | build-fail, ok, run-fail           |
| sortuniq            | build-fail, ok, run-fail           |

## Interpretation

This report is non-comparative: no scored entries were available, so ranking views are omitted.

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status     |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ---------- |
| binarytrees  | c (gcc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.3608         | 8.0423       | 130.07            | 18.17             | ok         |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1859         | 8.7572       | 130.02            | 5.73              | ok         |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 4.1790         | 9.6668       | 130.70            | 1560.12           | ok         |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.1069         | 2.5842       | 97.84             | 181.98            | ok         |
| binarytrees  | nim (gcc)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.6966         | 5.2821       | 262.01            | 42.52             | ok         |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.2655         | 5.4822       | 262.16            | 26.00             | ok         |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2168         | 2.9699       | 128.33            | 1006.36           | ok         |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.0205         | 10.9862      | 257.71            | 329.48            | ok         |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / trees of depth 4	 check: 3... | 0.0394         | 15.1699      | 5092.73           | 8.79              | mismatch   |
| binarytrees  | sarif (c/gcc)         | 20                               | -                                                                        | 0.2424         | 0.0000       | 0.00              | 0.00              | build-fail |
| binarytrees  | sarif (wasm/node)     | 20                               | -                                                                        | 0.0204         | 0.0000       | 0.00              | 0.14              | run-fail   |
| csvgroupby   | c (gcc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2376         | 0.0502       | 39.70             | 14.22             | ok         |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2100         | 0.0497       | 39.70             | 6.30              | ok         |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.4562         | 0.0254       | 39.70             | 1584.12           | ok         |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.9955         | 0.3436       | 39.70             | 177.46            | ok         |
| csvgroupby   | nim (gcc)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.7465         | 0.0653       | 39.70             | 42.55             | ok         |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.2418         | 0.0667       | 39.70             | 31.62             | ok         |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2050         | 0.1399       | 39.70             | 1010.14           | ok         |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 3.3001         | 0.0233       | 39.70             | 345.01            | ok         |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0542         | 0.0175       | 39.70             | 12.61             | ok         |
| csvgroupby   | sarif (c/gcc)         | fixture:orders-120000.csv        | -                                                                        | 0.0717         | 0.0000       | 0.00              | 0.00              | build-fail |
| csvgroupby   | sarif (wasm/node)     | fixture:orders-120000.csv        | -                                                                        | 0.0081         | 0.0000       | 0.00              | 0.14              | run-fail   |
| fasta        | c (gcc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1521         | 0.0300       | 43.30             | 14.16             | ok         |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1061         | 0.0341       | 55.53             | 7.51              | ok         |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1232         | 0.0410       | 57.82             | 1556.12           | ok         |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.0338         | 0.0724       | 65.02             | 184.27            | ok         |
| fasta        | nim (gcc)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.8025         | 0.0387       | 67.64             | 42.52             | ok         |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.2711         | 0.0365       | 69.90             | 27.66             | ok         |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1670         | 0.0546       | 72.50             | 1015.55           | ok         |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.7682         | 0.0335       | 74.92             | 332.41            | ok         |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0505         | 0.0302       | 77.30             | 9.09              | ok         |
| fasta        | sarif (c/gcc)         | 250000                           | -                                                                        | 0.0764         | 0.0000       | 0.00              | 0.00              | build-fail |
| fasta        | sarif (wasm/node)     | 250000                           | -                                                                        | 0.0185         | 0.0000       | 0.00              | 0.00              | build-fail |
| joinagg      | c (gcc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1504         | 0.1269       | 39.70             | 14.23             | ok         |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1211         | 0.1248       | 39.70             | 8.02              | ok         |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1280         | 0.1354       | 39.70             | 1592.12           | ok         |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.1795         | 0.9501       | 47.98             | 193.62            | ok         |
| joinagg      | nim (gcc)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.9607         | 0.1868       | 39.70             | 54.55             | ok         |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.3746         | 0.1777       | 39.70             | 40.89             | ok         |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1639         | 0.3193       | 39.70             | 1010.52           | ok         |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 3.0281         | 0.1160       | 39.70             | 362.85            | ok         |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0456         | 0.0552       | 39.70             | 16.66             | ok         |
| joinagg      | sarif (c/gcc)         | fixture:users-events-180000.txt  | -                                                                        | 0.0900         | 0.0000       | 0.00              | 0.00              | build-fail |
| joinagg      | sarif (wasm/node)     | fixture:users-events-180000.txt  | -                                                                        | 0.0114         | 0.0767       | 50.38             | 0.14              | mismatch   |
| knucleotide  | c (gcc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1577         | 0.0063       | 79.71             | 14.33             | ok         |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1323         | 0.0061       | 79.71             | 9.19              | ok         |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1278         | 0.0137       | 79.71             | 1580.12           | ok         |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.9853         | 0.0181       | 79.71             | 182.34            | ok         |
| knucleotide  | nim (gcc)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.8335         | 0.0069       | 79.71             | 50.49             | ok         |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.2478         | 0.0093       | 79.71             | 32.46             | ok         |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1756         | 0.0291       | 79.71             | 1065.58           | ok         |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.9137         | 0.0063       | 79.71             | 374.28            | ok         |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0404         | 0.0052       | 79.71             | 13.07             | ok         |
| knucleotide  | sarif (c/gcc)         | fixture:knucleotide-250000.fasta | -                                                                        | 0.0907         | 0.0000       | 0.00              | 0.00              | build-fail |
| knucleotide  | sarif (wasm/node)     | fixture:knucleotide-250000.fasta | -                                                                        | 0.0135         | 0.0000       | 0.00              | 0.14              | run-fail   |
| mandelbrot   | c (gcc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.0975         | 0.0147       | 79.71             | 14.14             | ok         |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.1007         | 0.0153       | 79.71             | 5.84              | ok         |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1140         | 0.0206       | 79.71             | 1548.12           | ok         |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.9786         | 0.0179       | 79.71             | 179.80            | ok         |
| mandelbrot   | nim (gcc)             | 512                              | sha256:e41a9386e912a316                                                  | 1.5193         | 0.0152       | 79.71             | 30.46             | ok         |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.2452         | 0.0154       | 79.71             | 23.77             | ok         |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1563         | 0.0193       | 79.71             | 1005.30           | ok         |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.6624         | 0.0169       | 79.71             | 329.73            | ok         |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0339         | 0.0172       | 79.71             | 5.97              | ok         |
| mandelbrot   | sarif (c/gcc)         | 512                              | -                                                                        | 0.0749         | 0.0000       | 0.00              | 0.00              | build-fail |
| mandelbrot   | sarif (wasm/node)     | 512                              | -                                                                        | 0.0133         | 0.0000       | 0.00              | 0.00              | build-fail |
| nbody        | c (gcc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1408         | 0.2659       | 79.71             | 14.15             | ok         |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1334         | 0.2146       | 79.71             | 8.52              | ok         |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1187         | 0.3537       | 79.71             | 1560.12           | ok         |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 1.0219         | 0.3874       | 79.71             | 185.55            | ok         |
| nbody        | nim (gcc)             | 5000000                          | -0.169075164 / -0.169083134                                              | 1.5666         | 0.2928       | 79.71             | 34.46             | ok         |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.3136         | 0.3224       | 79.71             | 27.09             | ok         |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1653         | 0.3807       | 79.71             | 1006.48           | ok         |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.7553         | 0.2080       | 79.71             | 356.32            | ok         |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0606         | 0.3320       | 79.71             | 14.78             | ok         |
| nbody        | sarif (c/gcc)         | 5000000                          | -                                                                        | 0.0821         | 0.0000       | 0.00              | 0.00              | build-fail |
| nbody        | sarif (wasm/node)     | 5000000                          | -                                                                        | 0.0123         | 0.0000       | 0.00              | 0.13              | run-fail   |
| primecount   | c (gcc)               | 50000                            | 5133                                                                     | 0.1017         | 0.0026       | 79.71             | 14.14             | ok         |
| primecount   | c (clang)             | 50000                            | 5133                                                                     | 0.0834         | 0.0025       | 79.71             | 5.04              | ok         |
| primecount   | go (gc)               | 50000                            | 5133                                                                     | 0.1152         | 0.0048       | 79.71             | 1548.12           | ok         |
| primecount   | moonbit (native)      | 50000                            | 5133                                                                     | 1.0098         | 0.0072       | 79.71             | 179.55            | ok         |
| primecount   | nim (gcc)             | 50000                            | 5133                                                                     | 1.4976         | 0.0027       | 79.71             | 30.46             | ok         |
| primecount   | nim (clang)           | 50000                            | 5133                                                                     | 1.2301         | 0.0027       | 79.71             | 22.77             | ok         |
| primecount   | ocaml (native)        | 50000                            | 5133                                                                     | 0.1521         | 0.0046       | 79.71             | 1005.27           | ok         |
| primecount   | rust (rustc/llvm)     | 50000                            | 5133                                                                     | 2.6308         | 0.0023       | 79.71             | 328.80            | ok         |
| primecount   | sarif (stage0/native) | 50000                            | 5133                                                                     | 0.0331         | 0.0032       | 79.71             | 6.56              | ok         |
| primecount   | sarif (c/gcc)         | 50000                            | -                                                                        | 0.0709         | 0.0000       | 0.00              | 0.00              | build-fail |
| primecount   | sarif (wasm/node)     | 50000                            | -                                                                        | 0.0119         | 0.0000       | 0.00              | 0.00              | build-fail |
| revcomp      | c (gcc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1287         | 0.0014       | 79.71             | 14.19             | ok         |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1088         | 0.0018       | 79.71             | 6.70              | ok         |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1173         | 0.0057       | 79.71             | 1468.12           | ok         |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.8444         | 0.0148       | 79.71             | 172.59            | ok         |
| revcomp      | nim (gcc)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.4613         | 0.0028       | 79.71             | 34.49             | ok         |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.0861         | 0.0031       | 79.71             | 25.70             | ok         |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1414         | 0.0073       | 79.71             | 774.73            | ok         |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.7443         | 0.0028       | 79.71             | 332.69            | ok         |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0359         | 0.0042       | 79.71             | 8.35              | ok         |
| revcomp      | sarif (c/gcc)         | fixture:knucleotide-250000.fasta | -                                                                        | 0.0749         | 0.0000       | 0.00              | 0.00              | build-fail |
| revcomp      | sarif (wasm/node)     | fixture:knucleotide-250000.fasta | -                                                                        | 0.0080         | 0.0000       | 0.00              | 0.14              | run-fail   |
| sortuniq     | c (gcc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1368         | 0.0798       | 79.71             | 14.21             | ok         |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0837         | 0.0773       | 79.71             | 5.97              | ok         |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1267         | 0.0462       | 79.71             | 1576.12           | ok         |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.8963         | 0.3202       | 79.71             | 175.27            | ok         |
| sortuniq     | nim (gcc)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.5731         | 0.1183       | 79.71             | 34.49             | ok         |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.1493         | 0.1117       | 79.71             | 27.66             | ok         |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1604         | 0.2278       | 79.71             | 1005.45           | ok         |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.6972         | 0.0585       | 79.71             | 340.95            | ok         |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0360         | 0.0203       | 79.71             | 11.52             | ok         |
| sortuniq     | sarif (c/gcc)         | fixture:words-250000.txt         | -                                                                        | 0.0732         | 0.0000       | 0.00              | 0.00              | build-fail |
| sortuniq     | sarif (wasm/node)     | fixture:words-250000.txt         | -                                                                        | 0.0090         | 0.0000       | 0.00              | 0.14              | run-fail   |
| spectralnorm | c (gcc)               | 5000                             | 1.274224153                                                              | 0.2016         | 0.7993       | 79.71             | 14.16             | ok         |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1681         | 1.2347       | 79.71             | 9.02              | ok         |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1200         | 1.4098       | 79.71             | 1560.12           | ok         |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 1.0652         | 3.2353       | 79.71             | 184.93            | ok         |
| spectralnorm | nim (gcc)             | 5000                             | 1.274224153                                                              | 1.6133         | 1.3125       | 79.71             | 34.46             | ok         |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.2974         | 1.3504       | 79.71             | 24.63             | ok         |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1737         | 4.2990       | 79.71             | 1009.98           | ok         |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.7523         | 1.2920       | 79.71             | 357.43            | ok         |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0356         | 1.3508       | 79.71             | 8.94              | ok         |
| spectralnorm | sarif (c/gcc)         | 5000                             | -                                                                        | 0.0784         | 0.0000       | 0.00              | 0.00              | build-fail |
| spectralnorm | sarif (wasm/node)     | 5000                             | -                                                                        | 0.0134         | 0.0000       | 0.00              | 0.00              | build-fail |

## Mismatches

| Benchmark    | Entry                 | Output                                                                   | Reference                                                                | Status     |
| ------------ | --------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ---------- |
| binarytrees  | sarif (stage0/native) | stretch tree of depth 21	 check: 4194303 / trees of depth 4	 check: 3... | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | mismatch   |
| binarytrees  | sarif (c/gcc)         | -                                                                        | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | build-fail |
| binarytrees  | sarif (wasm/node)     | -                                                                        | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | run-fail   |
| csvgroupby   | sarif (c/gcc)         | -                                                                        | sha256:b7ce6bd0a0cc01ea                                                  | build-fail |
| csvgroupby   | sarif (wasm/node)     | -                                                                        | sha256:b7ce6bd0a0cc01ea                                                  | run-fail   |
| joinagg      | sarif (c/gcc)         | -                                                                        | sha256:37c7ac2d5630fe43                                                  | build-fail |
| joinagg      | sarif (wasm/node)     | -                                                                        | sha256:37c7ac2d5630fe43                                                  | mismatch   |
| fasta        | sarif (c/gcc)         | -                                                                        | sha256:dfd37a44ede2e23f                                                  | build-fail |
| fasta        | sarif (wasm/node)     | -                                                                        | sha256:dfd37a44ede2e23f                                                  | build-fail |
| mandelbrot   | sarif (c/gcc)         | -                                                                        | sha256:e41a9386e912a316                                                  | build-fail |
| mandelbrot   | sarif (wasm/node)     | -                                                                        | sha256:e41a9386e912a316                                                  | build-fail |
| primecount   | sarif (c/gcc)         | -                                                                        | 5133                                                                     | build-fail |
| primecount   | sarif (wasm/node)     | -                                                                        | 5133                                                                     | build-fail |
| spectralnorm | sarif (c/gcc)         | -                                                                        | 1.274224153                                                              | build-fail |
| spectralnorm | sarif (wasm/node)     | -                                                                        | 1.274224153                                                              | build-fail |
| nbody        | sarif (c/gcc)         | -                                                                        | -0.169075164 / -0.169083134                                              | build-fail |
| nbody        | sarif (wasm/node)     | -                                                                        | -0.169075164 / -0.169083134                                              | run-fail   |
| knucleotide  | sarif (c/gcc)         | -                                                                        | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | build-fail |
| knucleotide  | sarif (wasm/node)     | -                                                                        | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | run-fail   |
| revcomp      | sarif (c/gcc)         | -                                                                        | sha256:14899a73679b1d83                                                  | build-fail |
| revcomp      | sarif (wasm/node)     | -                                                                        | sha256:14899a73679b1d83                                                  | run-fail   |
| sortuniq     | sarif (c/gcc)         | -                                                                        | sha256:6b28b0e803b80ff3                                                  | build-fail |
| sortuniq     | sarif (wasm/node)     | -                                                                        | sha256:6b28b0e803b80ff3                                                  | run-fail   |
