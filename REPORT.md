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
| c (clang)             | clang    | native  | dynamic | yes      | 5.73                     |
| go (gc)               | go       | native  | static  | yes      | 1560.12                  |
| moonbit (native)      | moon     | native  | dynamic | yes      | 181.98                   |
| nim (clang)           | clang    | c       | dynamic | yes      | 26.00                    |
| ocaml (native)        | ocamlopt | native  | dynamic | yes      | 1006.36                  |
| rust (rustc/llvm)     | rustc    | llvm    | dynamic | yes      | 329.48                   |
| sarif (stage0/native) | sarifc   | native  | dynamic | yes      | 9.17                     |

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
| moonbit (native)      | 11         | 1246         | 31241        | 0.4647     | 0.5180     |
| sarif (stage0/native) | 11         | 979          | 35452        | 0.5914     | 0.4565     |

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
| sarif (stage0/native) | 0.8102  | 0.7999     | 0.9866      | 0.7664         | 0.9776          | 0.9794         | 0.9789         | 0.8998  |
| c (clang)             | 0.8990  | 0.4247     | 0.8538      | 0.8983         | 0.5266          | 0.5693         | 0.4307         | 0.6575  |
| rust (rustc/llvm)     | 0.8221  | 0.2160     | 0.7272      | 0.6827         | 0.7546          | 0.5627         | 0.4172         | 0.5975  |
| go (gc)               | 0.6508  | 0.3085     | 0.4919      | 0.5527         | 0.7195          | 0.5143         | 0.4967         | 0.5335  |
| nim (clang)           | 0.7775  | 0.3522     | 0.6561      | 0.6582         | 0.4010          | 0.3859         | 0.3234         | 0.5077  |
| ocaml (native)        | 0.5551  | 0.6939     | 0.3439      | 0.4724         | 0.3077          | 0.3394         | 0.2779         | 0.4272  |
| moonbit (native)      | 0.5472  | 0.8550     | 0.3928      | 0.3629         | 0.2417          | 0.2296         | 0.2409         | 0.4100  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.8998 | 0.8764 | 0.9814 | 1.0000 | 0.6781 |
| 2       | c (clang)             | 0.6575 | 0.5809 | 0.9643 | 0.3709 | 0.9986 |
| 3       | rust (rustc/llvm)     | 0.5975 | 0.6404 | 0.8946 | 0.0132 | 0.0202 |
| 4       | go (gc)               | 0.5335 | 0.4902 | 0.9587 | 0.2288 | 0.0045 |
| 5       | nim (clang)           | 0.5077 | 0.4819 | 0.8985 | 0.0289 | 0.2377 |
| 6       | ocaml (native)        | 0.4272 | 0.3297 | 0.9515 | 0.2221 | 0.0071 |
| 7       | moonbit (native)      | 0.4100 | 0.3205 | 0.9804 | 0.0364 | 0.0387 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.8764      | 0.8998          |
| 2          | rust (rustc/llvm)     | 0.6404      | 0.5975          |
| 3          | c (clang)             | 0.5809      | 0.6575          |
| 4          | go (gc)               | 0.4902      | 0.5335          |
| 5          | nim (clang)           | 0.4819      | 0.5077          |
| 6          | ocaml (native)        | 0.3297      | 0.4272          |
| 7          | moonbit (native)      | 0.3205      | 0.4100          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | sarif (stage0/native) | 0.9814       | 0.8998          |
| 2           | moonbit (native)      | 0.9804       | 0.4100          |
| 3           | c (clang)             | 0.9643       | 0.6575          |
| 4           | go (gc)               | 0.9587       | 0.5335          |
| 5           | ocaml (native)        | 0.9515       | 0.4272          |
| 6           | nim (clang)           | 0.8985       | 0.5077          |
| 7           | rust (rustc/llvm)     | 0.8946       | 0.5975          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.8998          |
| 2          | c (clang)             | 0.3709      | 0.6575          |
| 3          | go (gc)               | 0.2288      | 0.5335          |
| 4          | ocaml (native)        | 0.2221      | 0.4272          |
| 5          | moonbit (native)      | 0.0364      | 0.4100          |
| 6          | nim (clang)           | 0.0289      | 0.5077          |
| 7          | rust (rustc/llvm)     | 0.0132      | 0.5975          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 0.9986     | 0.6575          |
| 2         | sarif (stage0/native) | 0.6781     | 0.8998          |
| 3         | nim (clang)           | 0.2377     | 0.5077          |
| 4         | moonbit (native)      | 0.0387     | 0.4100          |
| 5         | rust (rustc/llvm)     | 0.0202     | 0.5975          |
| 6         | ocaml (native)        | 0.0071     | 0.4272          |
| 7         | go (gc)               | 0.0045     | 0.5335          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0783         | 8.3673       | 129.93            | 5.73              | ok     |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.8839         | 9.2276       | 129.81            | 1560.12           | ok     |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.9906         | 2.2304       | 97.80             | 181.98            | ok     |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.2288         | 5.5030       | 261.96            | 26.00             | ok     |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1686         | 2.8002       | 128.23            | 1006.36           | ok     |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.5226         | 10.5125      | 257.95            | 329.48            | ok     |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0403         | 3.0934       | 97.48             | 9.17              | ok     |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0827         | 0.0492       | 33.85             | 6.30              | ok     |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2794         | 0.0229       | 33.85             | 1584.12           | ok     |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.8863         | 0.3215       | 33.85             | 177.46            | ok     |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.1851         | 0.0617       | 33.85             | 31.62             | ok     |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.1602         | 0.1344       | 33.85             | 1010.14           | ok     |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 2.6856         | 0.0210       | 33.85             | 345.01            | ok     |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0336         | 0.0179       | 33.85             | 11.41             | ok     |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1014         | 0.0338       | 44.68             | 7.51              | ok     |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1157         | 0.0385       | 48.55             | 1556.12           | ok     |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.0032         | 0.0720       | 51.07             | 184.27            | ok     |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.2493         | 0.0337       | 53.49             | 27.66             | ok     |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1569         | 0.0510       | 55.80             | 1015.55           | ok     |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.6161         | 0.0325       | 58.16             | 332.41            | ok     |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0345         | 0.0300       | 60.44             | 8.94              | ok     |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1091         | 0.1224       | 44.68             | 8.02              | ok     |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1250         | 0.1229       | 44.68             | 1592.12           | ok     |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.1022         | 0.9099       | 48.12             | 193.62            | ok     |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.4077         | 0.2021       | 44.68             | 40.89             | ok     |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1597         | 0.3007       | 44.68             | 1010.52           | ok     |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 2.8343         | 0.0973       | 44.68             | 362.85            | ok     |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0357         | 0.0540       | 44.68             | 13.66             | ok     |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1332         | 0.0060       | 63.11             | 9.19              | ok     |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1215         | 0.0132       | 63.11             | 1580.12           | ok     |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.9826         | 0.0184       | 63.11             | 182.34            | ok     |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.2577         | 0.0078       | 63.11             | 32.46             | ok     |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1647         | 0.0285       | 63.11             | 1065.58           | ok     |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.8230         | 0.0065       | 63.11             | 374.28            | ok     |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0383         | 0.0053       | 63.11             | 12.56             | ok     |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0885         | 0.0154       | 63.11             | 5.84              | ok     |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1084         | 0.0198       | 63.11             | 1548.12           | ok     |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.9397         | 0.0167       | 63.11             | 179.80            | ok     |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.1911         | 0.0144       | 63.11             | 23.77             | ok     |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1451         | 0.0182       | 63.11             | 1005.30           | ok     |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.5887         | 0.0166       | 63.11             | 329.73            | ok     |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0309         | 0.0202       | 63.11             | 5.88              | ok     |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1253         | 0.2126       | 63.11             | 8.52              | ok     |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1164         | 0.3562       | 63.11             | 1560.12           | ok     |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 1.0043         | 0.3852       | 63.11             | 185.55            | ok     |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.2478         | 0.3064       | 63.11             | 27.09             | ok     |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1706         | 0.3938       | 63.11             | 1006.48           | ok     |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.6401         | 0.1932       | 63.11             | 356.32            | ok     |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0367         | 0.3349       | 63.11             | 14.29             | ok     |
| primecount   | c (clang)             | 50000                            | 5133                                                                     | 0.0752         | 0.0024       | 63.11             | 5.04              | ok     |
| primecount   | go (gc)               | 50000                            | 5133                                                                     | 0.1022         | 0.0055       | 63.11             | 1548.12           | ok     |
| primecount   | moonbit (native)      | 50000                            | 5133                                                                     | 0.9735         | 0.0064       | 63.11             | 179.55            | ok     |
| primecount   | nim (clang)           | 50000                            | 5133                                                                     | 1.1729         | 0.0024       | 63.11             | 22.77             | ok     |
| primecount   | ocaml (native)        | 50000                            | 5133                                                                     | 0.1583         | 0.0048       | 63.11             | 1005.27           | ok     |
| primecount   | rust (rustc/llvm)     | 50000                            | 5133                                                                     | 2.6252         | 0.0023       | 63.11             | 328.80            | ok     |
| primecount   | sarif (stage0/native) | 50000                            | 5133                                                                     | 0.0293         | 0.0033       | 63.11             | 6.46              | ok     |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0975         | 0.0015       | 63.11             | 6.70              | ok     |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1053         | 0.0065       | 63.11             | 1468.12           | ok     |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.8270         | 0.0145       | 63.11             | 172.59            | ok     |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.1005         | 0.0029       | 63.11             | 25.70             | ok     |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1312         | 0.0065       | 63.11             | 774.73            | ok     |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.7040         | 0.0024       | 63.11             | 332.69            | ok     |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0339         | 0.0039       | 63.11             | 8.16              | ok     |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0831         | 0.0858       | 63.11             | 5.97              | ok     |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1294         | 0.0446       | 63.11             | 1576.12           | ok     |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.0140         | 0.3366       | 63.11             | 175.27            | ok     |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.1529         | 0.1102       | 63.11             | 27.66             | ok     |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1665         | 0.2096       | 63.11             | 1005.45           | ok     |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.7537         | 0.0562       | 63.11             | 340.95            | ok     |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0332         | 0.0186       | 63.11             | 10.33             | ok     |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1625         | 1.2501       | 63.11             | 9.02              | ok     |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.1200         | 1.4021       | 63.11             | 1560.12           | ok     |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 1.0283         | 3.3438       | 63.11             | 184.93            | ok     |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.3114         | 1.4447       | 63.11             | 24.63             | ok     |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1688         | 4.4748       | 63.11             | 1009.98           | ok     |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 2.7286         | 1.3231       | 63.11             | 357.43            | ok     |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0395         | 1.4051       | 63.11             | 8.67              | ok     |
