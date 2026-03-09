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

| Overall | Entry             | Score  | Speed       | Memory        | Build       | Size            |
| ------- | ----------------- | ------ | ----------- | ------------- | ----------- | --------------- |
| 1       | c (clang)         | 0.8539 | 2 (3.3580s) | 4 (60.84 MiB) | 1 (0.0989s) | 1 (7.41 KiB)    |
| 2       | c (gcc)           | 0.8050 | 1 (2.8042s) | 5 (60.85 MiB) | 2 (0.1407s) | 2 (14.83 KiB)   |
| 3       | nim (clang)       | 0.6844 | 3 (1.7899s) | 8 (92.69 MiB) | 6 (1.0608s) | 3 (25.97 KiB)   |
| 4       | nim (gcc)         | 0.6725 | 4 (1.7832s) | 7 (92.69 MiB) | 7 (1.3472s) | 4 (36.71 KiB)   |
| 5       | rust (rustc/llvm) | 0.6396 | 5 (3.2662s) | 6 (91.53 MiB) | 8 (2.5340s) | 6 (319.30 KiB)  |
| 6       | go (gc)           | 0.6251 | 6 (3.2135s) | 2 (51.82 MiB) | 4 (0.7282s) | 8 (1557.43 KiB) |
| 7       | ocaml (native)    | 0.6096 | 7 (1.7237s) | 3 (52.88 MiB) | 3 (0.1391s) | 7 (992.90 KiB)  |
| 8       | moonbit (native)  | 0.3394 | 8 (5.7955s) | 1 (45.46 MiB) | 5 (0.5351s) | 5 (200.48 KiB)  |

| Benchmark    | Entry             | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (gcc)           | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.2216         | 16.0337      | 258.21            | 18.17             | ok     |
| binarytrees  | c (clang)         | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.0812         | 19.0820      | 258.16            | 5.72              | ok     |
| binarytrees  | go (gc)           | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 3.8396         | 17.8090      | 201.79            | 1554.83           | ok     |
| binarytrees  | rust (rustc/llvm) | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 2.2819         | 18.1985      | 449.95            | 304.27            | ok     |
| binarytrees  | nim (gcc)         | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.2932         | 9.1158       | 457.21            | 38.52             | ok     |
| binarytrees  | nim (clang)       | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.1057         | 9.1766       | 457.23            | 26.38             | ok     |
| binarytrees  | ocaml (native)    | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1520         | 5.5670       | 208.37            | 1006.33           | ok     |
| binarytrees  | moonbit (native)  | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.5920         | 8.6459       | 162.02            | 200.94            | ok     |
| fannkuch     | c (gcc)           | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.0980         | 0.0805       | 23.26             | 14.20             | ok     |
| fannkuch     | c (clang)         | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.0932         | 0.0789       | 23.26             | 6.71              | ok     |
| fannkuch     | go (gc)           | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1390         | 0.0808       | 23.26             | 1554.83           | ok     |
| fannkuch     | rust (rustc/llvm) | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 2.2479         | 0.0722       | 23.26             | 305.47            | ok     |
| fannkuch     | nim (gcc)         | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 1.1585         | 0.0777       | 23.26             | 34.46             | ok     |
| fannkuch     | nim (clang)       | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 1.0421         | 0.0669       | 23.26             | 25.07             | ok     |
| fannkuch     | ocaml (native)    | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1237         | 0.1161       | 23.26             | 1009.77           | ok     |
| fannkuch     | moonbit (native)  | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.5332         | 1.0623       | 23.26             | 203.75            | ok     |
| knucleotide  | c (gcc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1125         | 0.0058       | 23.26             | 14.33             | ok     |
| knucleotide  | c (clang)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1122         | 0.0055       | 23.26             | 9.18              | ok     |
| knucleotide  | go (gc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.2110         | 0.0088       | 23.26             | 1579.08           | ok     |
| knucleotide  | rust (rustc/llvm) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 2.5736         | 0.0055       | 23.26             | 347.73            | ok     |
| knucleotide  | nim (gcc)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.2395         | 0.0061       | 23.26             | 46.49             | ok     |
| knucleotide  | nim (clang)       | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.9551         | 0.0083       | 23.26             | 32.41             | ok     |
| knucleotide  | ocaml (native)    | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1282         | 0.0222       | 23.26             | 1065.55           | ok     |
| knucleotide  | moonbit (native)  | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.4717         | 0.0664       | 23.26             | 193.98            | ok     |
| mandelbrot   | c (gcc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.0933         | 0.0180       | 23.26             | 14.14             | ok     |
| mandelbrot   | c (clang)         | 512                              | sha256:e41a9386e912a316                                                  | 0.0967         | 0.0177       | 23.26             | 5.81              | ok     |
| mandelbrot   | go (gc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.1421         | 0.0223       | 23.26             | 1546.83           | ok     |
| mandelbrot   | rust (rustc/llvm) | 512                              | sha256:e41a9386e912a316                                                  | 2.9307         | 0.0222       | 23.26             | 304.67            | ok     |
| mandelbrot   | nim (gcc)         | 512                              | sha256:e41a9386e912a316                                                  | 1.9206         | 0.0196       | 23.26             | 34.46             | ok     |
| mandelbrot   | nim (clang)       | 512                              | sha256:e41a9386e912a316                                                  | 1.3923         | 0.0179       | 23.26             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512                              | sha256:e41a9386e912a316                                                  | 0.1883         | 0.0195       | 23.26             | 1005.27           | ok     |
| mandelbrot   | moonbit (native)  | 512                              | sha256:e41a9386e912a316                                                  | 0.6007         | 0.1172       | 23.26             | 200.56            | ok     |
| nbody        | c (gcc)           | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1098         | 0.4477       | 23.26             | 14.15             | ok     |
| nbody        | c (clang)         | 10000000                         | -0.169075164 / -0.169077842                                              | 0.0965         | 0.3933       | 23.26             | 8.78              | ok     |
| nbody        | go (gc)           | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1031         | 0.5821       | 23.26             | 1558.83           | ok     |
| nbody        | rust (rustc/llvm) | 10000000                         | -0.169075164 / -0.169077842                                              | 2.4285         | 0.3371       | 23.26             | 329.12            | ok     |
| nbody        | nim (gcc)         | 10000000                         | -0.169075164 / -0.169077842                                              | 1.1944         | 0.4907       | 23.26             | 34.46             | ok     |
| nbody        | nim (clang)       | 10000000                         | -0.169075164 / -0.169077842                                              | 0.9895         | 0.4849       | 23.26             | 28.04             | ok     |
| nbody        | ocaml (native)    | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1267         | 0.6111       | 23.26             | 1006.45           | ok     |
| nbody        | moonbit (native)  | 10000000                         | -0.169075164 / -0.169077842                                              | 0.4935         | 5.9155       | 23.26             | 208.26            | ok     |
| spectralnorm | c (gcc)           | 5500                             | 1.274224153                                                              | 0.2295         | 0.9402       | 23.26             | 14.16             | ok     |
| spectralnorm | c (clang)         | 5500                             | 1.274224153                                                              | 0.1255         | 1.4099       | 23.26             | 8.99              | ok     |
| spectralnorm | go (gc)           | 5500                             | 1.274224153                                                              | 0.0944         | 1.5813       | 23.26             | 1554.83           | ok     |
| spectralnorm | rust (rustc/llvm) | 5500                             | 1.274224153                                                              | 2.8584         | 1.7778       | 23.26             | 329.27            | ok     |
| spectralnorm | nim (gcc)         | 5500                             | 1.274224153                                                              | 1.4563         | 1.4348       | 23.26             | 34.46             | ok     |
| spectralnorm | nim (clang)       | 5500                             | 1.274224153                                                              | 1.0418         | 1.4322       | 23.26             | 24.81             | ok     |
| spectralnorm | ocaml (native)    | 5500                             | 1.274224153                                                              | 0.1317         | 4.4370       | 23.26             | 1009.95           | ok     |
| spectralnorm | moonbit (native)  | 5500                             | 1.274224153                                                              | 0.5427         | 20.4146      | 23.26             | 205.51            | ok     |
| startup      | c (gcc)           | -                                | ok                                                                       | 0.0591         | 0.0005       | 23.26             | 14.13             | ok     |
| startup      | c (clang)         | -                                | ok                                                                       | 0.0503         | 0.0005       | 23.26             | 4.55              | ok     |
| startup      | go (gc)           | -                                | ok                                                                       | 0.0880         | 0.0013       | 23.26             | 1538.77           | ok     |
| startup      | rust (rustc/llvm) | -                                | ok                                                                       | 2.0671         | 0.0007       | 23.26             | 300.38            | ok     |
| startup      | nim (gcc)         | -                                | ok                                                                       | 0.6304         | 0.0005       | 23.26             | 26.29             | ok     |
| startup      | nim (clang)       | -                                | ok                                                                       | 0.4139         | 0.0005       | 23.26             | 5.88              | ok     |
| startup      | ocaml (native)    | -                                | ok                                                                       | 0.0749         | 0.0010       | 23.26             | 409.35            | ok     |
| startup      | moonbit (native)  | -                                | ok                                                                       | 0.4422         | 0.0007       | 23.26             | 160.05            | ok     |
