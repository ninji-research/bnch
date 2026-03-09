#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import math
import os
import shlex
import shutil
import stat
import subprocess
import sys
import textwrap
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
BIN = ROOT / "bin"
BUILD = ROOT / ".build"
DEFAULT_REPORT = ROOT / "REPORT.md"

METRIC_WEIGHTS = {
    "exec_time": 0.60,
    "peak_mem": 0.20,
    "build_time": 0.10,
    "bin_size": 0.10,
}


@dataclass(frozen=True)
class BenchmarkSpec:
    name: str
    args: tuple[str, ...]
    weight: float
    check: str
    algorithm: str
    time_complexity: str
    space_complexity: str
    output_contract: str
    fairness_notes: str


@dataclass(frozen=True)
class EntrySpec:
    key: str
    label: str
    language: str
    compiler: str
    backend: str
    linker: str


@dataclass
class Result:
    benchmark: str
    entry: str
    input_text: str
    raw_output: str
    output_text: str
    reference_text: str
    status: str
    build_command: str
    build_time: float
    exec_time: float
    peak_mem_kib: int
    bin_size: int
    binary_path: Path


BENCHMARKS: tuple[BenchmarkSpec, ...] = (
    BenchmarkSpec("binarytrees", ("21",), 1.00, "exact", "bottom-up binary tree construction and checksum", "O(nodes built)", "O(max tree size)", "exact multiline text", "Same tree/check workload; memory-management costs remain language-native."),
    BenchmarkSpec("mandelbrot", ("512",), 1.00, "exact", "scalar Mandelbrot escape-time bitmap checksum", "O(size^2 * iter)", "O(1)", "exact integer checksum", "Input size is set to 512 because all retained implementations agree there exactly."),
    BenchmarkSpec("spectralnorm", ("5500",), 1.00, "float_9", "power method on implicit matrix", "O(n^2 * iterations)", "O(n)", "one float rounded to 9 decimals", "Correctness compares canonical 9-decimal output, not raw printer differences."),
    BenchmarkSpec("fannkuch", ("10",), 1.00, "exact", "fannkuch-redux permutation flips", "O(n! * n)", "O(n)", "exact two-line text", "Same permutation-generation strategy across entries."),
    BenchmarkSpec("nbody", ("10000000",), 1.00, "float_9_lines", "5-body symplectic advance and energy", "O(iterations * bodies^2)", "O(1)", "two floats rounded to 9 decimals", "Correctness compares canonical 9-decimal energies line-by-line."),
    BenchmarkSpec("startup", (), 0.25, "exact", "process startup and hello-world print", "O(1)", "O(1)", "exact single line", "Useful signal for runtime/toolchain startup, but intentionally low ranking impact."),
)


def sh(command: list[str], cwd: Path | None = None, capture: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    env["TZ"] = "UTC"
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=capture,
        text=True,
        check=False,
    )


def timed(command: list[str], cwd: Path | None = None) -> tuple[subprocess.CompletedProcess[str], float, int]:
    env = os.environ.copy()
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    env["TZ"] = "UTC"
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8") as stdout_file, tempfile.NamedTemporaryFile(
        "w+", encoding="utf-8"
    ) as stderr_file:
        start = time.perf_counter()
        proc = subprocess.Popen(
            command,
            cwd=str(cwd) if cwd else None,
            env=env,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
        )
        _, status, usage = os.wait4(proc.pid, 0)
        end = time.perf_counter()
        stdout_file.seek(0)
        stderr_file.seek(0)
        completed = subprocess.CompletedProcess(
            command,
            os.waitstatus_to_exitcode(status),
            stdout_file.read(),
            stderr_file.read().strip(),
        )
        return completed, end - start, usage.ru_maxrss


def tool(name: str) -> str | None:
    return shutil.which(name)


def version_line(command: list[str]) -> str:
    proc = sh(command)
    text = (proc.stdout or proc.stderr).strip().splitlines()
    return text[0].strip() if text else ""


def version_or_dash(command: list[str]) -> str:
    return version_line(command) if tool(command[0]) else "-"


def ocaml_config_value(key: str) -> str:
    proc = sh(["ocamlopt", "-config"])
    for line in proc.stdout.splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    return ""


def cpu_count() -> int:
    return os.cpu_count() or 1


def entries() -> list[EntrySpec]:
    active: list[EntrySpec] = []
    if tool("gcc"):
        active.append(EntrySpec("c__gcc", "c (gcc)", "c", "gcc", "native", "default"))
    if tool("clang"):
        active.append(EntrySpec("c__clang", "c (clang)", "c", "clang", "native", "lld"))
    if tool("rustc"):
        active.append(EntrySpec("rust__llvm", "rust (rustc/llvm)", "rust", "rustc", "llvm", "lld"))
    if tool("nim") and tool("gcc"):
        active.append(EntrySpec("nim__gcc", "nim (gcc)", "nim", "gcc", "c", "default"))
    if tool("nim") and tool("clang"):
        active.append(EntrySpec("nim__clang", "nim (clang)", "nim", "clang", "c", "lld"))
    if tool("ocamlopt"):
        active.append(EntrySpec("ocaml__native", "ocaml (native)", "ocaml", "ocamlopt", "native", ocaml_config_value("c_compiler") or "default"))
    if tool("moon"):
        active.append(EntrySpec("moonbit__native", "moonbit (native)", "moonbit", "moon", "native", "host"))
    return active


def source_path(benchmark: str, entry: EntrySpec) -> Path:
    root = SRC / benchmark
    if entry.language == "c":
        return root / f"{benchmark}.c"
    if entry.language == "rust":
        return root / f"{benchmark}.rs"
    if entry.language == "nim":
        return root / f"{benchmark}.nim"
    if entry.language == "ocaml":
        return root / f"{benchmark}.ml"
    if entry.language == "moonbit":
        return root / f"moonbit_{benchmark}"
    raise ValueError(f"unsupported language: {entry.language}")


def benchmark_args(spec: BenchmarkSpec) -> tuple[str, ...]:
    return spec.args


def build_command(spec: BenchmarkSpec, entry: EntrySpec, binary: Path, build_dir: Path, build_jobs: int) -> list[str]:
    source = source_path(spec.name, entry)
    if entry.language == "c":
        cmd = [
            entry.compiler,
            "-O3",
            "-flto",
            "-march=native",
            "-mtune=native",
            "-fomit-frame-pointer",
            "-fno-math-errno",
            "-fno-trapping-math",
            "-pipe",
            "-s",
        ]
        if entry.compiler == "clang":
            cmd.append("-fuse-ld=lld")
        cmd.extend(["-o", str(binary), str(source), "-lm", "-lpthread"])
        return cmd
    if entry.language == "rust":
        return [
            "rustc",
            str(source),
            "-O",
            "-C",
            "target-cpu=native",
            "-C",
            "lto=fat",
            "-C",
            "codegen-units=1",
            "-C",
            "panic=abort",
            "-C",
            "strip=symbols",
            "-o",
            str(binary),
        ]
    if entry.language == "nim":
        cmd = [
            "nim",
            "c",
            "-d:danger",
            "-d:lto",
            "--opt:speed",
            "--mm:orc",
            "--threads:on",
            f"--cc:{entry.compiler}",
            f"--out:{binary}",
            f"--nimcache:{build_dir / 'nimcache'}",
            "--passC:-O3",
            "--passC:-flto",
            "--passC:-march=native",
            "--passC:-mtune=native",
            "--passC:-fomit-frame-pointer",
            "--passC:-pipe",
            "--passL:-flto",
            "--passL:-s",
        ]
        if entry.compiler == "clang":
            cmd.append("--passL:-fuse-ld=lld")
        cmd.append(str(source))
        return cmd
    if entry.language == "ocaml":
        return [
            "ocamlopt",
            "-O3",
            "-unsafe",
            "-nodynlink",
            "-o",
            str(binary),
            "-ccopt",
            "-O3",
            "-ccopt",
            "-march=native",
            "-ccopt",
            "-mtune=native",
            "-ccopt",
            "-fomit-frame-pointer",
            "-ccopt",
            "-pipe",
            str(source),
        ]
    if entry.language == "moonbit":
        return [
            "moon",
            "build",
            "--release",
            "--strip",
            "--target",
            "native",
            "--frozen",
            "--jobs",
            str(build_jobs),
            "--target-dir",
            str(build_dir),
            "--quiet",
        ]
    raise ValueError(f"unsupported language: {entry.language}")


def find_moonbit_binary(build_dir: Path) -> Path:
    candidates: list[Path] = []
    for path in build_dir.rglob("*"):
        if not path.is_file():
            continue
        if not os.access(path, os.X_OK):
            continue
        if path.suffix in {".o", ".a", ".so", ".dll", ".dylib"}:
            continue
        candidates.append(path)
    if not candidates:
        raise FileNotFoundError(f"no moonbit binary under {build_dir}")
    return max(candidates, key=lambda path: path.stat().st_mtime_ns)


def clean_dirs() -> None:
    for path in (BIN, BUILD):
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def cleanup_source_tree() -> None:
    removable_suffixes = {
        ".o",
        ".obj",
        ".cmi",
        ".cmo",
        ".cmx",
        ".cmxa",
        ".cmxs",
        ".cmt",
        ".cmti",
        ".annot",
    }
    removable_dirs = {"_build", "target", "nimcache"}
    for path in SRC.rglob("*"):
        if path.is_dir() and path.name in removable_dirs:
            shutil.rmtree(path, ignore_errors=True)
        elif path.is_file() and path.suffix in removable_suffixes:
            path.unlink(missing_ok=True)


def format_input(args: Iterable[str]) -> str:
    text = " ".join(args)
    return text if text else "-"


def normalize_output(text: str) -> str:
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines).strip()


def compact_output(benchmark: str, text: str) -> str:
    if not text:
        return "-"
    if benchmark == "mandelbrot":
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        return f"sha256:{digest}"
    one_line = text.replace("\n", " / ")
    return one_line if len(one_line) <= 72 else one_line[:69] + "..."


def parse_first_float(text: str) -> float:
    for token in text.replace("\n", " ").split():
        try:
            return float(token)
        except ValueError:
            continue
    raise ValueError(f"no float in output: {text!r}")


def format_fixed(value: float, digits: int) -> str:
    return f"{value:.{digits}f}"


def canonical_output(spec: BenchmarkSpec, text: str) -> str:
    normalized = normalize_output(text)
    if spec.check == "exact":
        return normalized
    if spec.check == "float_9":
        return format_fixed(parse_first_float(normalized), 9)
    if spec.check == "float_5":
        return format_fixed(parse_first_float(normalized), 5)
    if spec.check == "float_9_lines":
        return "\n".join(format_fixed(parse_first_float(line), 9) for line in normalized.splitlines())
    raise ValueError(f"unsupported check type: {spec.check}")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))
    parts = []
    parts.append("| " + " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)) + " |")
    parts.append("| " + " | ".join("-" * widths[index] for index in range(len(headers))) + " |")
    for row in rows:
        parts.append("| " + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)) + " |")
    return "\n".join(parts)


def fmt_seconds(value: float) -> str:
    return f"{value:.4f}"


def fmt_mib(kib: int) -> str:
    return f"{kib / 1024.0:.2f}"


def fmt_kib(value: int) -> str:
    return f"{value / 1024.0:.2f}"


def strip_binary(path: Path) -> float:
    if not path.exists() or not tool("strip"):
        return 0.0
    start = time.perf_counter()
    proc = sh(["strip", "--strip-all", str(path)])
    end = time.perf_counter()
    return end - start if proc.returncode == 0 else 0.0


def actual_linkage(path: Path) -> str:
    proc = sh(["readelf", "-lW", str(path)])
    if proc.returncode != 0:
        return "-"
    return "dynamic" if " INTERP " in proc.stdout else "static"


def stripped_state(path: Path) -> str:
    proc = sh(["file", str(path)])
    if proc.returncode != 0:
        return "-"
    text = proc.stdout.strip()
    if "not stripped" in text:
        return "no"
    if "stripped" in text:
        return "yes"
    return "-"


def metric_value(result: Result, metric: str) -> float:
    if metric == "exec_time":
        return result.exec_time
    if metric == "peak_mem":
        return float(result.peak_mem_kib)
    if metric == "build_time":
        return result.build_time
    if metric == "bin_size":
        return float(result.bin_size)
    raise ValueError(metric)


def scored_benchmarks(results: list[Result], benchmarks: list[BenchmarkSpec], active_entries: list[str] | None = None) -> list[BenchmarkSpec]:
    allowed_entries = set(active_entries) if active_entries is not None else None
    usable: list[BenchmarkSpec] = []
    for spec in benchmarks:
        rows = [row for row in results if row.benchmark == spec.name]
        if allowed_entries is not None:
            rows = [row for row in rows if row.entry in allowed_entries]
        if rows and all(row.status == "ok" for row in rows):
            usable.append(spec)
    return usable


def scores(results: list[Result], benchmarks: list[BenchmarkSpec]) -> dict[str, float]:
    valid_benchmarks = scored_benchmarks(results, benchmarks)
    by_benchmark: dict[str, list[Result]] = {}
    for result in results:
        if result.status == "ok":
            by_benchmark.setdefault(result.benchmark, []).append(result)

    complete_entries = {
        result.entry
        for result in results
        if all(
            any(item.entry == result.entry and item.benchmark == spec.name and item.status == "ok" for item in results)
            for spec in valid_benchmarks
        )
    }
    if not complete_entries:
        return {}

    totals = {entry: 0.0 for entry in complete_entries}
    total_weight = 0.0
    for spec in valid_benchmarks:
        rows = [row for row in by_benchmark.get(spec.name, []) if row.entry in complete_entries]
        if not rows:
            continue
        for metric, metric_weight in METRIC_WEIGHTS.items():
            best = min(metric_value(row, metric) for row in rows)
            if best <= 0:
                continue
            weight = spec.weight * metric_weight
            total_weight += weight
            for row in rows:
                totals[row.entry] += weight * (best / metric_value(row, metric))
    if total_weight == 0:
        return {}
    return {entry: totals[entry] / total_weight for entry in complete_entries}


def environment_rows(run_args: argparse.Namespace, active_entries: list[EntrySpec], benchmarks: list[BenchmarkSpec]) -> list[list[str]]:
    return [
        ["runs", str(run_args.runs)],
        ["warmup", str(run_args.warmup)],
        ["build_jobs", str(run_args.build_jobs)],
        ["link_policy", "dynamic (uniform default; moon native exposes no static toggle here)"],
        ["entries", str(len(active_entries))],
        ["benchmarks", str(len(benchmarks))],
        ["gcc", version_or_dash(["gcc", "--version"])],
        ["clang", version_or_dash(["clang", "--version"])],
        ["rustc", version_or_dash(["rustc", "--version"])],
        ["nim", version_or_dash(["nim", "--version"])],
        ["ocamlopt", version_or_dash(["ocamlopt", "-version"])],
        ["moon", version_or_dash(["moon", "version"])],
        ["strip", version_or_dash(["strip", "--version"])],
    ]


def entry_rows(active_entries: list[EntrySpec], results: list[Result]) -> list[list[str]]:
    sample_for_entry: dict[str, Result] = {}
    for result in results:
        if result.status == "ok" and result.benchmark == "startup":
            sample_for_entry[result.entry] = result
    for result in results:
        sample_for_entry.setdefault(result.entry, result)

    rows: list[list[str]] = []
    for entry in active_entries:
        sample = sample_for_entry.get(entry.key)
        linkage = actual_linkage(sample.binary_path) if sample and sample.binary_path.exists() else "-"
        stripped = stripped_state(sample.binary_path) if sample and sample.binary_path.exists() else "-"
        rows.append(
            [
                entry.label,
                entry.compiler,
                entry.backend,
                linkage,
                stripped,
                fmt_kib(sample.bin_size) if sample else "-",
            ]
        )
    return rows


def ranking_rows(score_map: dict[str, float], active_entries: list[EntrySpec]) -> list[list[str]]:
    labels = {entry.key: entry.label for entry in active_entries}
    ordered = sorted(score_map.items(), key=lambda item: item[1], reverse=True)
    return [[str(index), labels[key], f"{score:.4f}"] for index, (key, score) in enumerate(ordered, start=1)]


def result_rows(results: list[Result], active_entries: list[EntrySpec]) -> list[list[str]]:
    order = {entry.key: index for index, entry in enumerate(active_entries)}
    rows: list[list[str]] = []
    for result in sorted(results, key=lambda item: (item.benchmark, order.get(item.entry, 999), item.entry)):
        rows.append(
            [
                result.benchmark,
                next(entry.label for entry in active_entries if entry.key == result.entry),
                result.input_text,
                result.output_text,
                fmt_seconds(result.build_time),
                fmt_seconds(result.exec_time),
                fmt_mib(result.peak_mem_kib),
                fmt_kib(result.bin_size),
                result.status,
            ]
        )
    return rows


def mismatch_rows(results: list[Result], active_entries: list[EntrySpec]) -> list[list[str]]:
    labels = {entry.key: entry.label for entry in active_entries}
    rows: list[list[str]] = []
    for result in results:
        if result.status == "ok":
            continue
        rows.append(
            [
                result.benchmark,
                labels.get(result.entry, result.entry),
                result.output_text,
                result.reference_text,
                result.status,
            ]
        )
    return rows


def weight_rows(benchmarks: list[BenchmarkSpec]) -> list[list[str]]:
    rows = [[f"metric:{name}", f"{weight:.2f}"] for name, weight in METRIC_WEIGHTS.items()]
    rows.extend([["benchmark:" + spec.name, f"{spec.weight:.2f}"] for spec in benchmarks])
    return rows


def benchmark_rows(benchmarks: list[BenchmarkSpec]) -> list[list[str]]:
    return [
        [
            spec.name,
            spec.algorithm,
            spec.time_complexity,
            spec.space_complexity,
            spec.output_contract,
            spec.fairness_notes,
        ]
        for spec in benchmarks
    ]


def excluded_benchmark_rows(results: list[Result], benchmarks: list[BenchmarkSpec], active_entries: list[EntrySpec]) -> list[list[str]]:
    valid = {spec.name for spec in scored_benchmarks(results, benchmarks, [entry.key for entry in active_entries])}
    rows: list[list[str]] = []
    for spec in benchmarks:
        if spec.name in valid:
            continue
        statuses = sorted({row.status for row in results if row.benchmark == spec.name})
        reason = "output divergence or build/run failure"
        if statuses:
            reason = ", ".join(statuses)
        rows.append([spec.name, reason])
    return rows


def render_report(
    run_args: argparse.Namespace,
    active_entries: list[EntrySpec],
    benchmarks: list[BenchmarkSpec],
    results: list[Result],
) -> str:
    content = [
        "# Benchmark Report",
        "",
        markdown_table(["Setting", "Value"], environment_rows(run_args, active_entries, benchmarks)),
        "",
        markdown_table(["Weight", "Value"], weight_rows(benchmarks)),
        "",
        markdown_table(
            ["Benchmark", "Algorithm", "Time", "Space", "Output Contract", "Fairness Notes"],
            benchmark_rows(benchmarks),
        ),
        "",
        markdown_table(
            ["Entry", "Compiler", "Backend", "Linkage", "Stripped", "Binary Size (KiB)"],
            entry_rows(active_entries, results),
        ),
        "",
    ]

    excluded = excluded_benchmark_rows(results, benchmarks, active_entries)
    if excluded:
        content.extend(
            [
                markdown_table(["Excluded From Score", "Reason"], excluded),
                "",
            ]
        )

    score_map = scores(results, benchmarks)
    if score_map:
        content.extend(
            [
                markdown_table(["Rank", "Entry", "Score"], ranking_rows(score_map, active_entries)),
                "",
            ]
        )

    content.append(
        markdown_table(
            ["Benchmark", "Entry", "Input", "Output", "Build Time (s)", "Run Time (s)", "Peak Memory (MiB)", "Binary Size (KiB)", "Status"],
            result_rows(results, active_entries),
        )
    )
    mismatches = mismatch_rows(results, active_entries)
    if mismatches:
        content.extend(
            [
                "",
                "## Mismatches",
                "",
                markdown_table(["Benchmark", "Entry", "Output", "Reference", "Status"], mismatches),
            ]
        )
    content.append("")
    return "\n".join(content)


def build_and_run(spec: BenchmarkSpec, entry: EntrySpec, run_args: argparse.Namespace) -> tuple[Result, str]:
    binary = BIN / f"{spec.name}__{entry.key}"
    build_dir = BUILD / f"{spec.name}__{entry.key}"
    build_dir.mkdir(parents=True, exist_ok=True)
    binary.parent.mkdir(parents=True, exist_ok=True)

    source = source_path(spec.name, entry)
    command = build_command(spec, entry, binary, build_dir, run_args.build_jobs)
    command_text = shlex.join(command)
    build_cwd = source if entry.language == "moonbit" else None

    build_proc, build_time, _ = timed(command, cwd=build_cwd)
    if build_proc.returncode != 0:
        stderr = build_proc.stderr or build_proc.stdout or "build failed"
        return (
            Result(
                benchmark=spec.name,
                entry=entry.key,
                input_text=format_input(benchmark_args(spec)),
                raw_output="",
                output_text="-",
                reference_text="-",
                status="build-fail",
                build_command=command_text,
                build_time=build_time,
                exec_time=0.0,
                peak_mem_kib=0,
                bin_size=0,
                binary_path=binary,
            ),
            command_text + " // " + textwrap.shorten(stderr.replace("\n", " "), width=160, placeholder="..."),
        )

    if entry.language == "moonbit":
        built = find_moonbit_binary(build_dir)
        shutil.copy2(built, binary)
        binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    build_time += strip_binary(binary)

    args = benchmark_args(spec)
    exec_times: list[float] = []
    peak_kibs: list[int] = []
    output = "-"

    for _ in range(run_args.warmup):
        warm_proc, _, _ = timed([str(binary), *args])
        if warm_proc.returncode != 0:
            stderr = warm_proc.stderr or warm_proc.stdout or "run failed"
            return (
                Result(
                    benchmark=spec.name,
                    entry=entry.key,
                    input_text=format_input(args),
                    raw_output="",
                    output_text="-",
                    reference_text="-",
                    status="run-fail",
                    build_command=command_text,
                    build_time=build_time,
                    exec_time=0.0,
                    peak_mem_kib=0,
                    bin_size=binary.stat().st_size if binary.exists() else 0,
                    binary_path=binary,
                ),
                command_text + " // " + textwrap.shorten(stderr.replace("\n", " "), width=160, placeholder="..."),
            )

    for _ in range(run_args.runs):
        run_proc, exec_time, peak_kib = timed([str(binary), *args])
        if run_proc.returncode != 0:
            stderr = run_proc.stderr or run_proc.stdout or "run failed"
            return (
                Result(
                    benchmark=spec.name,
                    entry=entry.key,
                    input_text=format_input(args),
                    raw_output="",
                    output_text="-",
                    reference_text="-",
                    status="run-fail",
                    build_command=command_text,
                    build_time=build_time,
                    exec_time=0.0,
                    peak_mem_kib=0,
                    bin_size=binary.stat().st_size if binary.exists() else 0,
                    binary_path=binary,
                ),
                command_text + " // " + textwrap.shorten(stderr.replace("\n", " "), width=160, placeholder="..."),
            )
        output = normalize_output(run_proc.stdout)
        exec_times.append(exec_time)
        peak_kibs.append(peak_kib)

    return (
        Result(
            benchmark=spec.name,
            entry=entry.key,
            input_text=format_input(args),
            raw_output=output,
            output_text=compact_output(spec.name, output),
            reference_text="-",
            status="ok",
            build_command=command_text,
            build_time=build_time,
            exec_time=sum(exec_times) / len(exec_times),
            peak_mem_kib=max(peak_kibs),
            bin_size=binary.stat().st_size,
            binary_path=binary,
        ),
        command_text,
    )


def apply_references(results: list[Result], benchmarks: list[BenchmarkSpec]) -> None:
    exact_references: dict[str, str] = {}
    for spec in benchmarks:
        rows = [row for row in results if row.benchmark == spec.name and row.status == "ok"]
        if not rows:
            continue
        reference = rows[0].raw_output
        canonical_reference = canonical_output(spec, reference)
        exact_references[spec.name] = reference
        for row in rows:
            canonical = canonical_output(spec, row.raw_output)
            row.output_text = compact_output(spec.name, canonical)
            row.reference_text = compact_output(spec.name, canonical_reference)
            row.status = "ok" if canonical == canonical_reference else "mismatch"
        for row in results:
            if row.benchmark == spec.name and row.status != "ok":
                if spec.name in exact_references:
                    row.reference_text = compact_output(spec.name, canonical_reference)


def selected_items(values: list[str] | None, available: list[str]) -> set[str]:
    if not values:
        return set(available)
    chosen: set[str] = set()
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                chosen.add(item)
    unknown = sorted(chosen - set(available))
    if unknown:
        raise SystemExit(f"unknown selection: {', '.join(unknown)}")
    return chosen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--build-jobs", type=int, default=cpu_count())
    parser.add_argument("--report-path", default=str(DEFAULT_REPORT))
    parser.add_argument("--entry", action="append")
    parser.add_argument("--benchmark", action="append")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    active_entries = entries()
    if not active_entries:
        raise SystemExit("no supported toolchains found")

    chosen_entries = selected_items(args.entry, [entry.key for entry in active_entries])
    active_entries = [entry for entry in active_entries if entry.key in chosen_entries]
    chosen_benchmarks = selected_items(args.benchmark, [spec.name for spec in BENCHMARKS])
    active_benchmarks = [spec for spec in BENCHMARKS if spec.name in chosen_benchmarks]
    report_path = Path(args.report_path).resolve()

    clean_dirs()
    results: list[Result] = []
    for spec in active_benchmarks:
        for entry in active_entries:
            result, _ = build_and_run(spec, entry, args)
            results.append(result)

    apply_references(results, active_benchmarks)
    cleanup_source_tree()
    report_path.write_text(render_report(args, active_entries, active_benchmarks, results), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
