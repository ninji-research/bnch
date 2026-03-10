# Benchmark Report

## Environment

| Setting     | Value                                                              |
| ----------- | ------------------------------------------------------------------ |
| runs        | 3                                                                  |
| warmup      | 1                                                                  |
| build_jobs  | 16                                                                 |
| link_policy | toolchain-default release mode (mixed linkage; see entry metadata) |
| entries     | 8                                                                  |
| benchmarks  | 8                                                                  |
| gcc         | gcc (AerynOS) 15.2.1 20251024                                      |
| clang       | clang version 21.1.8 (AerynOS)                                     |
| go          | go version go1.26.0 linux/amd64                                    |
| rustc       | rustc 1.94.0 (4a4ef493e 2026-03-02)                                |
| nim         | Nim Compiler Version 2.2.8 [Linux: amd64]                          |
| ocamlopt    | 5.4.1                                                              |
| moon        | moon 0.1.20260309 (f21b520 2026-03-09)                             |
| strip       | GNU strip (GNU Binutils) 2.46.0                                    |

## Entries

| Entry             | Compiler | Backend | Linkage | Stripped | Binary Size Sample (KiB) |
| ----------------- | -------- | ------- | ------- | -------- | ------------------------ |
| c (gcc)           | gcc      | native  | dynamic | yes      | 18.17                    |
| c (clang)         | clang    | native  | dynamic | yes      | 5.72                     |
| go (gc)           | go       | native  | static  | yes      | 1554.83                  |
| rust (rustc/llvm) | rustc    | llvm    | dynamic | yes      | 304.27                   |
| nim (gcc)         | gcc      | c       | dynamic | yes      | 38.52                    |
| nim (clang)       | clang    | c       | dynamic | yes      | 26.38                    |
| ocaml (native)    | ocamlopt | native  | dynamic | yes      | 1006.33                  |
| moonbit (native)  | moon     | native  | dynamic | yes      | 201.15                   |

## Scoring Inputs

| Weight                 | Value |
| ---------------------- | ----- |
| metric:exec_time       | 0.60  |
| metric:peak_mem        | 0.20  |
| metric:build_time      | 0.10  |
| metric:bin_size        | 0.10  |
| benchmark:binarytrees  | 1.00  |
| benchmark:fasta        | 0.75  |
| benchmark:mandelbrot   | 1.00  |
| benchmark:spectralnorm | 1.00  |
| benchmark:fannkuch     | 1.00  |
| benchmark:nbody        | 1.00  |
| benchmark:knucleotide  | 1.00  |
| benchmark:revcomp      | 0.75  |

| Benchmark    | Algorithm                                                  | Time                     | Space                    | Output Contract                        | Fairness Notes                                                                                        |
| ------------ | ---------------------------------------------------------- | ------------------------ | ------------------------ | -------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| binarytrees  | bottom-up binary tree construction and checksum            | O(nodes built)           | O(max tree size)         | exact multiline text                   | Same tree/check workload; memory-management costs remain language-native.                             |
| fasta        | deterministic FASTA generation with buffered text emission | O(n)                     | O(1)                     | exact FASTA text                       | Adds text generation and formatting without turning the suite into a library benchmark.               |
| mandelbrot   | scalar Mandelbrot escape-time bitmap checksum              | O(size^2 * iter)         | O(1)                     | exact integer checksum                 | Input size is set to 512 because all retained implementations agree there exactly.                    |
| spectralnorm | power method on implicit matrix                            | O(n^2 * iterations)      | O(n)                     | one float rounded to 9 decimals        | Correctness compares canonical 9-decimal output, not raw printer differences.                         |
| fannkuch     | fannkuch-redux permutation flips                           | O(n! * n)                | O(n)                     | exact two-line text                    | Same permutation-generation strategy across entries.                                                  |
| nbody        | 5-body symplectic advance and energy                       | O(iterations * bodies^2) | O(1)                     | two floats rounded to 9 decimals       | Correctness compares canonical 9-decimal energies line-by-line.                                       |
| knucleotide  | FASTA parsing plus k-mer frequency and occurrence counting | O(n)                     | O(unique k-mers + input) | exact multiline text                   | Uses one committed deterministic FASTA fixture and processes only the >THREE section.                 |
| revcomp      | FASTA parsing plus reverse-complement text transformation  | O(n)                     | O(n)                     | FASTA text with case-insensitive bases | Adds streaming-style text transformation and output reshaping with the same committed fixture family. |

## Summary

| Overall | Entry             | Score  | Speed | Memory | Build | Size |
| ------- | ----------------- | ------ | ----- | ------ | ----- | ---- |
| 1       | c (clang)         | 0.8556 | 3     | 3      | 1     | 1    |
| 2       | c (gcc)           | 0.8175 | 1     | 2      | 2     | 2    |
| 3       | rust (rustc/llvm) | 0.6549 | 2     | 6      | 8     | 6    |
| 4       | nim (clang)       | 0.6516 | 4     | 8      | 6     | 3    |
| 5       | nim (gcc)         | 0.6363 | 5     | 7      | 7     | 4    |
| 6       | go (gc)           | 0.6356 | 6     | 4      | 3     | 8    |
| 7       | ocaml (native)    | 0.5816 | 7     | 5      | 4     | 7    |
| 8       | moonbit (native)  | 0.3184 | 8     | 1      | 5     | 5    |

_Overall score uses normalized per-benchmark scoring with the configured metric weights. Per-metric columns show rank only, using that metric's normalized score across the scored benchmarks._

## Results

| Benchmark    | Entry             | Input                            | Output                                                                   | Build Time (s) | Run Time (s) | Peak Memory (MiB) | Binary Size (KiB) | Status |
| ------------ | ----------------- | -------------------------------- | ------------------------------------------------------------------------ | -------------- | ------------ | ----------------- | ----------------- | ------ |
| binarytrees  | c (gcc)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.2050         | 7.4284       | 130.20            | 18.17             | ok     |
| binarytrees  | c (clang)         | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.0848         | 8.1104       | 130.21            | 5.72              | ok     |
| binarytrees  | go (gc)           | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 3.5861         | 8.5969       | 137.06            | 1554.83           | ok     |
| binarytrees  | rust (rustc/llvm) | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 2.5914         | 9.8341       | 257.95            | 304.27            | ok     |
| binarytrees  | nim (gcc)         | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.4608         | 4.3667       | 263.92            | 38.52             | ok     |
| binarytrees  | nim (clang)       | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 1.0869         | 4.2807       | 262.11            | 26.38             | ok     |
| binarytrees  | ocaml (native)    | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.1553         | 2.6092       | 132.47            | 1006.33           | ok     |
| binarytrees  | moonbit (native)  | 20                               | stretch tree of depth 21	 check: 4194303 / 1048576	 trees of depth 4	... | 0.6086         | 3.2440       | 98.11             | 201.15            | ok     |
| fannkuch     | c (gcc)           | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1182         | 0.1017       | 57.22             | 14.20             | ok     |
| fannkuch     | c (clang)         | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1058         | 0.0841       | 57.22             | 6.71              | ok     |
| fannkuch     | go (gc)           | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1290         | 0.0879       | 57.22             | 1554.83           | ok     |
| fannkuch     | rust (rustc/llvm) | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 2.6250         | 0.0800       | 57.22             | 305.47            | ok     |
| fannkuch     | nim (gcc)         | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 1.3353         | 0.0876       | 57.22             | 34.46             | ok     |
| fannkuch     | nim (clang)       | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 1.0837         | 0.0704       | 57.22             | 25.07             | ok     |
| fannkuch     | ocaml (native)    | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.1532         | 0.1275       | 57.22             | 1009.77           | ok     |
| fannkuch     | moonbit (native)  | 10                               | 2628 / Pfannkuchen(10) = 28                                              | 0.5888         | 1.1095       | 57.22             | 203.71            | ok     |
| fasta        | c (gcc)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1131         | 0.0314       | 39.95             | 14.16             | ok     |
| fasta        | c (clang)         | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1106         | 0.0319       | 42.69             | 7.45              | ok     |
| fasta        | go (gc)           | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.2815         | 0.0344       | 45.12             | 1551.20           | ok     |
| fasta        | rust (rustc/llvm) | 250000                           | sha256:dfd37a44ede2e23f                                                  | 2.5955         | 0.0317       | 47.47             | 311.83            | ok     |
| fasta        | nim (gcc)         | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.4504         | 0.0342       | 49.97             | 42.52             | ok     |
| fasta        | nim (clang)       | 250000                           | sha256:dfd37a44ede2e23f                                                  | 1.1293         | 0.0328       | 52.34             | 28.00             | ok     |
| fasta        | ocaml (native)    | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.1554         | 0.0487       | 54.76             | 1015.52           | ok     |
| fasta        | moonbit (native)  | 250000                           | sha256:dfd37a44ede2e23f                                                  | 0.5922         | 0.2568       | 57.22             | 203.12            | ok     |
| knucleotide  | c (gcc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1291         | 0.0062       | 57.22             | 14.33             | ok     |
| knucleotide  | c (clang)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1273         | 0.0057       | 57.22             | 9.18              | ok     |
| knucleotide  | go (gc)           | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1859         | 0.0103       | 57.22             | 1579.08           | ok     |
| knucleotide  | rust (rustc/llvm) | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 3.0977         | 0.0055       | 57.22             | 347.73            | ok     |
| knucleotide  | nim (gcc)         | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.4383         | 0.0076       | 57.22             | 46.49             | ok     |
| knucleotide  | nim (clang)       | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 1.1162         | 0.0090       | 57.22             | 32.41             | ok     |
| knucleotide  | ocaml (native)    | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.1642         | 0.0244       | 57.22             | 1065.55           | ok     |
| knucleotide  | moonbit (native)  | fixture:knucleotide-250000.fasta | A 30.328 / T 30.079 / C 19.799 / G 19.794 /  / AA 9.188 / TA 9.122 / ... | 0.5857         | 0.0741       | 57.22             | 193.38            | ok     |
| mandelbrot   | c (gcc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.0997         | 0.0140       | 57.22             | 14.14             | ok     |
| mandelbrot   | c (clang)         | 512                              | sha256:e41a9386e912a316                                                  | 0.0820         | 0.0145       | 57.22             | 5.81              | ok     |
| mandelbrot   | go (gc)           | 512                              | sha256:e41a9386e912a316                                                  | 0.1054         | 0.0173       | 57.22             | 1546.83           | ok     |
| mandelbrot   | rust (rustc/llvm) | 512                              | sha256:e41a9386e912a316                                                  | 2.5340         | 0.0155       | 57.22             | 304.67            | ok     |
| mandelbrot   | nim (gcc)         | 512                              | sha256:e41a9386e912a316                                                  | 1.2988         | 0.0139       | 57.22             | 34.46             | ok     |
| mandelbrot   | nim (clang)       | 512                              | sha256:e41a9386e912a316                                                  | 1.0769         | 0.0144       | 57.22             | 24.16             | ok     |
| mandelbrot   | ocaml (native)    | 512                              | sha256:e41a9386e912a316                                                  | 0.1449         | 0.0161       | 57.22             | 1005.27           | ok     |
| mandelbrot   | moonbit (native)  | 512                              | sha256:e41a9386e912a316                                                  | 0.5831         | 0.0971       | 57.22             | 200.52            | ok     |
| nbody        | c (gcc)           | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1330         | 0.2444       | 57.22             | 14.15             | ok     |
| nbody        | c (clang)         | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1127         | 0.2173       | 57.22             | 8.78              | ok     |
| nbody        | go (gc)           | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1225         | 0.3166       | 57.22             | 1558.83           | ok     |
| nbody        | rust (rustc/llvm) | 5000000                          | -0.169075164 / -0.169083134                                              | 2.7502         | 0.1809       | 57.22             | 329.12            | ok     |
| nbody        | nim (gcc)         | 5000000                          | -0.169075164 / -0.169083134                                              | 1.3258         | 0.2668       | 57.22             | 34.46             | ok     |
| nbody        | nim (clang)       | 5000000                          | -0.169075164 / -0.169083134                                              | 1.1029         | 0.2707       | 57.22             | 28.04             | ok     |
| nbody        | ocaml (native)    | 5000000                          | -0.169075164 / -0.169083134                                              | 0.1644         | 0.3338       | 57.22             | 1006.45           | ok     |
| nbody        | moonbit (native)  | 5000000                          | -0.169075164 / -0.169083134                                              | 0.6008         | 3.3953       | 57.22             | 208.28            | ok     |
| revcomp      | c (gcc)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1250         | 0.0013       | 57.22             | 14.19             | ok     |
| revcomp      | c (clang)         | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.0939         | 0.0019       | 57.22             | 6.69              | ok     |
| revcomp      | go (gc)           | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1122         | 0.0023       | 57.22             | 1467.23           | ok     |
| revcomp      | rust (rustc/llvm) | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 2.6308         | 0.0019       | 57.22             | 312.20            | ok     |
| revcomp      | nim (gcc)         | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 1.1953         | 0.0037       | 57.22             | 34.49             | ok     |
| revcomp      | nim (clang)       | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.9789         | 0.0035       | 57.22             | 26.02             | ok     |
| revcomp      | ocaml (native)    | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.1226         | 0.0049       | 57.22             | 774.70            | ok     |
| revcomp      | moonbit (native)  | fixture:knucleotide-250000.fasta | sha256:14899a73679b1d83                                                  | 0.5725         | 0.0591       | 57.22             | 180.62            | ok     |
| spectralnorm | c (gcc)           | 5000                             | 1.274224153                                                              | 0.1746         | 0.7176       | 57.22             | 14.16             | ok     |
| spectralnorm | c (clang)         | 5000                             | 1.274224153                                                              | 0.1471         | 1.1471       | 57.22             | 8.99              | ok     |
| spectralnorm | go (gc)           | 5000                             | 1.274224153                                                              | 0.1265         | 1.2339       | 57.22             | 1554.83           | ok     |
| spectralnorm | rust (rustc/llvm) | 5000                             | 1.274224153                                                              | 2.7609         | 1.3191       | 57.22             | 329.27            | ok     |
| spectralnorm | nim (gcc)         | 5000                             | 1.274224153                                                              | 1.3551         | 1.1904       | 57.22             | 34.46             | ok     |
| spectralnorm | nim (clang)       | 5000                             | 1.274224153                                                              | 1.1041         | 1.2183       | 57.22             | 24.81             | ok     |
| spectralnorm | ocaml (native)    | 5000                             | 1.274224153                                                              | 0.1628         | 3.8964       | 57.22             | 1009.95           | ok     |
| spectralnorm | moonbit (native)  | 5000                             | 1.274224153                                                              | 0.6121         | 17.9011      | 57.22             | 205.59            | ok     |
