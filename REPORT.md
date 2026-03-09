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
| 1    | c (clang)         | 0.8274 |
| 2    | c (gcc)           | 0.7727 |
| 3    | nim (clang)       | 0.6760 |
| 4    | nim (gcc)         | 0.6488 |
| 5    | ocaml (native)    | 0.6384 |
| 6    | rust (rustc/llvm) | 0.6176 |
| 7    | moonbit (native)  | 0.3651 |

| Benchmark    | Entry             | Input    | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (gcc)           | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.2400         | 15.2296      | 257.78            | 18.17             | ok     |
| binarytrees  | c (clang)         | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.0894         | 16.3591      | 257.90            | 5.72              | ok     |
| binarytrees  | rust (rustc/llvm) | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 2.6860         | 20.1532      | 449.21            | 304.27            | ok     |
| binarytrees  | nim (gcc)         | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.5229         | 9.4152       | 456.96            | 38.52             | ok     |
| binarytrees  | nim (clang)       | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.2121         | 9.0907       | 456.74            | 26.38             | ok     |
| binarytrees  | ocaml (native)    | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1689         | 5.3645       | 208.26            | 1006.33           | ok     |
| binarytrees  | moonbit (native)  | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.6244         | 6.8884       | 161.96            | 200.94            | ok     |
| fannkuch     | c (gcc)           | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1140         | 0.0915       | 24.82             | 14.20             | ok     |
| fannkuch     | c (clang)         | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1038         | 0.0839       | 24.82             | 6.71              | ok     |
| fannkuch     | rust (rustc/llvm) | 10       | 2628 / Pfannkuchen(10) = 28                                              | 2.6215         | 0.0771       | 24.82             | 305.47            | ok     |
| fannkuch     | nim (gcc)         | 10       | 2628 / Pfannkuchen(10) = 28                                              | 1.3011         | 0.0856       | 24.82             | 34.46             | ok     |
| fannkuch     | nim (clang)       | 10       | 2628 / Pfannkuchen(10) = 28                                              | 1.0429         | 0.0688       | 24.95             | 25.07             | ok     |
| fannkuch     | ocaml (native)    | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1261         | 0.1214       | 24.95             | 1009.77           | ok     |
| fannkuch     | moonbit (native)  | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.5196         | 1.1181       | 24.95             | 203.75            | ok     |
| mandelbrot   | c (gcc)           | 512      | sha256:e41a9386e912a316                                                  | 0.0942         | 0.0143       | 24.82             | 14.14             | ok     |
| mandelbrot   | c (clang)         | 512      | sha256:e41a9386e912a316                                                  | 0.0895         | 0.0143       | 24.82             | 5.81              | ok     |
| mandelbrot   | rust (rustc/llvm) | 512      | sha256:e41a9386e912a316                                                  | 2.5783         | 0.0148       | 24.82             | 304.67            | ok     |
| mandelbrot   | nim (gcc)         | 512      | sha256:e41a9386e912a316                                                  | 1.3045         | 0.0139       | 24.82             | 34.46             | ok     |
| mandelbrot   | nim (clang)       | 512      | sha256:e41a9386e912a316                                                  | 1.0826         | 0.0137       | 24.82             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512      | sha256:e41a9386e912a316                                                  | 0.1378         | 0.0163       | 24.82             | 1005.27           | ok     |
| mandelbrot   | moonbit (native)  | 512      | sha256:e41a9386e912a316                                                  | 0.5921         | 0.0944       | 24.82             | 200.56            | ok     |
| nbody        | c (gcc)           | 10000000 | -0.169075164 / -0.169077842                                              | 0.1205         | 0.4667       | 24.95             | 14.15             | ok     |
| nbody        | c (clang)         | 10000000 | -0.169075164 / -0.169077842                                              | 0.1053         | 0.4117       | 24.95             | 8.78              | ok     |
| nbody        | rust (rustc/llvm) | 10000000 | -0.169075164 / -0.169077842                                              | 2.8054         | 0.3658       | 24.95             | 329.12            | ok     |
| nbody        | nim (gcc)         | 10000000 | -0.169075164 / -0.169077842                                              | 1.3984         | 0.5383       | 24.95             | 34.46             | ok     |
| nbody        | nim (clang)       | 10000000 | -0.169075164 / -0.169077842                                              | 1.2048         | 0.5490       | 24.95             | 28.04             | ok     |
| nbody        | ocaml (native)    | 10000000 | -0.169075164 / -0.169077842                                              | 0.1832         | 0.6614       | 24.95             | 1006.45           | ok     |
| nbody        | moonbit (native)  | 10000000 | -0.169075164 / -0.169077842                                              | 0.6627         | 6.5594       | 24.95             | 208.26            | ok     |
| spectralnorm | c (gcc)           | 5500     | 1.274224153                                                              | 0.1876         | 0.9203       | 24.82             | 14.16             | ok     |
| spectralnorm | c (clang)         | 5500     | 1.274224153                                                              | 0.1412         | 1.4181       | 24.82             | 8.99              | ok     |
| spectralnorm | rust (rustc/llvm) | 5500     | 1.274224153                                                              | 2.9861         | 1.6316       | 24.82             | 329.27            | ok     |
| spectralnorm | nim (gcc)         | 5500     | 1.274224153                                                              | 1.4226         | 1.5108       | 24.82             | 34.46             | ok     |
| spectralnorm | nim (clang)       | 5500     | 1.274224153                                                              | 1.2014         | 1.4694       | 24.82             | 24.81             | ok     |
| spectralnorm | ocaml (native)    | 5500     | 1.274224153                                                              | 0.1550         | 4.8185       | 24.82             | 1009.95           | ok     |
| spectralnorm | moonbit (native)  | 5500     | 1.274224153                                                              | 0.6010         | 21.6747      | 24.82             | 205.51            | ok     |
| startup      | c (gcc)           | -        | ok                                                                       | 0.0828         | 0.0009       | 24.95             | 14.13             | ok     |
| startup      | c (clang)         | -        | ok                                                                       | 0.0635         | 0.0007       | 24.95             | 4.55              | ok     |
| startup      | rust (rustc/llvm) | -        | ok                                                                       | 2.6483         | 0.0010       | 24.95             | 300.38            | ok     |
| startup      | nim (gcc)         | -        | ok                                                                       | 0.7804         | 0.0006       | 24.95             | 26.29             | ok     |
| startup      | nim (clang)       | -        | ok                                                                       | 0.5196         | 0.0010       | 24.95             | 5.88              | ok     |
| startup      | ocaml (native)    | -        | ok                                                                       | 0.0870         | 0.0011       | 24.95             | 409.35            | ok     |
| startup      | moonbit (native)  | -        | ok                                                                       | 0.5110         | 0.0009       | 24.95             | 160.05            | ok     |
