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
| selected_benchmarks    | binarytrees                                                                                                                                                     |
| cpu_affinity           | -                                                                                                                                                               |
| scoring_balance        | equal category weight, benchmark weights normalized within category                                                                                             |
| link_policy            | toolchain-default release mode (mixed linkage; see entry metadata)                                                                                              |
| entries                | 1                                                                                                                                                               |
| benchmarks             | 1                                                                                                                                                               |
| cpu_model              | AMD Ryzen 9 5900HS with Radeon Graphics                                                                                                                         |
| logical_cores          | 16                                                                                                                                                              |
| memory_gib             | 15.02                                                                                                                                                           |
| peak_memory_mode       | cgroupv2-memory.peak                                                                                                                                            |
| peak_memory_detail     | /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-cosmic-com.system76.CosmicAppList-2600.scope/memory.peak                              |
| kernel                 | 7.0.10-35.stable                                                                                                                                                |
| gcc                    | gcc (AerynOS) 16.1.1 20260505                                                                                                                                   |
| clang                  | clang version 22.1.6 (AerynOS)                                                                                                                                  |
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
| sarif (stage0/native) | sarifc   | native  | -       | -        | 0.00                     |

## Entry Policies

| Entry                 | Build Profile | Low-Burden Optimizations                                                                                                                                  |
| --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sarif (stage0/native) | stage0-native | native executable emitted through sarifc build; stdout result mode for benchmark output parity; retained benchmark inputs declared in per-benchmark specs |

## Source Concision

| Entry                 | Benchmarks | Source Lines | Source Chars | Norm Lines | Norm Chars |
| --------------------- | ---------- | ------------ | ------------ | ---------- | ---------- |
| sarif (stage0/native) | 1          | 100          | 2743         | 1.0000     | 1.0000     |

## Benchmark Coverage

| Benchmark   | Category   | Base Wt | Effective Wt | Capabilities                                | Unique Coverage                             | Retained For                                                                                   |
| ----------- | ---------- | ------- | ------------ | ------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| binarytrees | Allocation | 1.00    | 1.0000       | allocation, pointer_chasing, tree_recursion | allocation, pointer_chasing, tree_recursion | Only benchmark centered on allocation-heavy pointer traversal and recursive tree construction. |

## Benchmarks

| Benchmark   | Algorithm                                       | Time           | Space            | Output Contract      | Fairness Notes                                                            |
| ----------- | ----------------------------------------------- | -------------- | ---------------- | -------------------- | ------------------------------------------------------------------------- |
| binarytrees | bottom-up binary tree construction and checksum | O(nodes built) | O(max tree size) | exact multiline text | Same tree/check workload; memory-management costs remain language-native. |

## Excluded

| Excluded From Score | Reason     |
| ------------------- | ---------- |
| binarytrees         | build-fail |

## Interpretation

This report is non-comparative: no scored entries were available, so ranking views are omitted.

## Results

| Benchmark   | Entry                 | Input | Output | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status     |
| ----------- | --------------------- | ----- | ------ | -------------- | ------------ | ----------------- | ----------------- | ---------- |
| binarytrees | sarif (stage0/native) | 20    | -      | 0.0108         | 0.0000       | 0.00              | 0.00              | build-fail |

## Mismatches

| Benchmark   | Entry                 | Output | Reference | Status     |
| ----------- | --------------------- | ------ | --------- | ---------- |
| binarytrees | sarif (stage0/native) | -      | -         | build-fail |
