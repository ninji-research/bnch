# Benchmark Report

| Setting     | Value                                                                |
| ----------- | -------------------------------------------------------------------- |
| runs        | 3                                                                    |
| warmup      | 1                                                                    |
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

| Entry             | Compiler | Backend | Linkage | Stripped | Startup Binary Size (KiB) |
| ----------------- | -------- | ------- | ------- | -------- | ------------------------- |
| c (gcc)           | gcc      | native  | dynamic | yes      | 14.13                     |
| c (clang)         | clang    | native  | dynamic | yes      | 4.55                      |
| rust (rustc/llvm) | rustc    | llvm    | dynamic | yes      | 300.38                    |
| nim (gcc)         | gcc      | c       | dynamic | yes      | 26.29                     |
| nim (clang)       | clang    | c       | dynamic | yes      | 5.88                      |
| ocaml (native)    | ocamlopt | native  | dynamic | yes      | 409.35                    |
| moonbit (native)  | moon     | native  | dynamic | yes      | 160.05                    |

| Overall | Entry             | Score  | Speed       | Memory         | Build       | Size           |
| ------- | ----------------- | ------ | ----------- | -------------- | ----------- | -------------- |
| 1       | c (clang)         | 0.8347 | 4 (3.2112s) | 3 (67.72 MiB)  | 1 (0.1014s) | 1 (7.08 KiB)   |
| 2       | c (gcc)           | 0.7992 | 1 (2.7886s) | 4 (67.73 MiB)  | 2 (0.1406s) | 2 (14.92 KiB)  |
| 3       | nim (clang)       | 0.6889 | 2 (2.1904s) | 7 (105.63 MiB) | 5 (1.0625s) | 3 (24.75 KiB)  |
| 4       | nim (gcc)         | 0.6657 | 3 (2.1132s) | 6 (105.61 MiB) | 6 (1.3688s) | 4 (34.85 KiB)  |
| 5       | ocaml (native)    | 0.6468 | 6 (2.0810s) | 2 (58.25 MiB)  | 3 (0.1476s) | 7 (979.07 KiB) |
| 6       | rust (rustc/llvm) | 0.6311 | 5 (3.7637s) | 5 (104.24 MiB) | 7 (2.5102s) | 6 (313.89 KiB) |
| 7       | moonbit (native)  | 0.3642 | 7 (6.6822s) | 1 (49.42 MiB)  | 4 (0.5720s) | 5 (201.72 KiB) |

| Benchmark    | Entry             | Input    | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (gcc)           | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.2022         | 13.1916      | 258.22            | 18.17             | ok     |
| binarytrees  | c (clang)         | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.0740         | 14.9504      | 258.19            | 5.72              | ok     |
| binarytrees  | rust (rustc/llvm) | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 2.1256         | 17.6463      | 449.92            | 304.27            | ok     |
| binarytrees  | nim (gcc)         | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.3857         | 9.0231       | 457.11            | 38.52             | ok     |
| binarytrees  | nim (clang)       | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.0739         | 9.3594       | 457.19            | 26.38             | ok     |
| binarytrees  | ocaml (native)    | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1800         | 5.4089       | 208.48            | 1006.33           | ok     |
| binarytrees  | moonbit (native)  | 21       | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.6052         | 6.8794       | 162.10            | 200.94            | ok     |
| fannkuch     | c (gcc)           | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1368         | 0.0890       | 22.91             | 14.20             | ok     |
| fannkuch     | c (clang)         | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.0978         | 0.0944       | 22.91             | 6.71              | ok     |
| fannkuch     | rust (rustc/llvm) | 10       | 2628 / Pfannkuchen(10) = 28                                              | 2.6200         | 0.0768       | 22.91             | 305.47            | ok     |
| fannkuch     | nim (gcc)         | 10       | 2628 / Pfannkuchen(10) = 28                                              | 1.3798         | 0.0830       | 22.91             | 34.46             | ok     |
| fannkuch     | nim (clang)       | 10       | 2628 / Pfannkuchen(10) = 28                                              | 1.1291         | 0.0710       | 22.91             | 25.07             | ok     |
| fannkuch     | ocaml (native)    | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.1393         | 0.1207       | 22.91             | 1009.77           | ok     |
| fannkuch     | moonbit (native)  | 10       | 2628 / Pfannkuchen(10) = 28                                              | 0.5707         | 1.0906       | 22.91             | 203.75            | ok     |
| mandelbrot   | c (gcc)           | 512      | sha256:e41a9386e912a316                                                  | 0.0943         | 0.0140       | 22.91             | 14.14             | ok     |
| mandelbrot   | c (clang)         | 512      | sha256:e41a9386e912a316                                                  | 0.0994         | 0.0146       | 22.91             | 5.81              | ok     |
| mandelbrot   | rust (rustc/llvm) | 512      | sha256:e41a9386e912a316                                                  | 2.5696         | 0.0149       | 22.91             | 304.67            | ok     |
| mandelbrot   | nim (gcc)         | 512      | sha256:e41a9386e912a316                                                  | 1.3202         | 0.0146       | 22.91             | 34.46             | ok     |
| mandelbrot   | nim (clang)       | 512      | sha256:e41a9386e912a316                                                  | 1.1083         | 0.0145       | 22.91             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512      | sha256:e41a9386e912a316                                                  | 0.1516         | 0.0164       | 22.91             | 1005.27           | ok     |
| mandelbrot   | moonbit (native)  | 512      | sha256:e41a9386e912a316                                                  | 0.5956         | 0.0978       | 22.91             | 200.56            | ok     |
| nbody        | c (gcc)           | 10000000 | -0.169075164 / -0.169077842                                              | 0.1116         | 0.4583       | 22.91             | 14.15             | ok     |
| nbody        | c (clang)         | 10000000 | -0.169075164 / -0.169077842                                              | 0.0935         | 0.3986       | 22.91             | 8.78              | ok     |
| nbody        | rust (rustc/llvm) | 10000000 | -0.169075164 / -0.169077842                                              | 2.4121         | 0.3952       | 22.91             | 329.12            | ok     |
| nbody        | nim (gcc)         | 10000000 | -0.169075164 / -0.169077842                                              | 1.4386         | 0.4994       | 22.91             | 34.46             | ok     |
| nbody        | nim (clang)       | 10000000 | -0.169075164 / -0.169077842                                              | 1.0116         | 0.5097       | 22.91             | 28.04             | ok     |
| nbody        | ocaml (native)    | 10000000 | -0.169075164 / -0.169077842                                              | 0.1301         | 0.6318       | 22.91             | 1006.45           | ok     |
| nbody        | moonbit (native)  | 10000000 | -0.169075164 / -0.169077842                                              | 0.5076         | 6.0912       | 22.91             | 208.26            | ok     |
| spectralnorm | c (gcc)           | 5500     | 1.274224153                                                              | 0.1781         | 0.8872       | 22.91             | 14.16             | ok     |
| spectralnorm | c (clang)         | 5500     | 1.274224153                                                              | 0.1552         | 1.4005       | 22.91             | 8.99              | ok     |
| spectralnorm | rust (rustc/llvm) | 5500     | 1.274224153                                                              | 2.8922         | 1.6258       | 22.91             | 329.27            | ok     |
| spectralnorm | nim (gcc)         | 5500     | 1.274224153                                                              | 1.4931         | 1.4743       | 22.91             | 34.46             | ok     |
| spectralnorm | nim (clang)       | 5500     | 1.274224153                                                              | 1.1332         | 1.5449       | 22.91             | 24.81             | ok     |
| spectralnorm | ocaml (native)    | 5500     | 1.274224153                                                              | 0.1525         | 4.7473       | 22.91             | 1009.95           | ok     |
| spectralnorm | moonbit (native)  | 5500     | 1.274224153                                                              | 0.6037         | 20.9224      | 22.91             | 205.51            | ok     |
| startup      | c (gcc)           | -        | ok                                                                       | 0.0615         | 0.0006       | 22.91             | 14.13             | ok     |
| startup      | c (clang)         | -        | ok                                                                       | 0.0495         | 0.0005       | 22.91             | 4.55              | ok     |
| startup      | rust (rustc/llvm) | -        | ok                                                                       | 2.2368         | 0.0006       | 22.91             | 300.38            | ok     |
| startup      | nim (gcc)         | -        | ok                                                                       | 0.6748         | 0.0005       | 22.91             | 26.29             | ok     |
| startup      | nim (clang)       | -        | ok                                                                       | 0.4883         | 0.0005       | 22.91             | 5.88              | ok     |
| startup      | ocaml (native)    | -        | ok                                                                       | 0.0868         | 0.0010       | 22.91             | 409.35            | ok     |
| startup      | moonbit (native)  | -        | ok                                                                       | 0.4815         | 0.0008       | 22.91             | 160.05            | ok     |
