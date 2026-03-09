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

| Overall | Entry             | Normalized Score | Speed      | Memory     | Build      | Size       |
| ------- | ----------------- | ---------------- | ---------- | ---------- | ---------- | ---------- |
| 1       | c (clang)         | 0.8409           | 3 (0.7626) | 4 (0.9405) | 1 (0.9529) | 1 (1.0000) |
| 2       | c (gcc)           | 0.7917           | 1 (0.7893) | 5 (0.9404) | 2 (0.7921) | 2 (0.5080) |
| 3       | nim (clang)       | 0.6661           | 5 (0.7423) | 7 (0.8967) | 6 (0.1130) | 3 (0.3004) |
| 4       | nim (gcc)         | 0.6595           | 4 (0.7515) | 8 (0.8967) | 7 (0.0897) | 4 (0.2029) |
| 5       | rust (rustc/llvm) | 0.6471           | 2 (0.7684) | 6 (0.8976) | 8 (0.0421) | 6 (0.0230) |
| 6       | ocaml (native)    | 0.6076           | 7 (0.5630) | 3 (0.9645) | 3 (0.7615) | 7 (0.0075) |
| 7       | go (gc)           | 0.5978           | 6 (0.5871) | 2 (0.9675) | 4 (0.5156) | 8 (0.0048) |
| 8       | moonbit (native)  | 0.3379           | 8 (0.1898) | 1 (1.0000) | 5 (0.2034) | 5 (0.0369) |

_Overall rank and per-metric columns use normalized per-benchmark scoring. Overall applies the configured metric weights; each per-metric column uses benchmark weights for that metric only._

| Benchmark    | Entry             | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (gcc)           | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.3347         | 14.6220      | 258.18            | 18.17             | ok     |
| binarytrees  | c (clang)         | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1959         | 14.9943      | 258.05            | 5.72              | ok     |
| binarytrees  | go (gc)           | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 3.0976         | 20.8547      | 203.32            | 1554.83           | ok     |
| binarytrees  | rust (rustc/llvm) | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 2.8455         | 16.9910      | 449.86            | 304.27            | ok     |
| binarytrees  | nim (gcc)         | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 1.3491         | 7.3722       | 457.12            | 38.52             | ok     |
| binarytrees  | nim (clang)       | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.9824         | 7.0443       | 457.11            | 26.38             | ok     |
| binarytrees  | ocaml (native)    | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.1689         | 3.9354       | 208.24            | 1006.33           | ok     |
| binarytrees  | moonbit (native)  | 21                               | stretch tree of depth 22	 check: 8388607 / 2097152	 trees of depth 4	... | 0.5419         | 5.5249       | 162.02            | 200.94            | ok     |
| fannkuch     | c (gcc)           | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1188         | 0.0838       | 22.98             | 14.20             | ok     |
| fannkuch     | c (clang)         | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1022         | 0.0836       | 22.98             | 6.71              | ok     |
| fannkuch     | go (gc)           | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1274         | 0.0848       | 22.98             | 1554.83           | ok     |
| fannkuch     | rust (rustc/llvm) | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 2.5612         | 0.0773       | 22.98             | 305.47            | ok     |
| fannkuch     | nim (gcc)         | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 1.2681         | 0.0839       | 22.98             | 34.46             | ok     |
| fannkuch     | nim (clang)       | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 1.0859         | 0.0683       | 22.98             | 25.07             | ok     |
| fannkuch     | ocaml (native)    | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1534         | 0.1224       | 22.98             | 1009.77           | ok     |
| fannkuch     | moonbit (native)  | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.5733         | 1.1109       | 22.98             | 203.75            | ok     |
| knucleotide  | c (gcc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1296         | 0.0061       | 22.98             | 14.33             | ok     |
| knucleotide  | c (clang)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1190         | 0.0053       | 22.98             | 9.18              | ok     |
| knucleotide  | go (gc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.3541         | 0.0106       | 22.98             | 1579.08           | ok     |
| knucleotide  | rust (rustc/llvm) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 3.0475         | 0.0054       | 22.98             | 347.73            | ok     |
| knucleotide  | nim (gcc)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.4112         | 0.0065       | 22.98             | 46.49             | ok     |
| knucleotide  | nim (clang)       | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1080         | 0.0097       | 22.98             | 32.41             | ok     |
| knucleotide  | ocaml (native)    | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1573         | 0.0246       | 22.98             | 1065.55           | ok     |
| knucleotide  | moonbit (native)  | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.5731         | 0.0728       | 22.98             | 193.98            | ok     |
| mandelbrot   | c (gcc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.0827         | 0.0135       | 22.98             | 14.14             | ok     |
| mandelbrot   | c (clang)         | 512                              | sha256:e41a9386e912a316                                                  | 0.0708         | 0.0139       | 22.98             | 5.81              | ok     |
| mandelbrot   | go (gc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.2939         | 0.0155       | 22.98             | 1546.83           | ok     |
| mandelbrot   | rust (rustc/llvm) | 512                              | sha256:e41a9386e912a316                                                  | 2.4845         | 0.0145       | 22.98             | 304.67            | ok     |
| mandelbrot   | nim (gcc)         | 512                              | sha256:e41a9386e912a316                                                  | 1.0968         | 0.0139       | 22.98             | 34.46             | ok     |
| mandelbrot   | nim (clang)       | 512                              | sha256:e41a9386e912a316                                                  | 0.8863         | 0.0136       | 22.98             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512                              | sha256:e41a9386e912a316                                                  | 0.1156         | 0.0157       | 22.98             | 1005.27           | ok     |
| mandelbrot   | moonbit (native)  | 512                              | sha256:e41a9386e912a316                                                  | 0.4859         | 0.0858       | 22.98             | 200.56            | ok     |
| nbody        | c (gcc)           | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1329         | 0.4691       | 22.98             | 14.15             | ok     |
| nbody        | c (clang)         | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1311         | 0.4166       | 22.98             | 8.78              | ok     |
| nbody        | go (gc)           | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1877         | 0.6086       | 22.98             | 1558.83           | ok     |
| nbody        | rust (rustc/llvm) | 10000000                         | -0.169075164 / -0.169077842                                              | 2.7016         | 0.3546       | 22.98             | 329.12            | ok     |
| nbody        | nim (gcc)         | 10000000                         | -0.169075164 / -0.169077842                                              | 1.3027         | 0.5234       | 22.98             | 34.46             | ok     |
| nbody        | nim (clang)       | 10000000                         | -0.169075164 / -0.169077842                                              | 1.0882         | 0.5298       | 22.98             | 28.04             | ok     |
| nbody        | ocaml (native)    | 10000000                         | -0.169075164 / -0.169077842                                              | 0.1567         | 0.6486       | 22.98             | 1006.45           | ok     |
| nbody        | moonbit (native)  | 10000000                         | -0.169075164 / -0.169077842                                              | 0.5841         | 6.3108       | 22.98             | 208.26            | ok     |
| spectralnorm | c (gcc)           | 5500                             | 1.274224153                                                              | 0.1499         | 0.8249       | 22.98             | 14.16             | ok     |
| spectralnorm | c (clang)         | 5500                             | 1.274224153                                                              | 0.1146         | 1.2655       | 22.98             | 8.99              | ok     |
| spectralnorm | go (gc)           | 5500                             | 1.274224153                                                              | 0.0967         | 1.3342       | 22.98             | 1554.83           | ok     |
| spectralnorm | rust (rustc/llvm) | 5500                             | 1.274224153                                                              | 2.2851         | 1.4811       | 22.98             | 329.27            | ok     |
| spectralnorm | nim (gcc)         | 5500                             | 1.274224153                                                              | 1.1241         | 1.3072       | 22.98             | 34.46             | ok     |
| spectralnorm | nim (clang)       | 5500                             | 1.274224153                                                              | 0.9332         | 1.2995       | 22.98             | 24.81             | ok     |
| spectralnorm | ocaml (native)    | 5500                             | 1.274224153                                                              | 0.1309         | 4.0735       | 22.98             | 1009.95           | ok     |
| spectralnorm | moonbit (native)  | 5500                             | 1.274224153                                                              | 0.5506         | 20.5397      | 22.98             | 205.51            | ok     |
| startup      | c (gcc)           | -                                | ok                                                                       | 0.0799         | 0.0006       | 22.98             | 14.13             | ok     |
| startup      | c (clang)         | -                                | ok                                                                       | 0.0574         | 0.0006       | 22.98             | 4.55              | ok     |
| startup      | go (gc)           | -                                | ok                                                                       | 0.1588         | 0.0013       | 22.98             | 1538.77           | ok     |
| startup      | rust (rustc/llvm) | -                                | ok                                                                       | 2.4834         | 0.0006       | 22.98             | 300.38            | ok     |
| startup      | nim (gcc)         | -                                | ok                                                                       | 0.7342         | 0.0005       | 22.98             | 26.29             | ok     |
| startup      | nim (clang)       | -                                | ok                                                                       | 0.4918         | 0.0006       | 22.98             | 5.88              | ok     |
| startup      | ocaml (native)    | -                                | ok                                                                       | 0.0960         | 0.0010       | 22.98             | 409.35            | ok     |
| startup      | moonbit (native)  | -                                | ok                                                                       | 0.5109         | 0.0016       | 22.98             | 160.05            | ok     |
