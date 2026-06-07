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

## Decision Profiles

| Profile      | Leader                | Runner-Up             | Third             | Intent                                                               |
| ------------ | --------------------- | --------------------- | ----------------- | -------------------------------------------------------------------- |
| Balanced     | sarif (stage0/native) | c (clang)             | rust (rustc/llvm) | Default composite across speed, memory, build time, and binary size. |
| Speed First  | sarif (stage0/native) | rust (rustc/llvm)     | c (clang)         | Throughput or latency matters most.                                  |
| Memory First | c (clang)             | sarif (stage0/native) | go (gc)           | RAM pressure matters most.                                           |
| Build First  | sarif (stage0/native) | c (clang)             | go (gc)           | Build and iteration cost matter most.                                |
| Deploy First | sarif (stage0/native) | c (clang)             | nim (clang)       | Artifact footprint matters alongside runtime.                        |

## Categories

| Entry                 | Numeric | Allocation | Hash/String | Text/Streaming | Parse/Aggregate | Join/Aggregate | Sort/Aggregate | Overall |
| --------------------- | ------- | ---------- | ----------- | -------------- | --------------- | -------------- | -------------- | ------- |
| sarif (stage0/native) | 0.8296  | 0.2069     | 0.9252      | 0.8387         | 0.9726          | 0.9723         | 0.9732         | 0.8169  |
| c (clang)             | 0.9085  | 0.4214     | 0.9285      | 0.7334         | 0.4353          | 0.5728         | 0.4204         | 0.6315  |
| rust (rustc/llvm)     | 0.8232  | 0.2278     | 0.7624      | 0.7985         | 0.5976          | 0.5097         | 0.4220         | 0.5916  |
| go (gc)               | 0.6683  | 0.3299     | 0.5411      | 0.6768         | 0.6516          | 0.4820         | 0.4916         | 0.5487  |
| nim (clang)           | 0.7295  | 0.4031     | 0.6175      | 0.5877         | 0.3377          | 0.3430         | 0.3144         | 0.4761  |
| ocaml (native)        | 0.5499  | 0.7683     | 0.3446      | 0.5585         | 0.2859          | 0.2662         | 0.2545         | 0.4325  |
| moonbit (native)      | 0.6669  | 0.8572     | 0.4164      | 0.4068         | 0.2317          | 0.1488         | 0.2411         | 0.4241  |

## Summary

| Overall | Entry                 | Score  | Speed  | Memory | Build  | Size   |
| ------- | --------------------- | ------ | ------ | ------ | ------ | ------ |
| 1       | sarif (stage0/native) | 0.8169 | 0.8028 | 0.8336 | 1.0000 | 0.5683 |
| 2       | c (clang)             | 0.6315 | 0.5504 | 0.9647 | 0.3075 | 1.0000 |
| 3       | rust (rustc/llvm)     | 0.5916 | 0.6387 | 0.8692 | 0.0159 | 0.0202 |
| 4       | go (gc)               | 0.5487 | 0.5154 | 0.9504 | 0.2342 | 0.0045 |
| 5       | nim (clang)           | 0.4761 | 0.4390 | 0.8769 | 0.0351 | 0.2382 |
| 6       | ocaml (native)        | 0.4325 | 0.3410 | 0.9335 | 0.2385 | 0.0071 |
| 7       | moonbit (native)      | 0.4241 | 0.3618 | 0.9158 | 0.0463 | 0.0232 |

_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._

## Speed View

| Speed Rank | Entry                 | Speed Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 0.8028      | 0.8169          |
| 2          | rust (rustc/llvm)     | 0.6387      | 0.5916          |
| 3          | c (clang)             | 0.5504      | 0.6315          |
| 4          | go (gc)               | 0.5154      | 0.5487          |
| 5          | nim (clang)           | 0.4390      | 0.4761          |
| 6          | moonbit (native)      | 0.3618      | 0.4241          |
| 7          | ocaml (native)        | 0.3410      | 0.4325          |

## Memory View

| Memory Rank | Entry                 | Memory Score | Composite Score |
| ----------- | --------------------- | ------------ | --------------- |
| 1           | c (clang)             | 0.9647       | 0.6315          |
| 2           | go (gc)               | 0.9504       | 0.5487          |
| 3           | ocaml (native)        | 0.9335       | 0.4325          |
| 4           | moonbit (native)      | 0.9158       | 0.4241          |
| 5           | nim (clang)           | 0.8769       | 0.4761          |
| 6           | rust (rustc/llvm)     | 0.8692       | 0.5916          |
| 7           | sarif (stage0/native) | 0.8336       | 0.8169          |

## Build View

| Build Rank | Entry                 | Build Score | Composite Score |
| ---------- | --------------------- | ----------- | --------------- |
| 1          | sarif (stage0/native) | 1.0000      | 0.8169          |
| 2          | c (clang)             | 0.3075      | 0.6315          |
| 3          | ocaml (native)        | 0.2385      | 0.4325          |
| 4          | go (gc)               | 0.2342      | 0.5487          |
| 5          | moonbit (native)      | 0.0463      | 0.4241          |
| 6          | nim (clang)           | 0.0351      | 0.4761          |
| 7          | rust (rustc/llvm)     | 0.0159      | 0.5916          |

## Size View

| Size Rank | Entry                 | Size Score | Composite Score |
| --------- | --------------------- | ---------- | --------------- |
| 1         | c (clang)             | 1.0000     | 0.6315          |
| 2         | sarif (stage0/native) | 0.5683     | 0.8169          |
| 3         | nim (clang)           | 0.2382     | 0.4761          |
| 4         | moonbit (native)      | 0.0232     | 0.4241          |
| 5         | rust (rustc/llvm)     | 0.0202     | 0.5916          |
| 6         | ocaml (native)        | 0.0071     | 0.4325          |
| 7         | go (gc)               | 0.0045     | 0.5487          |

## Results

| Benchmark    | Entry                 | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | --------------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (clang)             | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2411         | 8.5318       | 130.12            | 5.73              | ok     |
| binarytrees  | go (gc)               | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 4.3750         | 9.3353       | 130.20            | 1560.12           | ok     |
| binarytrees  | moonbit (native)      | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.0192         | 2.5519       | 98.01             | 302.43            | ok     |
| binarytrees  | nim (clang)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.5469         | 5.2984       | 261.77            | 26.00             | ok     |
| binarytrees  | ocaml (native)        | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2273         | 2.8227       | 128.55            | 1006.36           | ok     |
| binarytrees  | rust (rustc/llvm)     | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.1534         | 11.1305      | 258.11            | 329.78            | ok     |
| binarytrees  | sarif (stage0/native) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0634         | 22.9779      | 2838.11           | 10.28             | ok     |
| csvgroupby   | c (clang)             | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.4200         | 0.0530       | 27.09             | 6.30              | ok     |
| csvgroupby   | go (gc)               | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.4931         | 0.0206       | 27.09             | 1584.12           | ok     |
| csvgroupby   | moonbit (native)      | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.1866         | 0.3568       | 27.09             | 301.22            | ok     |
| csvgroupby   | nim (clang)           | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 1.4386         | 0.0732       | 27.09             | 31.62             | ok     |
| csvgroupby   | ocaml (native)        | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.2595         | 0.1471       | 27.09             | 1010.14           | ok     |
| csvgroupby   | rust (rustc/llvm)     | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 3.1887         | 0.0229       | 27.09             | 345.23            | ok     |
| csvgroupby   | sarif (stage0/native) | fixture:orders-120000.csv        | sha256:b7ce6bd0a0cc01ea                                                  | 0.0629         | 0.0139       | 27.09             | 13.94             | ok     |
| fasta        | c (clang)             | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1187         | 0.0308       | 27.69             | 7.51              | ok     |
| fasta        | go (gc)               | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1662         | 0.0405       | 33.78             | 1556.12           | ok     |
| fasta        | moonbit (native)      | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.9248         | 0.0720       | 36.23             | 304.71            | ok     |
| fasta        | nim (clang)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.2727         | 0.0336       | 38.81             | 27.66             | ok     |
| fasta        | ocaml (native)        | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1688         | 0.0533       | 41.36             | 1015.55           | ok     |
| fasta        | rust (rustc/llvm)     | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.6902         | 0.0326       | 43.65             | 332.72            | ok     |
| fasta        | sarif (stage0/native) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.0442         | 0.0317       | 46.02             | 10.49             | ok     |
| joinagg      | c (clang)             | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.1184         | 0.1100       | 27.69             | 8.02              | ok     |
| joinagg      | go (gc)               | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.2044         | 0.1204       | 27.97             | 1592.12           | ok     |
| joinagg      | moonbit (native)      | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.1035         | 0.8339       | 52.38             | 314.12            | ok     |
| joinagg      | nim (clang)           | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 1.4232         | 0.2134       | 30.54             | 40.89             | ok     |
| joinagg      | ocaml (native)        | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.2191         | 0.5278       | 29.55             | 1010.52           | ok     |
| joinagg      | rust (rustc/llvm)     | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 3.2216         | 0.0965       | 31.20             | 363.07            | ok     |
| joinagg      | sarif (stage0/native) | fixture:users-events-180000.txt  | sha256:37c7ac2d5630fe43                                                  | 0.0398         | 0.0489       | 27.69             | 17.98             | ok     |
| knucleotide  | c (clang)             | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1376         | 0.0056       | 48.54             | 9.19              | ok     |
| knucleotide  | go (gc)               | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1077         | 0.0120       | 48.54             | 1580.12           | ok     |
| knucleotide  | moonbit (native)      | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.0423         | 0.0173       | 48.54             | 306.09            | ok     |
| knucleotide  | nim (clang)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.2421         | 0.0091       | 48.54             | 32.46             | ok     |
| knucleotide  | ocaml (native)        | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1819         | 0.0299       | 48.54             | 1065.58           | ok     |
| knucleotide  | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.7012         | 0.0065       | 48.54             | 374.44            | ok     |
| knucleotide  | sarif (stage0/native) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.0392         | 0.0062       | 48.54             | 14.34             | ok     |
| mandelbrot   | c (clang)             | 512                              | sha256:e41a9386e912a316                                                  | 0.0933         | 0.0169       | 48.54             | 5.84              | ok     |
| mandelbrot   | go (gc)               | 512                              | sha256:e41a9386e912a316                                                  | 0.1013         | 0.0201       | 48.54             | 1548.12           | ok     |
| mandelbrot   | moonbit (native)      | 512                              | sha256:e41a9386e912a316                                                  | 0.9805         | 0.0164       | 48.54             | 300.24            | ok     |
| mandelbrot   | nim (clang)           | 512                              | sha256:e41a9386e912a316                                                  | 1.2610         | 0.0166       | 48.54             | 23.77             | ok     |
| mandelbrot   | ocaml (native)        | 512                              | sha256:e41a9386e912a316                                                  | 0.1582         | 0.0227       | 48.54             | 1005.30           | ok     |
| mandelbrot   | rust (rustc/llvm)     | 512                              | sha256:e41a9386e912a316                                                  | 2.6487         | 0.0170       | 48.54             | 330.03            | ok     |
| mandelbrot   | sarif (stage0/native) | 512                              | sha256:e41a9386e912a316                                                  | 0.0434         | 0.0179       | 48.54             | 7.23              | ok     |
| nbody        | c (clang)             | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1431         | 0.2201       | 48.54             | 8.52              | ok     |
| nbody        | go (gc)               | 5000000                          | -0.169075164 / -0.169083134                                              | 0.2059         | 0.3780       | 48.54             | 1560.12           | ok     |
| nbody        | moonbit (native)      | 5000000                          | -0.169075164 / -0.169083134                                              | 1.2199         | 0.4126       | 48.54             | 305.99            | ok     |
| nbody        | nim (clang)           | 5000000                          | -0.169075164 / -0.169083134                                              | 1.3268         | 0.3229       | 48.54             | 27.09             | ok     |
| nbody        | ocaml (native)        | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1815         | 0.3696       | 48.54             | 1006.48           | ok     |
| nbody        | rust (rustc/llvm)     | 5000000                          | -0.169075164 / -0.169083134                                              | 2.5701         | 0.1933       | 48.54             | 356.63            | ok     |
| nbody        | sarif (stage0/native) | 5000000                          | -0.169075164 / -0.169083134                                              | 0.0575         | 0.3480       | 48.54             | 16.54             | ok     |
| primecount   | c (clang)             | 50000                            | 5133                                                                     | 0.0799         | 0.0027       | 48.54             | 5.04              | ok     |
| primecount   | go (gc)               | 50000                            | 5133                                                                     | 0.1120         | 0.0055       | 48.54             | 1548.12           | ok     |
| primecount   | moonbit (native)      | 50000                            | 5133                                                                     | 0.9837         | 0.0025       | 48.54             | 299.99            | ok     |
| primecount   | nim (clang)           | 50000                            | 5133                                                                     | 1.1818         | 0.0038       | 48.54             | 22.77             | ok     |
| primecount   | ocaml (native)        | 50000                            | 5133                                                                     | 0.1732         | 0.0055       | 48.54             | 1005.27           | ok     |
| primecount   | rust (rustc/llvm)     | 50000                            | 5133                                                                     | 2.6432         | 0.0026       | 48.54             | 329.10            | ok     |
| primecount   | sarif (stage0/native) | 50000                            | 5133                                                                     | 0.0370         | 0.0032       | 48.54             | 7.81              | ok     |
| revcomp      | c (clang)             | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1096         | 0.0092       | 48.54             | 6.70              | ok     |
| revcomp      | go (gc)               | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1022         | 0.0052       | 48.54             | 1468.12           | ok     |
| revcomp      | moonbit (native)      | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.7780         | 0.0131       | 48.54             | 296.34            | ok     |
| revcomp      | nim (clang)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.0629         | 0.0110       | 48.54             | 25.70             | ok     |
| revcomp      | ocaml (native)        | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1195         | 0.0064       | 48.54             | 774.73            | ok     |
| revcomp      | rust (rustc/llvm)     | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.6590         | 0.0034       | 48.54             | 332.84            | ok     |
| revcomp      | sarif (stage0/native) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0388         | 0.0049       | 48.54             | 9.66              | ok     |
| sortuniq     | c (clang)             | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1022         | 0.0904       | 48.54             | 5.97              | ok     |
| sortuniq     | go (gc)               | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.1561         | 0.0459       | 48.54             | 1576.12           | ok     |
| sortuniq     | moonbit (native)      | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.8641         | 0.3431       | 48.54             | 299.03            | ok     |
| sortuniq     | nim (clang)           | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 1.2319         | 0.1228       | 48.54             | 27.66             | ok     |
| sortuniq     | ocaml (native)        | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.2050         | 0.3300       | 48.54             | 1005.45           | ok     |
| sortuniq     | rust (rustc/llvm)     | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 2.9378         | 0.0563       | 48.54             | 341.17            | ok     |
| sortuniq     | sarif (stage0/native) | fixture:words-250000.txt         | sha256:6b28b0e803b80ff3                                                  | 0.0341         | 0.0191       | 48.54             | 12.85             | ok     |
| spectralnorm | c (clang)             | 5000                             | 1.274224153                                                              | 0.1526         | 1.2050       | 48.54             | 9.02              | ok     |
| spectralnorm | go (gc)               | 5000                             | 1.274224153                                                              | 0.0993         | 1.4156       | 48.54             | 1560.12           | ok     |
| spectralnorm | moonbit (native)      | 5000                             | 1.274224153                                                              | 0.9478         | 3.2662       | 48.54             | 305.38            | ok     |
| spectralnorm | nim (clang)           | 5000                             | 1.274224153                                                              | 1.2447         | 1.3287       | 48.54             | 24.63             | ok     |
| spectralnorm | ocaml (native)        | 5000                             | 1.274224153                                                              | 0.1513         | 4.3741       | 48.54             | 1009.98           | ok     |
| spectralnorm | rust (rustc/llvm)     | 5000                             | 1.274224153                                                              | 3.3411         | 1.3637       | 48.54             | 357.77            | ok     |
| spectralnorm | sarif (stage0/native) | 5000                             | 1.274224153                                                              | 0.0548         | 1.5256       | 48.54             | 10.20             | ok     |
