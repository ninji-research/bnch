#!/usr/bin/env python3

from __future__ import annotations

import argparse
import functools
import hashlib
import math
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
FIXTURES = ROOT / "fixtures"
BIN = ROOT / "bin"
BUILD = ROOT / ".build"
GO_CACHE = BUILD / "go-cache"
DEFAULT_REPORT = ROOT / "REPORT.md"
FIXED_ENV = {
    "LC_ALL": "C",
    "LANG": "C",
    "TZ": "UTC",
    "CGO_ENABLED": "0",
    "GOCACHE": str(GO_CACHE),
}

METRIC_WEIGHTS = {
    "exec_time": 0.60,
    "peak_mem": 0.20,
    "build_time": 0.10,
    "bin_size": 0.10,
}

SUMMARY_METRICS: tuple[tuple[str, str], ...] = (
    ("Speed", "exec_time"),
    ("Memory", "peak_mem"),
    ("Build", "build_time"),
    ("Size", "bin_size"),
)

TOOL_VERSION_COMMANDS: tuple[tuple[str, list[str]], ...] = (
    ("gcc", ["gcc", "--version"]),
    ("clang", ["clang", "--version"]),
    ("go", ["go", "version"]),
    ("rustc", ["rustc", "--version"]),
    ("nim", ["nim", "--version"]),
    ("ocamlopt", ["ocamlopt", "-version"]),
    ("moon", ["moon", "version"]),
    ("strip", ["strip", "--version"]),
)

SOURCE_SUFFIXES = {
    "c": ".c",
    "go": ".go",
    "rust": ".rs",
    "nim": ".nim",
    "ocaml": ".ml",
}

DIGEST_OUTPUT_BENCHMARKS = {"mandelbrot", "fasta", "revcomp"}
ENTRY_TABLE_HEADERS = ["Entry", "Compiler", "Backend", "Linkage", "Stripped", "Binary Size Sample (KiB)"]
RESULT_TABLE_HEADERS = ["Benchmark", "Entry", "Input", "Output", "Build Time (s)", "Run Time (s)", "Peak Memory (MiB)", "Binary Size (KiB)", "Status"]
MISMATCH_TABLE_HEADERS = ["Benchmark", "Entry", "Output", "Reference", "Status"]


@dataclass(frozen=True)
class BenchmarkSpec:
    name: str
    args: tuple[str, ...]
    stdin_fixture: str | None
    input_label: str
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


ENTRY_CANDIDATES: tuple[tuple[tuple[str, ...], EntrySpec], ...] = (
    (("gcc",), EntrySpec("c__gcc", "c (gcc)", "c", "gcc", "native")),
    (("clang",), EntrySpec("c__clang", "c (clang)", "c", "clang", "native")),
    (("go",), EntrySpec("go__gc", "go (gc)", "go", "go", "native")),
    (("rustc",), EntrySpec("rust__llvm", "rust (rustc/llvm)", "rust", "rustc", "llvm")),
    (("nim", "gcc"), EntrySpec("nim__gcc", "nim (gcc)", "nim", "gcc", "c")),
    (("nim", "clang"), EntrySpec("nim__clang", "nim (clang)", "nim", "clang", "c")),
    (("ocamlopt",), EntrySpec("ocaml__native", "ocaml (native)", "ocaml", "ocamlopt", "native")),
    (("moon",), EntrySpec("moonbit__native", "moonbit (native)", "moonbit", "moon", "native")),
)


@dataclass
class Result:
    benchmark: str
    entry: str
    input_text: str
    raw_output: str
    output_text: str
    reference_text: str
    status: str
    build_time: float
    exec_time: float
    peak_mem_kib: int
    bin_size: int
    binary_path: Path


@dataclass(frozen=True)
class SummaryData:
    overall_scores: dict[str, float]
    overall_order: list[str]
    overall_ranks: dict[str, int]
    metric_ranks: dict[str, dict[str, int]]


@dataclass(frozen=True)
class Selection:
    entries: list[EntrySpec]
    benchmarks: list[BenchmarkSpec]


@dataclass(frozen=True)
class BuiltArtifact:
    binary: Path
    build_time: float


def failed_result(
    spec: BenchmarkSpec,
    entry: EntrySpec,
    input_text: str,
    status: str,
    build_time: float,
    binary: Path,
) -> Result:
    return Result(
        benchmark=spec.name,
        entry=entry.key,
        input_text=input_text,
        raw_output="",
        output_text="-",
        reference_text="-",
        status=status,
        build_time=build_time,
        exec_time=0.0,
        peak_mem_kib=0,
        bin_size=binary.stat().st_size if binary.exists() else 0,
        binary_path=binary,
    )


BENCHMARKS: tuple[BenchmarkSpec, ...] = (
    BenchmarkSpec("binarytrees", ("20",), None, "20", 1.00, "exact", "bottom-up binary tree construction and checksum", "O(nodes built)", "O(max tree size)", "exact multiline text", "Same tree/check workload; memory-management costs remain language-native."),
    BenchmarkSpec("fasta", ("250000",), None, "250000", 0.75, "exact", "deterministic FASTA generation with buffered text emission", "O(n)", "O(1)", "exact FASTA text", "Adds text generation and formatting without turning the suite into a library benchmark."),
    BenchmarkSpec("mandelbrot", ("512",), None, "512", 1.00, "exact", "scalar Mandelbrot escape-time bitmap checksum", "O(size^2 * iter)", "O(1)", "exact integer checksum", "Input size is set to 512 because all retained implementations agree there exactly."),
    BenchmarkSpec("spectralnorm", ("5000",), None, "5000", 1.00, "float_9", "power method on implicit matrix", "O(n^2 * iterations)", "O(n)", "one float rounded to 9 decimals", "Correctness compares canonical 9-decimal output, not raw printer differences."),
    BenchmarkSpec("fannkuch", ("10",), None, "10", 1.00, "exact", "fannkuch-redux permutation flips", "O(n! * n)", "O(n)", "exact two-line text", "Same permutation-generation strategy across entries."),
    BenchmarkSpec("nbody", ("5000000",), None, "5000000", 1.00, "float_9_lines", "5-body symplectic advance and energy", "O(iterations * bodies^2)", "O(1)", "two floats rounded to 9 decimals", "Correctness compares canonical 9-decimal energies line-by-line."),
    BenchmarkSpec("knucleotide", (), "knucleotide/knucleotide-250000.fasta", "fixture:knucleotide-250000.fasta", 1.00, "exact", "FASTA parsing plus k-mer frequency and occurrence counting", "O(n)", "O(unique k-mers + input)", "exact multiline text", "Uses one committed deterministic FASTA fixture and processes only the >THREE section."),
    BenchmarkSpec("revcomp", (), "knucleotide/knucleotide-250000.fasta", "fixture:knucleotide-250000.fasta", 0.75, "fasta_casefold", "FASTA parsing plus reverse-complement text transformation", "O(n)", "O(n)", "FASTA text with case-insensitive bases", "Adds streaming-style text transformation and output reshaping with the same committed fixture family."),
)


def sh(command: list[str], cwd: Path | None = None, capture: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(FIXED_ENV)
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=capture,
        text=True,
        check=False,
    )


def timed(command: list[str], cwd: Path | None = None, stdin_text: str | None = None) -> tuple[subprocess.CompletedProcess[str], float, int]:
    env = os.environ.copy()
    env.update(FIXED_ENV)
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8") as stdout_file, tempfile.NamedTemporaryFile(
        "w+", encoding="utf-8"
    ) as stderr_file, tempfile.NamedTemporaryFile("w+", encoding="utf-8") as stdin_file:
        if stdin_text is not None:
            stdin_file.write(stdin_text)
            stdin_file.flush()
            stdin_file.seek(0)
        start = time.perf_counter()
        proc = subprocess.Popen(
            command,
            cwd=str(cwd) if cwd else None,
            env=env,
            stdin=stdin_file if stdin_text is not None else None,
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


@functools.cache
def tool(name: str) -> str | None:
    return shutil.which(name)


def version_line(command: list[str]) -> str:
    proc = sh(command)
    text = (proc.stdout or proc.stderr).strip().splitlines()
    return text[0].strip() if text else ""


def version_or_dash(command: list[str]) -> str:
    return version_line(command) if tool(command[0]) else "-"


def cpu_count() -> int:
    return os.cpu_count() or 1


def entries() -> list[EntrySpec]:
    return [entry for required_tools, entry in ENTRY_CANDIDATES if all(tool(name) for name in required_tools)]


def source_path(benchmark: str, entry: EntrySpec) -> Path:
    root = SRC / benchmark
    if entry.language in SOURCE_SUFFIXES:
        return root / f"{benchmark}{SOURCE_SUFFIXES[entry.language]}"
    if entry.language == "moonbit":
        return root / f"moonbit_{benchmark}"
    raise ValueError(f"unsupported language: {entry.language}")


def benchmark_args(spec: BenchmarkSpec) -> tuple[str, ...]:
    return spec.args


def benchmark_input_text(spec: BenchmarkSpec) -> str | None:
    if spec.stdin_fixture is None:
        return None
    return fixture_text(spec.stdin_fixture)


@functools.cache
def fixture_text(relative_path: str) -> str:
    return (FIXTURES / relative_path).read_text(encoding="utf-8")


def benchmark_input_label(spec: BenchmarkSpec) -> str:
    return spec.input_label


def entry_labels(active_entries: list[EntrySpec]) -> dict[str, str]:
    return {entry.key: entry.label for entry in active_entries}


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
    if entry.language == "go":
        return [
            "go",
            "build",
            "-p",
            str(build_jobs),
            "-trimpath",
            "-buildvcs=false",
            "-ldflags=-s -w -buildid=",
            "-o",
            str(binary),
            str(source),
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
    GO_CACHE.mkdir(parents=True, exist_ok=True)


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
    shutil.rmtree(ROOT / "__pycache__", ignore_errors=True)


def normalize_output(text: str) -> str:
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines).strip()


def compact_output(benchmark: str, text: str) -> str:
    if not text:
        return "-"
    if benchmark in DIGEST_OUTPUT_BENCHMARKS or len(text) > 512:
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
    if spec.check == "fasta_casefold":
        lines = []
        for line in normalized.splitlines():
            lines.append(line if line.startswith(">") else line.upper())
        return "\n".join(lines)
    if spec.check == "float_9":
        return format_fixed(parse_first_float(normalized), 9)
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


def metric_scores(
    results: list[Result],
    benchmarks: list[BenchmarkSpec],
    metrics: dict[str, float] | Iterable[str],
) -> dict[str, float]:
    metric_weights = metrics if isinstance(metrics, dict) else {metric: 1.0 for metric in metrics}
    metric_names = tuple(metric_weights)
    if not metric_names:
        return {}
    by_benchmark: dict[str, list[Result]] = {}
    for result in results:
        if result.status == "ok":
            by_benchmark.setdefault(result.benchmark, []).append(result)

    complete_entries = complete_entry_keys(results, benchmarks)
    if not complete_entries:
        return {}

    totals = {entry: 0.0 for entry in complete_entries}
    total_weight = 0.0
    for spec in benchmarks:
        rows = [row for row in by_benchmark.get(spec.name, []) if row.entry in complete_entries]
        if not rows:
            continue
        for metric in metric_names:
            best = min(metric_value(row, metric) for row in rows)
            if best <= 0:
                continue
            weight = spec.weight * metric_weights[metric]
            total_weight += weight
            for row in rows:
                totals[row.entry] += weight * (best / metric_value(row, metric))
    if total_weight == 0:
        return {}
    return {entry: totals[entry] / total_weight for entry in complete_entries}


def complete_entry_keys(results: list[Result], benchmarks: list[BenchmarkSpec]) -> set[str]:
    if not benchmarks:
        return set()
    benchmark_names = {spec.name for spec in benchmarks}
    completed: dict[str, set[str]] = {}
    for result in results:
        if result.status != "ok" or result.benchmark not in benchmark_names:
            continue
        completed.setdefault(result.entry, set()).add(result.benchmark)
    return {entry for entry, names in completed.items() if len(names) == len(benchmark_names)}


def environment_rows(run_args: argparse.Namespace, active_entries: list[EntrySpec], benchmarks: list[BenchmarkSpec]) -> list[list[str]]:
    rows = [
        ["runs", str(run_args.runs)],
        ["warmup", str(run_args.warmup)],
        ["build_jobs", str(run_args.build_jobs)],
        ["link_policy", "toolchain-default release mode (mixed linkage; see entry metadata)"],
        ["entries", str(len(active_entries))],
        ["benchmarks", str(len(benchmarks))],
    ]
    rows.extend([[name, version_or_dash(command)] for name, command in TOOL_VERSION_COMMANDS])
    return rows


def entry_rows(active_entries: list[EntrySpec], results: list[Result]) -> list[list[str]]:
    sample_for_entry: dict[str, Result] = {}
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


def fmt_normalized_score(value: float) -> str:
    return f"{value:.4f}"


def rank_positions(values: dict[str, float], reverse: bool = False, rel_tol: float = 1e-12, abs_tol: float = 1e-12) -> dict[str, int]:
    ordered = sorted(values.items(), key=lambda item: item[1], reverse=reverse)
    ranks: dict[str, int] = {}
    last_value: float | None = None
    last_rank = 0
    for index, (entry, value) in enumerate(ordered, start=1):
        if last_value is not None and math.isclose(value, last_value, rel_tol=rel_tol, abs_tol=abs_tol):
            ranks[entry] = last_rank
            continue
        ranks[entry] = index
        last_rank = index
        last_value = value
    return ranks


def build_summary_data(results: list[Result], benchmarks: list[BenchmarkSpec]) -> SummaryData:
    valid_benchmarks = scored_benchmarks(results, benchmarks)
    overall_scores = metric_scores(results, valid_benchmarks, METRIC_WEIGHTS)
    metric_score_maps = {label: metric_scores(results, valid_benchmarks, {metric: 1.0}) for label, metric in SUMMARY_METRICS}
    overall_order = [entry for entry, _ in sorted(overall_scores.items(), key=lambda item: item[1], reverse=True)]
    return SummaryData(
        overall_scores=overall_scores,
        overall_order=overall_order,
        overall_ranks=rank_positions(overall_scores, reverse=True),
        metric_ranks={label: rank_positions(scores, reverse=True) for label, scores in metric_score_maps.items()},
    )


def summary_headers() -> list[str]:
    return ["Overall", "Entry", "Score", *[label for label, _ in SUMMARY_METRICS]]


def summary_rows(summary: SummaryData, active_entries: list[EntrySpec]) -> list[list[str]]:
    labels = entry_labels(active_entries)

    rows: list[list[str]] = []
    for entry_key in summary.overall_order:
        metric_cells: list[str] = []
        for label, _ in SUMMARY_METRICS:
            rank = summary.metric_ranks[label].get(entry_key)
            if rank is None:
                metric_cells.append("-")
                continue
            metric_cells.append(str(rank))
        rows.append(
            [
                str(summary.overall_ranks[entry_key]),
                labels[entry_key],
                fmt_normalized_score(summary.overall_scores[entry_key]),
                *metric_cells,
            ]
        )
    return rows


def result_rows(results: list[Result], active_entries: list[EntrySpec]) -> list[list[str]]:
    order = {entry.key: index for index, entry in enumerate(active_entries)}
    labels = entry_labels(active_entries)
    rows: list[list[str]] = []
    for result in sorted(results, key=lambda item: (item.benchmark, order.get(item.entry, 999), item.entry)):
        rows.append(
            [
                result.benchmark,
                labels.get(result.entry, result.entry),
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
    labels = entry_labels(active_entries)
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
    content_sections = [
        "## Environment",
        "",
        markdown_table(["Setting", "Value"], environment_rows(run_args, active_entries, benchmarks)),
        "",
        "## Entries",
        "",
        markdown_table(
            ENTRY_TABLE_HEADERS,
            entry_rows(active_entries, results),
        ),
        "",
        "## Scoring Inputs",
        "",
        markdown_table(["Weight", "Value"], weight_rows(benchmarks)),
        "",
        markdown_table(
            ["Benchmark", "Algorithm", "Time", "Space", "Output Contract", "Fairness Notes"],
            benchmark_rows(benchmarks),
        ),
        "",
    ]
    content = [
        "# Benchmark Report",
        "",
        *content_sections,
    ]

    excluded = excluded_benchmark_rows(results, benchmarks, active_entries)
    if excluded:
        content.extend(
            [
                markdown_table(["Excluded From Score", "Reason"], excluded),
                "",
            ]
        )

    summary = build_summary_data(results, benchmarks)
    if summary.overall_scores:
        content.extend(
            [
                "## Summary",
                "",
                markdown_table(summary_headers(), summary_rows(summary, active_entries)),
                "",
                "_Overall score uses normalized per-benchmark scoring with the configured metric weights. Per-metric columns show rank only, using that metric's normalized score across the scored benchmarks._",
                "",
            ]
        )

    content.append(
        "## Results"
    )
    content.append("")
    content.append(
        markdown_table(RESULT_TABLE_HEADERS, result_rows(results, active_entries))
    )
    mismatches = mismatch_rows(results, active_entries)
    if mismatches:
        content.extend(
            [
                "",
                "## Mismatches",
                "",
                markdown_table(MISMATCH_TABLE_HEADERS, mismatches),
            ]
        )
    content.append("")
    return "\n".join(content)


def finalize_binary(entry: EntrySpec, binary: Path, build_dir: Path, build_time: float) -> BuiltArtifact:
    if entry.language == "moonbit":
        built = find_moonbit_binary(build_dir)
        shutil.copy2(built, binary)
        binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    build_time += strip_binary(binary)
    return BuiltArtifact(binary=binary, build_time=build_time)


def run_binary(binary: Path, args: tuple[str, ...], stdin_text: str | None, repeats: int) -> tuple[list[float], list[int], str] | None:
    exec_times: list[float] = []
    peak_kibs: list[int] = []
    output = "-"
    for _ in range(repeats):
        run_proc, exec_time, peak_kib = timed([str(binary), *args], stdin_text=stdin_text)
        if run_proc.returncode != 0:
            return None
        output = normalize_output(run_proc.stdout)
        exec_times.append(exec_time)
        peak_kibs.append(peak_kib)
    return exec_times, peak_kibs, output


def build_and_run(spec: BenchmarkSpec, entry: EntrySpec, run_args: argparse.Namespace) -> Result:
    binary = BIN / f"{spec.name}__{entry.key}"
    build_dir = BUILD / f"{spec.name}__{entry.key}"
    build_dir.mkdir(parents=True, exist_ok=True)
    binary.parent.mkdir(parents=True, exist_ok=True)

    source = source_path(spec.name, entry)
    command = build_command(spec, entry, binary, build_dir, run_args.build_jobs)
    build_cwd = source if entry.language == "moonbit" else None

    stdin_text = benchmark_input_text(spec)
    build_proc, build_time, _ = timed(command, cwd=build_cwd)
    if build_proc.returncode != 0:
        return failed_result(spec, entry, benchmark_input_label(spec), "build-fail", build_time, binary)

    artifact = finalize_binary(entry, binary, build_dir, build_time)

    args = benchmark_args(spec)
    if run_args.warmup:
        warmup = run_binary(artifact.binary, args, stdin_text, run_args.warmup)
        if warmup is None:
            return failed_result(spec, entry, benchmark_input_label(spec), "run-fail", artifact.build_time, artifact.binary)

    measured = run_binary(artifact.binary, args, stdin_text, run_args.runs)
    if measured is None:
        return failed_result(spec, entry, benchmark_input_label(spec), "run-fail", artifact.build_time, artifact.binary)
    exec_times, peak_kibs, output = measured

    return Result(
        benchmark=spec.name,
        entry=entry.key,
        input_text=benchmark_input_label(spec),
        raw_output=output,
        output_text=compact_output(spec.name, output),
        reference_text="-",
        status="ok",
        build_time=artifact.build_time,
        exec_time=sum(exec_times) / len(exec_times),
        peak_mem_kib=max(peak_kibs),
        bin_size=artifact.binary.stat().st_size,
        binary_path=artifact.binary,
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


def parse_csv_args(values: list[str] | None) -> list[str]:
    if not values:
        return []
    chosen: list[str] = []
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                chosen.append(item)
    return chosen


def selected_keys(values: list[str] | None, available: list[str], kind: str) -> list[str]:
    if not values:
        return list(available)
    requested = parse_csv_args(values)
    unknown = sorted(set(requested) - set(available))
    if unknown:
        raise SystemExit(f"unknown {kind}: {', '.join(unknown)}")
    ordered: list[str] = []
    seen: set[str] = set()
    for item in requested:
        if item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered


def resolve_selection(run_args: argparse.Namespace, available_entries: list[EntrySpec]) -> Selection:
    available_entry_keys = [entry.key for entry in available_entries]
    selected_entry_keys = set(selected_keys(run_args.entry, available_entry_keys, "entry"))
    chosen_entries = [entry for entry in available_entries if entry.key in selected_entry_keys]
    if not chosen_entries:
        raise SystemExit("no active entries selected")

    available_benchmark_keys = [spec.name for spec in BENCHMARKS]
    selected_benchmark_keys = set(selected_keys(run_args.benchmark, available_benchmark_keys, "benchmark"))
    chosen_benchmarks = [spec for spec in BENCHMARKS if spec.name in selected_benchmark_keys]
    if not chosen_benchmarks:
        raise SystemExit("no benchmarks selected")

    return Selection(entries=chosen_entries, benchmarks=chosen_benchmarks)


def log_progress(index: int, total: int, spec: BenchmarkSpec, entry: EntrySpec) -> None:
    print(f"[{index}/{total}] {spec.name} :: {entry.label}", file=sys.stderr, flush=True)


def run_suite(run_args: argparse.Namespace, active_entries: list[EntrySpec], active_benchmarks: list[BenchmarkSpec]) -> list[Result]:
    total = len(active_entries) * len(active_benchmarks)
    results: list[Result] = []
    current = 0
    for spec in active_benchmarks:
        for entry in active_entries:
            current += 1
            log_progress(current, total, spec, entry)
            results.append(build_and_run(spec, entry, run_args))
    return results


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be a non-negative integer")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build retained benchmark implementations and write a markdown report.")
    parser.add_argument("--runs", type=positive_int, default=3, help="Measured runs per benchmark after warmup.")
    parser.add_argument("--warmup", type=non_negative_int, default=1, help="Warmup runs before timing.")
    parser.add_argument("--build-jobs", type=positive_int, default=cpu_count(), help="Parallel jobs used by supported build tools.")
    parser.add_argument("--report-path", default=str(DEFAULT_REPORT), help="Output path for the generated markdown report.")
    parser.add_argument("--entry", action="append", help="Entry key or comma-separated entry keys to include.")
    parser.add_argument("--benchmark", action="append", help="Benchmark name or comma-separated benchmark names to include.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    available_entries = entries()
    if not available_entries:
        raise SystemExit("no supported toolchains found")

    selection = resolve_selection(args, available_entries)
    active_entries = selection.entries
    active_benchmarks = selection.benchmarks
    report_path = Path(args.report_path).resolve()

    clean_dirs()
    results = run_suite(args, active_entries, active_benchmarks)
    apply_references(results, active_benchmarks)
    cleanup_source_tree()
    report_path.write_text(render_report(args, active_entries, active_benchmarks, results), encoding="utf-8")
    print(f"wrote {report_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
