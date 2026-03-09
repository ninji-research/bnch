# Benchmark Report

| Setting     | Value                                                                |
| ----------- | -------------------------------------------------------------------- |
| runs        | 1                                                                    |
| warmup      | 0                                                                    |
| build_jobs  | 16                                                                   |
| link_policy | dynamic (uniform default; moon native exposes no static toggle here) |
| entries     | 7                                                                    |
| benchmarks  | 6                                                                    |
| gcc         | gcc (AerynOS) 15.2.1 20251024                                        |
| clang       | clang version 21.1.8 (AerynOS)                                       |
| rustc       | rustc 1.94.0 (4a4ef493e 2026-03-02)                                  |
| nim         | Nim Compiler Version 2.2.8 [Linux: amd64]                            |
| ocamlopt    | 5.4.1                                                                |
| moon        | moon 0.1.20260209 (b129ae2 2026-02-09)                               |
| strip       | GNU strip (GNU Binutils) 2.46.0                                      |

| Weight                 | Value |
| ---------------------- | ----- |
| metric:exec_time       | 0.60  |
| metric:peak_mem        | 0.20  |
| metric:build_time      | 0.10  |
| metric:bin_size        | 0.10  |
| benchmark:binarytrees  | 1.00  |
| benchmark:mandelbrot   | 1.00  |
| benchmark:spectralnorm | 1.00  |
| benchmark:fannkuch     | 1.00  |
| benchmark:nbody        | 1.00  |
| benchmark:startup      | 0.25  |

| Benchmark    | Algorithm                                       | Time                     | Space            | Output Contract                  | Fairness Notes                                                                     |
| ------------ | ----------------------------------------------- | ------------------------ | ---------------- | -------------------------------- | ---------------------------------------------------------------------------------- |
| binarytrees  | bottom-up binary tree construction and checksum | O(nodes built)           | O(max tree size) | exact multiline text             | Same tree/check workload; memory-management costs remain language-native.          |
| mandelbrot   | scalar Mandelbrot escape-time bitmap checksum   | O(size^2 * iter)         | O(1)             | exact integer checksum           | Input size is set to 512 because all retained implementations agree there exactly. |
| spectralnorm | power method on implicit matrix                 | O(n^2 * iterations)      | O(n)             | one float rounded to 9 decimals  | Correctness compares canonical 9-decimal output, not raw printer differences.      |
| fannkuch     | fannkuch-redux permutation flips                | O(n! * n)                | O(n)             | exact two-line text              | Same permutation-generation strategy across entries.                               |
| nbody        | 5-body symplectic advance and energy            | O(iterations * bodies^2) | O(1)             | two floats rounded to 9 decimals | Correctness compares canonical 9-decimal energies line-by-line.                    |
| startup      | process startup and hello-world print           | O(1)                     | O(1)             | exact single line                | Useful signal for runtime/toolchain startup, but intentionally low ranking impact. |

| Entry             | Compiler | Backend | Linkage | Stripped | Binary Size (KiB) |
| ----------------- | -------- | ------- | ------- | -------- | ----------------- |
| c (gcc)           | gcc      | native  | dynamic | yes      | 14.13             |
| c (clang)         | clang    | native  | dynamic | yes      | 4.55              |
| rust (rustc/llvm) | rustc    | llvm    | dynamic | yes      | 300.38            |
| nim (gcc)         | gcc      | c       | dynamic | yes      | 26.29             |
| nim (clang)       | clang    | c       | dynamic | yes      | 5.88              |
| ocaml (native)    | ocamlopt | native  | dynamic | yes      | 409.35            |
| moonbit (native)  | moon     | native  | dynamic | yes      | 160.05            |

| Rank | Entry             | Score  |
| ---- | ----------------- | ------ |
| 1    | c (clang)         | 0.8138 |
| 2    | c (gcc)           | 0.7971 |
| 3    | nim (clang)       | 0.7052 |
| 4    | nim (gcc)         | 0.6800 |
| 5    | ocaml (native)    | 0.6381 |
| 6    | rust (rustc/llvm) | 0.6165 |
| 7    | moonbit (native)  | 0.3858 |

| Benchmark    | Entry             | Input    | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (gcc)           | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.2340         | 15.0079      | 257.91            | 18.17             | ok     |
| binarytrees  | c (clang)         | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1066         | 16.0551      | 258.21            | 5.72              | ok     |
| binarytrees  | rust (rustc/llvm) | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 2.5479         | 18.9448      | 449.78            | 304.27            | ok     |
| binarytrees  | nim (gcc)         | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.3605         | 8.5991       | 456.98            | 38.52             | ok     |
| binarytrees  | nim (clang)       | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.0444         | 8.8327       | 457.02            | 26.38             | ok     |
| binarytrees  | ocaml (native)    | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1841         | 6.5964       | 207.86            | 1006.33           | ok     |
| binarytrees  | moonbit (native)  | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.8543         | 6.4758       | 162.05            | 200.94            | ok     |
| fannkuch     | c (gcc)           | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1066         | 0.0836       | 24.90             | 14.20             | ok     |
| fannkuch     | c (clang)         | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1071         | 0.0783       | 24.90             | 6.71              | ok     |
| fannkuch     | rust (rustc/llvm) | 10       | 2628 / Pfannkuchen(10) = 28                                              | 2.6064         | 0.0773       | 24.90             | 305.47            | ok     |
| fannkuch     | nim (gcc)         | 10       | 2628 / Pfannkuchen(10) = 28                                              | 1.3904         | 0.0883       | 24.90             | 34.46             | ok     |
| fannkuch     | nim (clang)       | 10       | 2628 / Pfannkuchen(10) = 28                                              | 1.1720         | 0.0737       | 24.90             | 25.07             | ok     |
| fannkuch     | ocaml (native)    | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1935         | 0.1203       | 24.90             | 1009.77           | ok     |
| fannkuch     | moonbit (native)  | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.6572         | 1.1128       | 24.90             | 203.75            | ok     |
| mandelbrot   | c (gcc)           | 512      | sha256:e41a9386e912a316                                                  | 0.0994         | 0.0143       | 24.90             | 14.14             | ok     |
| mandelbrot   | c (clang)         | 512      | sha256:e41a9386e912a316                                                  | 0.0921         | 0.0166       | 24.90             | 5.81              | ok     |
| mandelbrot   | rust (rustc/llvm) | 512      | sha256:e41a9386e912a316                                                  | 2.6230         | 0.0193       | 24.90             | 304.73            | ok     |
| mandelbrot   | nim (gcc)         | 512      | sha256:e41a9386e912a316                                                  | 1.3580         | 0.0141       | 24.90             | 34.46             | ok     |
| mandelbrot   | nim (clang)       | 512      | sha256:e41a9386e912a316                                                  | 1.0988         | 0.0140       | 24.90             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512      | sha256:e41a9386e912a316                                                  | 0.1434         | 0.0172       | 24.90             | 1005.27           | ok     |
| mandelbrot   | moonbit (native)  | 512      | sha256:e41a9386e912a316                                                  | 0.6241         | 0.0997       | 24.90             | 200.62            | ok     |
| nbody        | c (gcc)           | 10000000 | -0.169075164 / -0.169077842                                              | 0.1296         | 0.4854       | 24.90             | 14.15             | ok     |
| nbody        | c (clang)         | 10000000 | -0.169075164 / -0.169077842                                              | 0.1240         | 0.4508       | 24.90             | 8.78              | ok     |
| nbody        | rust (rustc/llvm) | 10000000 | -0.169075164 / -0.169077842                                              | 2.8057         | 0.3518       | 24.90             | 329.12            | ok     |
| nbody        | nim (gcc)         | 10000000 | -0.169075164 / -0.169077842                                              | 1.2699         | 0.5134       | 24.90             | 34.46             | ok     |
| nbody        | nim (clang)       | 10000000 | -0.169075164 / -0.169077842                                              | 1.0901         | 0.5164       | 24.90             | 28.04             | ok     |
| nbody        | ocaml (native)    | 10000000 | -0.169075164 / -0.169077842                                              | 0.1430         | 0.6359       | 24.90             | 1006.45           | ok     |
| nbody        | moonbit (native)  | 10000000 | -0.169075164 / -0.169077842                                              | 0.5705         | 6.1305       | 24.90             | 208.26            | ok     |
| spectralnorm | c (gcc)           | 5500     | 1.274224153                                                              | 0.1891         | 0.8993       | 24.90             | 14.16             | ok     |
| spectralnorm | c (clang)         | 5500     | 1.274224153                                                              | 0.1498         | 1.5478       | 24.90             | 8.99              | ok     |
| spectralnorm | rust (rustc/llvm) | 5500     | 1.274224153                                                              | 3.2996         | 1.5714       | 24.90             | 329.27            | ok     |
| spectralnorm | nim (gcc)         | 5500     | 1.274224153                                                              | 1.3540         | 1.3918       | 24.90             | 34.46             | ok     |
| spectralnorm | nim (clang)       | 5500     | 1.274224153                                                              | 1.0745         | 1.4057       | 24.90             | 24.81             | ok     |
| spectralnorm | ocaml (native)    | 5500     | 1.274224153                                                              | 0.1703         | 4.4176       | 24.90             | 1009.95           | ok     |
| spectralnorm | moonbit (native)  | 5500     | 1.274224153                                                              | 0.6491         | 21.3727      | 24.90             | 205.51            | ok     |
| startup      | c (gcc)           | -        | ok                                                                       | 0.0751         | 0.0007       | 24.90             | 14.13             | ok     |
| startup      | c (clang)         | -        | ok                                                                       | 0.0562         | 0.0007       | 24.90             | 4.55              | ok     |
| startup      | rust (rustc/llvm) | -        | ok                                                                       | 2.4287         | 0.0006       | 24.90             | 300.38            | ok     |
| startup      | nim (gcc)         | -        | ok                                                                       | 0.6867         | 0.0005       | 24.90             | 26.29             | ok     |
| startup      | nim (clang)       | -        | ok                                                                       | 0.4969         | 0.0006       | 24.90             | 5.88              | ok     |
| startup      | ocaml (native)    | -        | ok                                                                       | 0.0968         | 0.0011       | 24.90             | 409.35            | ok     |
| startup      | moonbit (native)  | -        | ok                                                                       | 0.5103         | 0.0009       | 24.90             | 160.05            | ok     |
