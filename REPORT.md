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
| 1    | c (clang)         | 0.8011 |
| 2    | c (gcc)           | 0.7655 |
| 3    | nim (clang)       | 0.6813 |
| 4    | nim (gcc)         | 0.6445 |
| 5    | ocaml (native)    | 0.6413 |
| 6    | rust (rustc/llvm) | 0.5990 |
| 7    | moonbit (native)  | 0.3558 |

| Entry             | Overall | Speed | Memory | Build | Size |
| ----------------- | ------- | ----- | ------ | ----- | ---- |
| c (clang)         | 1       | 5     | 4      | 1     | 1    |
| c (gcc)           | 2       | 2     | 3      | 2     | 2    |
| nim (clang)       | 3       | 1     | 7      | 5     | 3    |
| nim (gcc)         | 4       | 3     | 6      | 6     | 4    |
| ocaml (native)    | 5       | 6     | 2      | 3     | 7    |
| rust (rustc/llvm) | 6       | 4     | 5      | 7     | 6    |
| moonbit (native)  | 7       | 7     | 1      | 4     | 5    |

| Benchmark    | Entry             | Input    | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (gcc)           | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.2058         | 14.2758      | 258.04            | 18.17             | ok     |
| binarytrees  | c (clang)         | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.0876         | 15.7424      | 258.16            | 5.72              | ok     |
| binarytrees  | rust (rustc/llvm) | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 2.5365         | 19.5952      | 449.59            | 304.27            | ok     |
| binarytrees  | nim (gcc)         | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.3746         | 8.5041       | 456.80            | 38.52             | ok     |
| binarytrees  | nim (clang)       | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.1426         | 7.8075       | 457.95            | 26.38             | ok     |
| binarytrees  | ocaml (native)    | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1321         | 4.3497       | 208.28            | 1006.33           | ok     |
| binarytrees  | moonbit (native)  | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.5069         | 6.2518       | 162.02            | 200.94            | ok     |
| fannkuch     | c (gcc)           | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1925         | 0.0942       | 23.21             | 14.20             | ok     |
| fannkuch     | c (clang)         | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1521         | 0.0957       | 23.21             | 6.71              | ok     |
| fannkuch     | rust (rustc/llvm) | 10       | 2628 / Pfannkuchen(10) = 28                                              | 3.4994         | 0.0794       | 23.21             | 305.47            | ok     |
| fannkuch     | nim (gcc)         | 10       | 2628 / Pfannkuchen(10) = 28                                              | 1.2487         | 0.0791       | 23.21             | 34.46             | ok     |
| fannkuch     | nim (clang)       | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.9745         | 0.0644       | 23.21             | 25.07             | ok     |
| fannkuch     | ocaml (native)    | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1689         | 0.1204       | 23.21             | 1009.77           | ok     |
| fannkuch     | moonbit (native)  | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.5254         | 1.0859       | 23.21             | 203.75            | ok     |
| mandelbrot   | c (gcc)           | 512      | sha256:e41a9386e912a316                                                  | 0.0821         | 0.0134       | 23.21             | 14.14             | ok     |
| mandelbrot   | c (clang)         | 512      | sha256:e41a9386e912a316                                                  | 0.0714         | 0.0136       | 23.21             | 5.81              | ok     |
| mandelbrot   | rust (rustc/llvm) | 512      | sha256:e41a9386e912a316                                                  | 2.3074         | 0.0148       | 23.21             | 304.67            | ok     |
| mandelbrot   | nim (gcc)         | 512      | sha256:e41a9386e912a316                                                  | 1.1814         | 0.0140       | 23.21             | 34.46             | ok     |
| mandelbrot   | nim (clang)       | 512      | sha256:e41a9386e912a316                                                  | 0.9928         | 0.0138       | 23.21             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512      | sha256:e41a9386e912a316                                                  | 0.1275         | 0.0165       | 23.21             | 1005.27           | ok     |
| mandelbrot   | moonbit (native)  | 512      | sha256:e41a9386e912a316                                                  | 0.6092         | 0.0919       | 23.21             | 200.56            | ok     |
| nbody        | c (gcc)           | 10000000 | -0.169075164 / -0.169077842                                              | 0.1052         | 0.4590       | 23.21             | 14.15             | ok     |
| nbody        | c (clang)         | 10000000 | -0.169075164 / -0.169077842                                              | 0.0945         | 0.4027       | 23.21             | 8.78              | ok     |
| nbody        | rust (rustc/llvm) | 10000000 | -0.169075164 / -0.169077842                                              | 2.3788         | 0.3603       | 23.21             | 329.12            | ok     |
| nbody        | nim (gcc)         | 10000000 | -0.169075164 / -0.169077842                                              | 1.1574         | 0.5042       | 23.21             | 34.46             | ok     |
| nbody        | nim (clang)       | 10000000 | -0.169075164 / -0.169077842                                              | 1.0063         | 0.4892       | 23.21             | 28.04             | ok     |
| nbody        | ocaml (native)    | 10000000 | -0.169075164 / -0.169077842                                              | 0.1286         | 0.6161       | 23.21             | 1006.45           | ok     |
| nbody        | moonbit (native)  | 10000000 | -0.169075164 / -0.169077842                                              | 0.4986         | 6.0775       | 23.21             | 208.26            | ok     |
| spectralnorm | c (gcc)           | 5500     | 1.274224153                                                              | 0.1442         | 0.8589       | 23.21             | 14.16             | ok     |
| spectralnorm | c (clang)         | 5500     | 1.274224153                                                              | 0.1310         | 1.3515       | 23.21             | 8.99              | ok     |
| spectralnorm | rust (rustc/llvm) | 5500     | 1.274224153                                                              | 2.6208         | 1.5418       | 23.21             | 329.27            | ok     |
| spectralnorm | nim (gcc)         | 5500     | 1.274224153                                                              | 1.4645         | 1.4220       | 23.21             | 34.46             | ok     |
| spectralnorm | nim (clang)       | 5500     | 1.274224153                                                              | 1.1214         | 1.4745       | 23.21             | 24.81             | ok     |
| spectralnorm | ocaml (native)    | 5500     | 1.274224153                                                              | 0.1269         | 4.4997       | 23.21             | 1009.95           | ok     |
| spectralnorm | moonbit (native)  | 5500     | 1.274224153                                                              | 0.5319         | 21.8463      | 23.21             | 205.51            | ok     |
| startup      | c (gcc)           | -        | ok                                                                       | 0.0680         | 0.0007       | 23.21             | 14.13             | ok     |
| startup      | c (clang)         | -        | ok                                                                       | 0.0645         | 0.0008       | 23.21             | 4.55              | ok     |
| startup      | rust (rustc/llvm) | -        | ok                                                                       | 2.3900         | 0.0008       | 23.21             | 300.38            | ok     |
| startup      | nim (gcc)         | -        | ok                                                                       | 0.6594         | 0.0005       | 23.21             | 26.29             | ok     |
| startup      | nim (clang)       | -        | ok                                                                       | 0.4386         | 0.0006       | 23.21             | 5.88              | ok     |
| startup      | ocaml (native)    | -        | ok                                                                       | 0.0742         | 0.0011       | 23.21             | 409.35            | ok     |
| startup      | moonbit (native)  | -        | ok                                                                       | 0.4456         | 0.0008       | 23.21             | 160.05            | ok     |
