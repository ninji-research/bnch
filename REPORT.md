# Benchmark Report

| Setting     | Value                                                              |
| ----------- | ------------------------------------------------------------------ |
| runs        | 3                                                                  |
| warmup      | 1                                                                  |
| build_jobs  | 16                                                                 |
| link_policy | toolchain-default release mode (mixed linkage; see entry metadata) |
| entries     | 8                                                                  |
| benchmarks  | 7                                                                  |
| gcc         | gcc (AerynOS) 15.2.1 20251024                                      |
| clang       | clang version 21.1.8 (AerynOS)                                     |
| go          | go version go1.26.0 linux/amd64                                    |
| rustc       | rustc 1.94.0 (4a4ef493e 2026-03-02)                                |
| nim         | Nim Compiler Version 2.2.8 [Linux: amd64]                          |
| ocamlopt    | 5.4.1                                                              |
| moon        | moon 0.1.20260209 (b129ae2 2026-02-09)                             |
| strip       | GNU strip (GNU Binutils) 2.46.0                                    |

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
| benchmark:knucleotide  | 1.00  |
| benchmark:startup      | 0.25  |

| Benchmark    | Algorithm                                                  | Time                     | Space                    | Output Contract                  | Fairness Notes                                                                        |
| ------------ | ---------------------------------------------------------- | ------------------------ | ------------------------ | -------------------------------- | ------------------------------------------------------------------------------------- |
| binarytrees  | bottom-up binary tree construction and checksum            | O(nodes built)           | O(max tree size)         | exact multiline text             | Same tree/check workload; memory-management costs remain language-native.             |
| mandelbrot   | scalar Mandelbrot escape-time bitmap checksum              | O(size^2 * iter)         | O(1)                     | exact integer checksum           | Input size is set to 512 because all retained implementations agree there exactly.    |
| spectralnorm | power method on implicit matrix                            | O(n^2 * iterations)      | O(n)                     | one float rounded to 9 decimals  | Correctness compares canonical 9-decimal output, not raw printer differences.         |
| fannkuch     | fannkuch-redux permutation flips                           | O(n! * n)                | O(n)                     | exact two-line text              | Same permutation-generation strategy across entries.                                  |
| nbody        | 5-body symplectic advance and energy                       | O(iterations * bodies^2) | O(1)                     | two floats rounded to 9 decimals | Correctness compares canonical 9-decimal energies line-by-line.                       |
| knucleotide  | FASTA parsing plus k-mer frequency and occurrence counting | O(n)                     | O(unique k-mers + input) | exact multiline text             | Uses one committed deterministic FASTA fixture and processes only the >THREE section. |
| startup      | process startup and hello-world print                      | O(1)                     | O(1)                     | exact single line                | Useful signal for runtime/toolchain startup, but intentionally low ranking impact.    |

| Entry             | Compiler | Backend | Linkage | Stripped | Startup Binary Size (KiB) |
| ----------------- | -------- | ------- | ------- | -------- | ------------------------- |
| c (gcc)           | gcc      | native  | dynamic | yes      | 14.13                     |
| c (clang)         | clang    | native  | dynamic | yes      | 4.55                      |
| go (gc)           | go       | native  | static  | yes      | 1538.77                   |
| rust (rustc/llvm) | rustc    | llvm    | dynamic | yes      | 300.38                    |
| nim (gcc)         | gcc      | c       | dynamic | yes      | 26.29                     |
| nim (clang)       | clang    | c       | dynamic | yes      | 5.88                      |
| ocaml (native)    | ocamlopt | native  | dynamic | yes      | 409.35                    |
| moonbit (native)  | moon     | native  | dynamic | yes      | 160.05                    |

| Overall | Entry             | Score  | Speed | Memory | Build | Size |
| ------- | ----------------- | ------ | ----- | ------ | ----- | ---- |
| 1       | c (clang)         | 0.8461 | 2     | 4      | 1     | 1    |
| 2       | c (gcc)           | 0.8093 | 1     | 5      | 2     | 2    |
| 3       | nim (clang)       | 0.6565 | 3     | 8      | 6     | 3    |
| 4       | nim (gcc)         | 0.6357 | 5     | 7      | 7     | 4    |
| 5       | go (gc)           | 0.6234 | 6     | 2      | 4     | 8    |
| 6       | rust (rustc/llvm) | 0.6163 | 4     | 6      | 8     | 6    |
| 7       | ocaml (native)    | 0.5793 | 7     | 3      | 3     | 7    |
| 8       | moonbit (native)  | 0.3448 | 8     | 1      | 5     | 5    |

_Overall score uses normalized per-benchmark scoring with the configured metric weights. Per-metric columns show rank only, using that metric's normalized score across the scored benchmarks._

| Benchmark    | Entry             | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (gcc)           | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.2084         | 14.6334      | 258.22            | 18.17             | ok     |
| binarytrees  | c (clang)         | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.0996         | 14.8631      | 258.21            | 5.72              | ok     |
| binarytrees  | go (gc)           | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 3.5296         | 15.9156      | 201.81            | 1554.83           | ok     |
| binarytrees  | rust (rustc/llvm) | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 3.1168         | 19.0894      | 449.89            | 304.27            | ok     |
| binarytrees  | nim (gcc)         | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.4788         | 9.0763       | 457.07            | 38.52             | ok     |
| binarytrees  | nim (clang)       | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.1344         | 8.9651       | 457.21            | 26.38             | ok     |
| binarytrees  | ocaml (native)    | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1821         | 5.2001       | 208.19            | 1006.33           | ok     |
| binarytrees  | moonbit (native)  | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.6334         | 6.7676       | 162.02            | 200.94            | ok     |
| fannkuch     | c (gcc)           | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1250         | 0.0904       | 22.74             | 14.20             | ok     |
| fannkuch     | c (clang)         | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1142         | 0.0868       | 22.74             | 6.71              | ok     |
| fannkuch     | go (gc)           | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.2085         | 0.0905       | 22.74             | 1554.83           | ok     |
| fannkuch     | rust (rustc/llvm) | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 2.6708         | 0.0812       | 22.74             | 305.47            | ok     |
| fannkuch     | nim (gcc)         | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 1.3246         | 0.0870       | 22.74             | 34.46             | ok     |
| fannkuch     | nim (clang)       | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 1.1149         | 0.0744       | 22.74             | 25.07             | ok     |
| fannkuch     | ocaml (native)    | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1581         | 0.1283       | 22.74             | 1009.77           | ok     |
| fannkuch     | moonbit (native)  | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.6091         | 1.1864       | 22.74             | 203.75            | ok     |
| knucleotide  | c (gcc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1315         | 0.0061       | 23.24             | 14.33             | ok     |
| knucleotide  | c (clang)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1283         | 0.0058       | 23.24             | 9.18              | ok     |
| knucleotide  | go (gc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.2827         | 0.0096       | 23.24             | 1579.08           | ok     |
| knucleotide  | rust (rustc/llvm) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 3.4330         | 0.0074       | 23.24             | 347.73            | ok     |
| knucleotide  | nim (gcc)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.9561         | 0.0110       | 23.24             | 46.49             | ok     |
| knucleotide  | nim (clang)       | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.6935         | 0.0110       | 23.24             | 32.41             | ok     |
| knucleotide  | ocaml (native)    | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.2088         | 0.0405       | 23.24             | 1065.55           | ok     |
| knucleotide  | moonbit (native)  | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.7253         | 0.0809       | 23.24             | 193.98            | ok     |
| mandelbrot   | c (gcc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.1034         | 0.0138       | 22.74             | 14.14             | ok     |
| mandelbrot   | c (clang)         | 512                              | sha256:e41a9386e912a316                                                  | 0.0972         | 0.0144       | 22.74             | 5.81              | ok     |
| mandelbrot   | go (gc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.1437         | 0.0165       | 22.74             | 1546.83           | ok     |
| mandelbrot   | rust (rustc/llvm) | 512                              | sha256:e41a9386e912a316                                                  | 2.6554         | 0.0175       | 22.74             | 304.67            | ok     |
| mandelbrot   | nim (gcc)         | 512                              | sha256:e41a9386e912a316                                                  | 1.3162         | 0.0142       | 22.74             | 34.46             | ok     |
| mandelbrot   | nim (clang)       | 512                              | sha256:e41a9386e912a316                                                  | 1.0706         | 0.0142       | 22.74             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512                              | sha256:e41a9386e912a316                                                  | 0.1490         | 0.0173       | 22.74             | 1005.27           | ok     |
| mandelbrot   | moonbit (native)  | 512                              | sha256:e41a9386e912a316                                                  | 0.5769         | 0.0955       | 22.74             | 200.56            | ok     |
| nbody        | c (gcc)           | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1383         | 0.4980       | 22.74             | 14.15             | ok     |
| nbody        | c (clang)         | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1290         | 0.4419       | 22.74             | 8.78              | ok     |
| nbody        | go (gc)           | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1379         | 0.6482       | 22.74             | 1558.83           | ok     |
| nbody        | rust (rustc/llvm) | 10000000                         | -0.169075164 / -0.169077842                                              | 2.8585         | 0.3730       | 22.74             | 329.12            | ok     |
| nbody        | nim (gcc)         | 10000000                         | -0.169075164 / -0.169077842                                              | 1.3765         | 0.5463       | 22.74             | 34.46             | ok     |
| nbody        | nim (clang)       | 10000000                         | -0.169075164 / -0.169077842                                              | 1.1479         | 0.5454       | 22.74             | 28.04             | ok     |
| nbody        | ocaml (native)    | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1531         | 0.6920       | 22.74             | 1006.45           | ok     |
| nbody        | moonbit (native)  | 10000000                         | -0.169075164 / -0.169077842                                              | 0.6020         | 6.6591       | 22.74             | 208.26            | ok     |
| spectralnorm | c (gcc)           | 5500                             | 1.274224153                                                              | 0.1798         | 0.8647       | 22.74             | 14.16             | ok     |
| spectralnorm | c (clang)         | 5500                             | 1.274224153                                                              | 0.1518         | 1.3858       | 22.74             | 8.99              | ok     |
| spectralnorm | go (gc)           | 5500                             | 1.274224153                                                              | 0.1232         | 1.4969       | 22.74             | 1554.83           | ok     |
| spectralnorm | rust (rustc/llvm) | 5500                             | 1.274224153                                                              | 2.9015         | 1.6078       | 22.74             | 329.27            | ok     |
| spectralnorm | nim (gcc)         | 5500                             | 1.274224153                                                              | 1.3397         | 1.4470       | 22.74             | 34.46             | ok     |
| spectralnorm | nim (clang)       | 5500                             | 1.274224153                                                              | 1.1157         | 1.4671       | 22.74             | 24.81             | ok     |
| spectralnorm | ocaml (native)    | 5500                             | 1.274224153                                                              | 0.1568         | 4.8263       | 22.74             | 1009.95           | ok     |
| spectralnorm | moonbit (native)  | 5500                             | 1.274224153                                                              | 0.5972         | 22.2163      | 22.74             | 205.51            | ok     |
| startup      | c (gcc)           | -                                | ok                                                                       | 0.0906         | 0.0007       | 23.24             | 14.13             | ok     |
| startup      | c (clang)         | -                                | ok                                                                       | 0.0791         | 0.0009       | 23.24             | 4.55              | ok     |
| startup      | go (gc)           | -                                | ok                                                                       | 0.1175         | 0.0015       | 23.24             | 1538.77           | ok     |
| startup      | rust (rustc/llvm) | -                                | ok                                                                       | 3.2247         | 0.0008       | 23.24             | 300.38            | ok     |
| startup      | nim (gcc)         | -                                | ok                                                                       | 0.9498         | 0.0006       | 23.24             | 26.29             | ok     |
| startup      | nim (clang)       | -                                | ok                                                                       | 0.8129         | 0.0007       | 23.24             | 5.88              | ok     |
| startup      | ocaml (native)    | -                                | ok                                                                       | 0.1316         | 0.0026       | 23.24             | 409.35            | ok     |
| startup      | moonbit (native)  | -                                | ok                                                                       | 0.6645         | 0.0011       | 23.24             | 160.05            | ok     |
