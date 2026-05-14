#!/usr/bin/env python3

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import math
import os
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
FIXTURES = ROOT / "fixtures"
RUN_ROOT = Path(os.environ.get("BNCH_RUN_ROOT", ROOT / ".runs" / f"{os.getpid()}-{time.time_ns():x}"))
BIN = RUN_ROOT / "bin"
BUILD = RUN_ROOT / ".build"
GO_CACHE = BUILD / "go-cache"
DEFAULT_REPORT = ROOT / "REPORT.md"
DEFAULT_JSON_REPORT = ROOT / "REPORT.json"
DEFAULT_VARIANT_REPORT = ROOT / "REPORT.variants.md"
DEFAULT_VARIANT_JSON_REPORT = ROOT / "REPORT.variants.json"
DEFAULT_EXPERIMENTAL_REPORT = ROOT / "REPORT.experimental.md"
DEFAULT_EXPERIMENTAL_JSON_REPORT = ROOT / "REPORT.experimental.json"
DEFAULT_EXPERIMENTAL_VARIANT_REPORT = ROOT / "REPORT.experimental.variants.md"
DEFAULT_EXPERIMENTAL_VARIANT_JSON_REPORT = ROOT / "REPORT.experimental.variants.json"
FIXED_ENV = {
    "LC_ALL": "C",
    "LANG": "C",
    "TZ": "UTC",
    "CGO_ENABLED": "0",
    "GOCACHE": str(GO_CACHE),
}

PROJECT_OBJECTIVE = (
    "Build the strongest fixed-host benchmark harness for canonical, production-ready native-language "
    "implementations, with correctness enforced before any ranking."
)

METRIC_WEIGHTS = {
    "exec_time": 0.65,
    "peak_mem": 0.20,
    "build_time": 0.10,
    "bin_size": 0.05,
}

PROFILE_WEIGHTS: tuple[tuple[str, dict[str, float], str], ...] = (
    ("Balanced", METRIC_WEIGHTS, "Default composite across speed, memory, build time, and binary size."),
    ("Speed First", {"exec_time": 0.85, "peak_mem": 0.10, "build_time": 0.03, "bin_size": 0.02}, "Throughput or latency matters most."),
    ("Memory First", {"exec_time": 0.20, "peak_mem": 0.70, "build_time": 0.05, "bin_size": 0.05}, "RAM pressure matters most."),
    ("Build First", {"exec_time": 0.15, "peak_mem": 0.05, "build_time": 0.75, "bin_size": 0.05}, "Build and iteration cost matter most."),
    ("Deploy First", {"exec_time": 0.35, "peak_mem": 0.15, "build_time": 0.15, "bin_size": 0.35}, "Artifact footprint matters alongside runtime."),
)

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
    "sarif": ".sarif",
}
ENTRY_TRACKS = {"main", "experimental"}

DIGEST_OUTPUT_BENCHMARKS = {"mandelbrot", "fasta", "revcomp"}
ENTRY_TABLE_HEADERS = ["Entry", "Compiler", "Backend", "Linkage", "Stripped", "Binary Size Sample (KiB)"]
ENTRY_POLICY_HEADERS = ["Entry", "Build Profile", "Low-Burden Optimizations"]
RESULT_TABLE_HEADERS = ["Benchmark", "Entry", "Input", "Output", "Build Time (s)", "Run Time (s)", "Peak Memory (MiB)", "Binary Size (KiB)", "Status"]
MISMATCH_TABLE_HEADERS = ["Benchmark", "Entry", "Output", "Reference", "Status"]
BENCHMARK_COVERAGE_HEADERS = ["Benchmark", "Category", "Base Wt", "Effective Wt", "Capabilities", "Unique Coverage", "Retained For"]
BENCHMARK_TABLE_HEADERS = ["Benchmark", "Algorithm", "Time", "Space", "Output Contract", "Fairness Notes"]
SOURCE_TABLE_HEADERS = ["Entry", "Benchmarks", "Source Lines", "Source Chars", "Norm Lines", "Norm Chars"]
CATEGORY_LABELS = {
    "numeric_compute": "Numeric",
    "allocation_runtime": "Allocation",
    "hash_map_string": "Hash/String",
    "text_streaming": "Text/Streaming",
    "parse_aggregate": "Parse/Aggregate",
    "join_aggregate": "Join/Aggregate",
    "sort_aggregate": "Sort/Aggregate",
}
OUTPUT_KIND_BY_CHECK = {
    "exact": "exact_text",
    "fasta_casefold": "fasta_casefold",
    "float_9": "float_9dp",
    "float_9_lines": "float_lines_9dp",
}
BENCHMARK_SPEC_DIR = ROOT / "benchmarks"
ENTRY_SPEC_DIR = ROOT / "entries"


@dataclass(frozen=True)
class BenchmarkSpec:
    name: str
    category: str
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
    capabilities: tuple[str, ...]
    retained_for: str


@dataclass(frozen=True)
class EntrySpec:
    key: str
    label: str
    language: str
    compiler: str
    backend: str
    track: str
    canonical: bool
    supported_benchmarks: tuple[str, ...] | None
    required_tools: tuple[str, ...]
    build_profile: str
    optimization_notes: tuple[str, ...]


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
    exec_time_spread: float
    measured_runs: int
    peak_mem_kib: int
    bin_size: int
    binary_path: Path


@dataclass(frozen=True)
class SummaryData:
    overall_scores: dict[str, float]
    overall_order: list[str]
    overall_ranks: dict[str, int]
    metric_scores: dict[str, dict[str, float]]
    metric_orders: dict[str, list[str]]
    metric_ranks: dict[str, dict[str, int]]


@dataclass(frozen=True)
class ProfileSummary:
    label: str
    description: str
    summary: SummaryData


@dataclass(frozen=True)
class CategorySummary:
    labels: list[str]
    scores: dict[str, dict[str, float]]


@dataclass(frozen=True)
class Selection:
    entries: list[EntrySpec]
    benchmarks: list[BenchmarkSpec]


@dataclass(frozen=True)
class BuiltArtifact:
    binary: Path
    build_time: float


@dataclass(frozen=True)
class SourceMetrics:
    benchmarks: int
    lines: int
    chars: int


@dataclass(frozen=True)
class MemoryMeasurement:
    mode: str
    detail: str


@dataclass(frozen=True)
class RunBinaryResult:
    exec_times: list[float]
    peak_kibs: list[int]
    output: str
    status: str


@dataclass(frozen=True)
class ManifestLoadResult:
    documents: dict[str, dict[str, object]]
    errors: list[str]


def load_json_object(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON ({exc.msg} at line {exc.lineno} column {exc.colno})") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected top-level object, got {type(data).__name__}")
    return data


def load_manifest_dir(directory: Path, filename: str) -> ManifestLoadResult:
    documents: dict[str, dict[str, object]] = {}
    errors: list[str] = []
    for path in sorted(directory.glob(f"*/{filename}")):
        key = path.parent.name
        try:
            documents[key] = load_json_object(path)
        except ValueError as exc:
            errors.append(str(exc))
    return ManifestLoadResult(documents=documents, errors=errors)


@functools.cache
def benchmark_manifest_data() -> ManifestLoadResult:
    return load_manifest_dir(BENCHMARK_SPEC_DIR, "spec.json")


@functools.cache
def entry_manifest_data() -> ManifestLoadResult:
    return load_manifest_dir(ENTRY_SPEC_DIR, "entry.json")


def manifest_error(path: str, message: str) -> ValueError:
    return ValueError(f"{path}: {message}")


def manifest_string(path: str, value: object) -> str:
    if not isinstance(value, str):
        raise manifest_error(path, f"expected str, got {type(value).__name__}")
    return value


def manifest_non_empty_string(path: str, value: object) -> str:
    parsed = manifest_string(path, value).strip()
    if not parsed:
        raise manifest_error(path, "must be a non-empty string")
    return parsed


def manifest_number(path: str, value: object) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise manifest_error(path, f"expected number, got {type(value).__name__}")
    return float(value)


def manifest_integer(path: str, value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise manifest_error(path, f"expected int, got {type(value).__name__}")
    return value


def manifest_dict(path: str, value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise manifest_error(path, f"expected object, got {type(value).__name__}")
    return value


def manifest_list(path: str, value: object) -> list[object]:
    if not isinstance(value, list):
        raise manifest_error(path, f"expected list, got {type(value).__name__}")
    return value


def manifest_string_list(path: str, value: object) -> tuple[str, ...]:
    values = manifest_list(path, value)
    parsed: list[str] = []
    for index, item in enumerate(values):
        parsed.append(manifest_non_empty_string(f"{path}[{index}]", item))
    return tuple(parsed)


def ensure_unique(items: Iterable[str], path: str, what: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    if duplicates:
        repeated = ", ".join(sorted(duplicates))
        raise manifest_error(path, f"duplicate {what}: {repeated}")


def parse_benchmark_spec(name: str, manifest: dict[str, object]) -> tuple[int, BenchmarkSpec]:
    base = f"benchmarks/{name}/spec.json"
    manifest_id = manifest_non_empty_string(f"{base}.id", manifest.get("id"))
    if manifest_id != name:
        raise manifest_error(f"{base}.id", f"expected {name!r}, got {manifest_id!r}")
    category = manifest_non_empty_string(f"{base}.category", manifest.get("category"))
    if category not in CATEGORY_LABELS:
        raise manifest_error(f"{base}.category", f"unknown category {category!r}")
    order = manifest_integer(f"{base}.order", manifest.get("order"))
    if order <= 0:
        raise manifest_error(f"{base}.order", "must be a positive integer")
    weight = manifest_number(f"{base}.weight", manifest.get("weight"))
    if not math.isfinite(weight) or weight <= 0:
        raise manifest_error(f"{base}.weight", "must be a finite positive number")
    check = manifest_non_empty_string(f"{base}.check", manifest.get("check"))
    if check not in OUTPUT_KIND_BY_CHECK:
        raise manifest_error(f"{base}.check", f"unknown check {check!r}")

    input_spec = manifest_dict(f"{base}.input", manifest.get("input"))
    input_kind = manifest_string(f"{base}.input.kind", input_spec.get("kind"))
    args: tuple[str, ...]
    stdin_fixture: str | None
    input_label: str
    if input_kind == "args":
        raw_value = manifest_non_empty_string(f"{base}.input.value", input_spec.get("value"))
        args = tuple(shlex.split(raw_value))
        stdin_fixture = None
        input_label = raw_value
    elif input_kind == "fixture":
        fixture_path = manifest_non_empty_string(f"{base}.input.path", input_spec.get("path"))
        prefix = "fixtures/"
        if not fixture_path.startswith(prefix):
            raise manifest_error(f"{base}.input.path", "fixture paths must start with 'fixtures/'")
        stdin_fixture = fixture_path[len(prefix) :]
        if not (FIXTURES / stdin_fixture).exists():
            raise manifest_error(f"{base}.input.path", f"missing fixture {fixture_path}")
        args = ()
        input_label = f"fixture:{Path(stdin_fixture).name}"
    else:
        raise manifest_error(f"{base}.input.kind", "expected 'args' or 'fixture'")

    capabilities = manifest_string_list(f"{base}.capabilities", manifest.get("capabilities"))
    if not capabilities:
        raise manifest_error(f"{base}.capabilities", "must not be empty")
    ensure_unique(capabilities, f"{base}.capabilities", "capabilities")

    return order, BenchmarkSpec(
        name=name,
        category=category,
        args=args,
        stdin_fixture=stdin_fixture,
        input_label=input_label,
        weight=weight,
        check=check,
        algorithm=manifest_non_empty_string(f"{base}.algorithm", manifest.get("algorithm")),
        time_complexity=manifest_non_empty_string(f"{base}.time_complexity", manifest.get("time_complexity")),
        space_complexity=manifest_non_empty_string(f"{base}.space_complexity", manifest.get("space_complexity")),
        output_contract=manifest_non_empty_string(f"{base}.output_contract", manifest.get("output_contract")),
        fairness_notes=manifest_non_empty_string(f"{base}.fairness_notes", manifest.get("fairness_notes")),
        capabilities=capabilities,
        retained_for=manifest_non_empty_string(f"{base}.retained_for", manifest.get("retained_for")),
    )


@functools.cache
def benchmark_specs() -> tuple[BenchmarkSpec, ...]:
    manifest_data = benchmark_manifest_data()
    parsed: list[tuple[int, BenchmarkSpec]] = []
    errors = list(manifest_data.errors)
    for name, manifest in manifest_data.documents.items():
        try:
            parsed.append(parse_benchmark_spec(name, manifest))
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        raise ValueError("\n".join(errors))
    ensure_unique((str(order) for order, _ in parsed), "benchmarks", "orders")
    return tuple(spec for _, spec in sorted(parsed, key=lambda item: (item[0], item[1].name)))


def parse_entry_variant(
    language: str,
    manifest: dict[str, object],
    variant: object,
    index: int,
    canonical_key: str,
    track: str,
    supported_benchmarks: tuple[str, ...] | None,
    build_profile: str,
    optimization_notes: tuple[str, ...],
) -> EntrySpec:
    base = f"entries/{language}/entry.json.variants[{index}]"
    data = manifest_dict(base, variant)
    key = manifest_non_empty_string(f"{base}.key", data.get("key"))
    required_tools = manifest_string_list(f"{base}.required_tools", data.get("required_tools"))
    if not required_tools:
        raise manifest_error(f"{base}.required_tools", "must not be empty")
    ensure_unique(required_tools, f"{base}.required_tools", "tools")
    return EntrySpec(
        key=key,
        label=manifest_non_empty_string(f"{base}.label", data.get("label")),
        language=language,
        compiler=manifest_non_empty_string(f"{base}.compiler", data.get("compiler")),
        backend=manifest_non_empty_string(f"{base}.backend", data.get("backend")),
        track=track,
        canonical=key == canonical_key,
        supported_benchmarks=supported_benchmarks,
        required_tools=required_tools,
        build_profile=build_profile,
        optimization_notes=optimization_notes,
    )


@functools.cache
def entry_specs() -> tuple[EntrySpec, ...]:
    manifest_data = entry_manifest_data()
    parsed: list[EntrySpec] = []
    errors = list(manifest_data.errors)
    for language, manifest in manifest_data.documents.items():
        base = f"entries/{language}/entry.json"
        try:
            manifest_language = manifest_non_empty_string(f"{base}.language", manifest.get("language"))
            if manifest_language != language:
                raise manifest_error(f"{base}.language", f"expected {language!r}, got {manifest_language!r}")
            track = manifest.get("track", "main")
            if track not in ENTRY_TRACKS:
                raise manifest_error(f"{base}.track", f"expected one of {sorted(ENTRY_TRACKS)!r}, got {track!r}")
            supported_benchmarks_raw = manifest.get("benchmarks")
            if supported_benchmarks_raw is None:
                supported_benchmarks = None
            else:
                supported_benchmarks_list = manifest_string_list(f"{base}.benchmarks", supported_benchmarks_raw)
                if not supported_benchmarks_list:
                    raise manifest_error(f"{base}.benchmarks", "must be a non-empty list when present")
                ensure_unique(supported_benchmarks_list, f"{base}.benchmarks", "benchmarks")
                supported_benchmarks = tuple(supported_benchmarks_list)
            canonical_key = manifest_non_empty_string(f"{base}.canonical_entry", manifest.get("canonical_entry"))
            build = manifest_dict(f"{base}.build", manifest.get("build"))
            build_profile = manifest_non_empty_string(f"{base}.build.profile_label", build.get("profile_label"))
            optimization_notes = manifest_string_list(f"{base}.build.low_burden_optimizations", build.get("low_burden_optimizations"))
            if not optimization_notes:
                raise manifest_error(f"{base}.build.low_burden_optimizations", "must not be empty")
            ensure_unique(optimization_notes, f"{base}.build.low_burden_optimizations", "optimizations")
            variants = manifest_list(f"{base}.variants", manifest.get("variants"))
            if not variants:
                raise manifest_error(f"{base}.variants", "must not be empty")
            language_entries = [
                parse_entry_variant(
                    language,
                    manifest,
                    variant,
                    index,
                    canonical_key,
                    track,
                    supported_benchmarks,
                    build_profile,
                    optimization_notes,
                )
                for index, variant in enumerate(variants)
            ]
            ensure_unique((entry.key for entry in language_entries), f"{base}.variants", "variant keys")
            if not any(entry.key == canonical_key for entry in language_entries):
                raise manifest_error(f"{base}.canonical_entry", f"missing variant for {canonical_key!r}")
            parsed.extend(language_entries)
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        raise ValueError("\n".join(errors))
    ensure_unique((entry.key for entry in parsed), "entries", "entry keys")
    return tuple(parsed)


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
        exec_time_spread=0.0,
        measured_runs=0,
        peak_mem_kib=0,
        bin_size=binary.stat().st_size if binary.exists() else 0,
        binary_path=binary,
    )


def with_affinity(command: list[str], cpu_list: str | None) -> list[str]:
    if cpu_list and tool("taskset"):
        return ["taskset", "--cpu-list", cpu_list, *command]
    return command


def sh(command: list[str], cwd: Path | None = None, capture: bool = True, cpu_list: str | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(FIXED_ENV)
    return subprocess.run(
        with_affinity(command, cpu_list),
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=capture,
        text=True,
        check=False,
    )


def timed(command: list[str], cwd: Path | None = None, stdin_text: str | None = None, cpu_list: str | None = None) -> tuple[subprocess.CompletedProcess[str], float, int]:
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
        try:
            proc = subprocess.Popen(
                with_affinity(command, cpu_list),
                cwd=str(cwd) if cwd else None,
                env=env,
                stdin=stdin_file if stdin_text is not None else None,
                stdout=stdout_file,
                stderr=stderr_file,
                text=True,
            )
        except FileNotFoundError as exc:
            end = time.perf_counter()
            return subprocess.CompletedProcess(command, 127, "", str(exc)), end - start, 0
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


def sarifc_version_or_dash() -> str:
    try:
        command = [*sarifc_driver_command(), "--version"]
    except ValueError:
        return "-"
    proc = sh(command)
    text = (proc.stdout or proc.stderr).strip().splitlines()
    return text[0].strip() if text else "-"


def cpu_count() -> int:
    return os.cpu_count() or 1


def sarif_repo_candidates() -> tuple[Path, ...]:
    configured = os.environ.get("BNCH_SARIF_REPO")
    candidates: list[Path] = []
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.extend((ROOT.parent / "sarif", ROOT.parent / "sarif-main"))
    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate not in seen:
            unique.append(candidate)
            seen.add(candidate)
    return tuple(unique)


def sarif_manifest_candidates() -> tuple[Path, ...]:
    return tuple(candidate / "Cargo.toml" for candidate in sarif_repo_candidates())


def sarif_bin_candidates() -> tuple[Path, ...]:
    candidates: list[Path] = []
    for repo in sarif_repo_candidates():
        candidates.extend(
            (
                repo / "target" / "release" / "sarifc",
                repo / "target" / "debug" / "sarifc",
            )
        )
    return tuple(candidates)


def sarif_binary_is_fresh(repo: Path, binary: Path) -> bool:
    if not binary.is_file():
        return False
    try:
        binary_mtime = binary.stat().st_mtime
    except OSError:
        return False
    source_globs = ("Cargo.toml", "Cargo.lock", "build.rs", "*.rs", "*.c", "*.h")
    for pattern in source_globs:
        for path in repo.rglob(pattern):
            if not path.is_file():
                continue
            try:
                if path.stat().st_mtime > binary_mtime:
                    return False
            except OSError:
                return False
    return True


def has_required_tools(entry: EntrySpec) -> bool:
    return all(tool(name) for name in entry.required_tools)


def entry_is_available(entry: EntrySpec) -> bool:
    if entry.language == "sarif":
        try:
            sarifc_driver_command()
        except ValueError:
            return False
        return True
    return has_required_tools(entry)


def entries(include_variants: bool = False, include_experimental: bool = False) -> list[EntrySpec]:
    found = [entry for entry in entry_specs() if entry_is_available(entry)]
    if not include_experimental:
        found = [entry for entry in found if entry.track == "main"]
    return found if include_variants else [entry for entry in found if entry.canonical]


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


def benchmark_map() -> dict[str, BenchmarkSpec]:
    return {spec.name: spec for spec in benchmark_specs()}


def canonical_entry_map() -> dict[str, EntrySpec]:
    return {
        entry.language: entry
        for entry in entry_specs()
        if entry.canonical and entry.track == "main"
    }


def host_cpu_model() -> str:
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text(encoding="utf-8").splitlines():
            if line.startswith("model name"):
                return line.partition(":")[2].strip()
    return "-"


def host_memory_gib() -> str:
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                kib = int(line.split()[1])
                return f"{kib / (1024.0 * 1024.0):.2f}"
    return "-"


def current_cgroup_path() -> Path | None:
    cgroup_file = Path("/proc/self/cgroup")
    if not cgroup_file.exists():
        return None
    for line in cgroup_file.read_text(encoding="utf-8").splitlines():
        parts = line.split(":", 2)
        if len(parts) == 3 and parts[0] == "0":
            return Path("/sys/fs/cgroup") / parts[2].lstrip("/")
    return None


@functools.cache
def memory_measurement() -> MemoryMeasurement:
    cgroup_path = current_cgroup_path()
    if cgroup_path is None:
        return MemoryMeasurement("ru_maxrss", "cgroup path unavailable")
    peak_path = cgroup_path / "memory.peak"
    if peak_path.exists():
        try:
            peak_path.write_text("0\n", encoding="utf-8")
            return MemoryMeasurement("cgroupv2-memory.peak", str(peak_path))
        except OSError as exc:
            return MemoryMeasurement("ru_maxrss", f"{peak_path} unavailable for reset ({exc.strerror})")
    return MemoryMeasurement("ru_maxrss", f"{peak_path} unavailable")


def has_lld() -> bool:
    return tool("ld.lld") is not None


def sarifc_driver_command(build: bool = False) -> list[str]:
    if tool("cargo") and tool("rustc"):
        for manifest in sarif_manifest_candidates():
            if manifest.is_file():
                repo = manifest.parent
                candidate = sarifc_repo_driver_binary(repo, manifest, build)
                if candidate is not None:
                    return [str(candidate)]
                return ["cargo", "run", "--quiet", "--manifest-path", str(manifest), "-p", "sarifc", "--"]
    for candidate in sarif_bin_candidates():
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return [str(candidate)]
    installed = tool("sarifc")
    if installed is not None:
        return [installed]
    raise ValueError(
        "sarif entry requires `sarifc` on PATH or a Sarif checkout via BNCH_SARIF_REPO, ~/sarif, or ~/sarif-main"
    )


@functools.cache
def sarifc_repo_driver_binary(repo: Path, manifest: Path, build: bool) -> Path | None:
    for candidate in (repo / "target" / "release" / "sarifc", repo / "target" / "debug" / "sarifc"):
        if os.access(candidate, os.X_OK) and sarif_binary_is_fresh(repo, candidate):
            return candidate
    if not build:
        return None
    command = [
        "cargo",
        "build",
        "--quiet",
        "--manifest-path",
        str(manifest),
        "-p",
        "sarifc",
        "--release",
    ]
    proc = sh(command, cwd=repo)
    if proc.returncode != 0:
        raise ValueError(
            f"sarifc build failed for {manifest}: {proc.stderr.strip() or proc.stdout.strip()}"
        )
    release = repo / "target" / "release" / "sarifc"
    if os.access(release, os.X_OK):
        return release
    debug = repo / "target" / "debug" / "sarifc"
    if os.access(debug, os.X_OK):
        return debug
    raise ValueError(f"sarifc build did not produce a binary at {release}")


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
        if entry.compiler == "clang" and has_lld():
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
            "codegen-units=1",
            "-C",
            "lto=thin",
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
        if entry.compiler == "clang" and has_lld():
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
            "run",
            "--build-only",
            "--release",
            "--strip",
            "--target",
            "native",
            "--frozen",
            "--quiet",
            "cmd/main",
        ]
    if entry.language == "sarif":
        return [*sarifc_driver_command(build=True), "build", str(source), "--print-main", "-o", str(binary)]
    raise ValueError(f"unsupported language: {entry.language}")


def moonbit_build_candidates(source_dir: Path) -> list[Path]:
    build_dir = source_dir / "_build"
    candidates: list[Path] = []
    for path in build_dir.rglob("*"):
        if not path.is_file():
            continue
        if not os.access(path, os.X_OK):
            continue
        if path.suffix in {".o", ".a", ".so", ".dll", ".dylib"}:
            continue
        candidates.append(path)
    return candidates


def find_moonbit_binary(source_dir: Path, build_output: str) -> Path:
    declared: list[Path] = []
    for line in reversed(build_output.splitlines()):
        text = line.strip()
        if not text.startswith("{"):
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        artifacts = payload.get("artifacts_path")
        if isinstance(artifacts, list):
            for artifact in artifacts:
                if isinstance(artifact, str):
                    path = Path(artifact)
                    if path.exists():
                        return path
                    declared.append(path)
    build_dir = source_dir / "_build"
    for _ in range(10):
        candidates = moonbit_build_candidates(source_dir)
        if candidates:
            return max(candidates, key=lambda path: path.stat().st_mtime_ns)
        for path in declared:
            if path.exists():
                return path
        time.sleep(0.05)
    if declared:
        raise FileNotFoundError(f"no moonbit binary under {build_dir} (declared: {declared[0]})")
    raise FileNotFoundError(f"no moonbit binary under {build_dir}")


def clean_dirs() -> None:
    for path in (BIN, BUILD):
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True, exist_ok=True)
    GO_CACHE.mkdir(parents=True, exist_ok=True)


def prewarm_sarif_native_runtime(active_entries: list[EntrySpec], cpu_list: str | None) -> None:
    if not any(entry.language == "sarif" for entry in active_entries):
        return
    driver = sarifc_driver_command(build=True)
    warmup_dir = BUILD / "sarif-runtime-warmup"
    warmup_dir.mkdir(parents=True, exist_ok=True)
    programs = [
        ("plain", "fn main() -> Text { \"ok\" }\n"),
        (
            "builder",
            "fn main() -> Text effects [alloc] { "
            "let mut b = text_builder_new(); b += \"ok\"; text_builder_finish(b) }\n",
        ),
        (
            "index",
            "fn main() -> Text effects [alloc] { "
            "let mut index = text_index_new(); index = text_index_set(index, \"ok\", 1); \"ok\" }\n",
        ),
        ("sort", (SRC / "sortuniq" / "sortuniq.sarif").read_text(encoding="utf-8")),
    ]
    for name, source_text in programs:
        source = warmup_dir / f"{name}.sarif"
        output = warmup_dir / name
        source.write_text(source_text, encoding="utf-8")
        proc = sh(
            [*driver, "build", str(source), "--print-main", "-o", str(output)],
            cpu_list=cpu_list,
        )
        if proc.returncode != 0:
            raise SystemExit(
                f"sarif runtime warmup failed for {name}: {proc.stderr.strip() or proc.stdout.strip()}"
            )


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
    if ROOT.exists():
        try:
            pycache_dirs = list(ROOT.rglob("__pycache__"))
        except FileNotFoundError:
            pycache_dirs = []
        for path in pycache_dirs:
            shutil.rmtree(path, ignore_errors=True)


def cleanup_generated_dirs() -> None:
    for path in (BIN, BUILD):
        shutil.rmtree(path, ignore_errors=True)
    run_root = RUN_ROOT
    while run_root != ROOT and run_root.exists():
        try:
            run_root.rmdir()
        except OSError:
            break
        run_root = run_root.parent


def ensure_consistent_outputs(spec: BenchmarkSpec, outputs: list[str]) -> str | None:
    if not outputs:
        return "run-fail"
    try:
        canonical_outputs = [canonical_output(spec, output) for output in outputs]
    except ValueError:
        return "output-invalid"
    return None if len(set(canonical_outputs)) == 1 else "output-unstable"


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
    if stripped_state(path) == "yes":
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


def median(values: list[float]) -> float:
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2.0


def relative_spread(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    center = median(values)
    if center <= 0:
        return 0.0
    return (max(values) - min(values)) / center


def category_benchmark_weights(benchmarks: list[BenchmarkSpec]) -> dict[str, float]:
    category_totals: dict[str, float] = {}
    for spec in benchmarks:
        category_totals[spec.category] = category_totals.get(spec.category, 0.0) + spec.weight
    category_count = len(category_totals)
    if category_count == 0:
        return {}
    weights: dict[str, float] = {}
    for spec in benchmarks:
        category_total = category_totals[spec.category]
        if category_total <= 0:
            continue
        weights[spec.name] = (1.0 / category_count) * (spec.weight / category_total)
    return weights


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
    benchmark_weights = category_benchmark_weights(benchmarks)
    for spec in benchmarks:
        rows = [row for row in by_benchmark.get(spec.name, []) if row.entry in complete_entries]
        if not rows:
            continue
        benchmark_weight = benchmark_weights.get(spec.name, 0.0)
        if benchmark_weight <= 0:
            continue
        for metric in metric_names:
            best = min(metric_value(row, metric) for row in rows)
            if best <= 0:
                continue
            weight = benchmark_weight * metric_weights[metric]
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


def environment_data(run_args: argparse.Namespace, active_entries: list[EntrySpec], benchmarks: list[BenchmarkSpec]) -> dict[str, object]:
    memory_info = memory_measurement()
    tool_versions = {name: version_or_dash(command) for name, command in TOOL_VERSION_COMMANDS}
    if any(entry.language == "sarif" for entry in active_entries):
        tool_versions["sarifc"] = sarifc_version_or_dash()
    return {
        "objective": PROJECT_OBJECTIVE,
        "runs": run_args.runs,
        "min_runs": run_args.min_runs,
        "warmup": run_args.warmup,
        "runtime_target_s": run_args.runtime_target,
        "max_relative_spread": run_args.max_relative_spread,
        "build_jobs": run_args.build_jobs,
        "canonical_entries_only": not run_args.all_entries,
        "experimental_entries": run_args.experimental_entries,
        "selected_benchmarks": ",".join(spec.name for spec in benchmarks),
        "cpu_affinity": run_args.cpu_list or "",
        "scoring_balance": "equal category weight, benchmark weights normalized within category",
        "link_policy": "toolchain-default release mode (mixed linkage; see entry metadata)",
        "entries": len(active_entries),
        "benchmarks": len(benchmarks),
        "cpu_model": host_cpu_model(),
        "logical_cores": cpu_count(),
        "memory_gib": host_memory_gib(),
        "peak_memory_mode": memory_info.mode,
        "peak_memory_detail": memory_info.detail,
        "kernel": os.uname().release,
        "tool_versions": tool_versions,
    }


def display_env_value(value: object) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    if value == "":
        return "-"
    return str(value)


def environment_rows(run_args: argparse.Namespace, active_entries: list[EntrySpec], benchmarks: list[BenchmarkSpec]) -> list[list[str]]:
    data = environment_data(run_args, active_entries, benchmarks)
    row_keys = (
        "objective",
        "runs",
        "min_runs",
        "warmup",
        "runtime_target_s",
        "max_relative_spread",
        "build_jobs",
        "canonical_entries_only",
        "experimental_entries",
        "selected_benchmarks",
        "cpu_affinity",
        "scoring_balance",
        "link_policy",
        "entries",
        "benchmarks",
        "cpu_model",
        "logical_cores",
        "memory_gib",
        "peak_memory_mode",
        "peak_memory_detail",
        "kernel",
    )
    rows = [[key, display_env_value(data[key])] for key in row_keys]
    rows.extend([[name, version] for name, version in data["tool_versions"].items()])
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


def entry_policy_rows(active_entries: list[EntrySpec]) -> list[list[str]]:
    return [
        [
            entry.label,
            entry.build_profile,
            "; ".join(entry.optimization_notes),
        ]
        for entry in active_entries
    ]


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


def build_summary_data(
    results: list[Result],
    benchmarks: list[BenchmarkSpec],
    metric_weights: dict[str, float] | None = None,
) -> SummaryData:
    valid_benchmarks = scored_benchmarks(results, benchmarks)
    composite_weights = metric_weights or METRIC_WEIGHTS
    overall_scores = metric_scores(results, valid_benchmarks, composite_weights)
    metric_score_maps = {
        label: metric_scores(results, valid_benchmarks, {metric: 1.0})
        for label, metric in SUMMARY_METRICS
    }
    overall_order = [entry for entry, _ in sorted(overall_scores.items(), key=lambda item: item[1], reverse=True)]
    metric_orders = {
        label: [entry for entry, _ in sorted(scores.items(), key=lambda item: item[1], reverse=True)]
        for label, scores in metric_score_maps.items()
    }
    return SummaryData(
        overall_scores=overall_scores,
        overall_order=overall_order,
        overall_ranks=rank_positions(overall_scores, reverse=True),
        metric_scores=metric_score_maps,
        metric_orders=metric_orders,
        metric_ranks={label: rank_positions(scores, reverse=True) for label, scores in metric_score_maps.items()},
    )


def build_profile_summaries(results: list[Result], benchmarks: list[BenchmarkSpec]) -> list[ProfileSummary]:
    return [
        ProfileSummary(label=label, description=description, summary=build_summary_data(results, benchmarks, weights))
        for label, weights, description in PROFILE_WEIGHTS
    ]


def summary_headers() -> list[str]:
    return ["Overall", "Entry", "Score", *[label for label, _ in SUMMARY_METRICS]]


def summary_rows(summary: SummaryData, active_entries: list[EntrySpec]) -> list[list[str]]:
    labels = entry_labels(active_entries)

    rows: list[list[str]] = []
    for entry_key in summary.overall_order:
        metric_cells: list[str] = []
        for label, _ in SUMMARY_METRICS:
            value = summary.metric_scores[label].get(entry_key)
            if value is None:
                metric_cells.append("-")
                continue
            metric_cells.append(fmt_normalized_score(value))
        rows.append(
            [
                str(summary.overall_ranks[entry_key]),
                labels[entry_key],
                fmt_normalized_score(summary.overall_scores[entry_key]),
                *metric_cells,
            ]
        )
    return rows


def metric_view_headers(label: str) -> list[str]:
    return [f"{label} Rank", "Entry", f"{label} Score", "Composite Score"]


def metric_view_rows(summary: SummaryData, active_entries: list[EntrySpec], label: str) -> list[list[str]]:
    labels = entry_labels(active_entries)
    rows: list[list[str]] = []
    for entry_key in summary.metric_orders.get(label, []):
        rows.append(
            [
                str(summary.metric_ranks[label][entry_key]),
                labels[entry_key],
                fmt_normalized_score(summary.metric_scores[label][entry_key]),
                fmt_normalized_score(summary.overall_scores.get(entry_key, 0.0)),
            ]
        )
    return rows


def profile_headers() -> list[str]:
    return ["Profile", "Leader", "Runner-Up", "Third", "Intent"]


def profile_rows(profiles: list[ProfileSummary], active_entries: list[EntrySpec]) -> list[list[str]]:
    labels = entry_labels(active_entries)
    rows: list[list[str]] = []
    for profile in profiles:
        leaders = [labels[entry] for entry in profile.summary.overall_order[:3]]
        while len(leaders) < 3:
            leaders.append("-")
        rows.append([profile.label, leaders[0], leaders[1], leaders[2], profile.description])
    return rows


def benchmark_unique_capabilities(benchmarks: list[BenchmarkSpec]) -> dict[str, list[str]]:
    counts: dict[str, int] = {}
    for spec in benchmarks:
        for capability in spec.capabilities:
            counts[capability] = counts.get(capability, 0) + 1
    return {
        spec.name: [capability for capability in spec.capabilities if counts.get(capability, 0) == 1]
        for spec in benchmarks
    }


def benchmark_coverage_rows(benchmarks: list[BenchmarkSpec]) -> list[list[str]]:
    effective_weights = category_benchmark_weights(benchmarks)
    unique_capabilities = benchmark_unique_capabilities(benchmarks)
    return [
        [
            spec.name,
            CATEGORY_LABELS.get(spec.category, spec.category),
            f"{spec.weight:.2f}",
            f"{effective_weights.get(spec.name, 0.0):.4f}",
            ", ".join(spec.capabilities),
            ", ".join(unique_capabilities.get(spec.name, [])) or "-",
            spec.retained_for,
        ]
        for spec in benchmarks
    ]


def build_category_summary(results: list[Result], benchmarks: list[BenchmarkSpec]) -> CategorySummary:
    valid_benchmarks = scored_benchmarks(results, benchmarks)
    categories = [key for key in CATEGORY_LABELS if any(spec.category == key for spec in valid_benchmarks)]
    scores = {
        category: metric_scores(results, [spec for spec in valid_benchmarks if spec.category == category], METRIC_WEIGHTS)
        for category in categories
    }
    return CategorySummary(labels=categories, scores=scores)


def category_headers(category_summary: CategorySummary) -> list[str]:
    return ["Entry", *[CATEGORY_LABELS[label] for label in category_summary.labels], "Overall"]


def category_rows(category_summary: CategorySummary, summary: SummaryData, active_entries: list[EntrySpec]) -> list[list[str]]:
    labels = entry_labels(active_entries)
    rows: list[list[str]] = []
    for entry_key in summary.overall_order:
        rows.append(
            [
                labels[entry_key],
                *[
                    fmt_normalized_score(category_summary.scores[category][entry_key]) if entry_key in category_summary.scores[category] else "-"
                    for category in category_summary.labels
                ],
                fmt_normalized_score(summary.overall_scores[entry_key]),
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


def source_files_for_entry(benchmark: str, entry: EntrySpec) -> list[Path]:
    source = source_path(benchmark, entry)
    if entry.language == "moonbit":
        return sorted(source.rglob("*.mbt"))
    return [source]


def count_source_metrics(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    return len(text.splitlines()), len(text)


def aggregate_source_metrics(active_entries: list[EntrySpec], benchmarks: list[BenchmarkSpec]) -> dict[str, SourceMetrics]:
    metrics: dict[str, SourceMetrics] = {}
    for entry in active_entries:
        benchmark_count = 0
        line_count = 0
        char_count = 0
        for spec in benchmarks:
            files = source_files_for_entry(spec.name, entry)
            if not files:
                continue
            benchmark_count += 1
            for path in files:
                lines, chars = count_source_metrics(path)
                line_count += lines
                char_count += chars
        metrics[entry.key] = SourceMetrics(benchmarks=benchmark_count, lines=line_count, chars=char_count)
    return metrics


def source_metric_rows(active_entries: list[EntrySpec], benchmarks: list[BenchmarkSpec]) -> list[list[str]]:
    labels = entry_labels(active_entries)
    metrics = aggregate_source_metrics(active_entries, benchmarks)
    complete = [entry.key for entry in active_entries if metrics.get(entry.key, SourceMetrics(0, 0, 0)).benchmarks == len(benchmarks)]
    if not complete:
        return []
    best_lines = min(metrics[key].lines for key in complete if metrics[key].lines > 0)
    best_chars = min(metrics[key].chars for key in complete if metrics[key].chars > 0)
    ordered = sorted(complete, key=lambda key: (metrics[key].chars, metrics[key].lines, labels[key]))
    return [
        [
            labels[key],
            str(metrics[key].benchmarks),
            str(metrics[key].lines),
            str(metrics[key].chars),
            f"{best_lines / metrics[key].lines:.4f}",
            f"{best_chars / metrics[key].chars:.4f}",
        ]
        for key in ordered
    ]


def benchmark_payloads(benchmarks: list[BenchmarkSpec]) -> list[dict[str, object]]:
    effective_weights = category_benchmark_weights(benchmarks)
    return [
        {
            "name": spec.name,
            "category": spec.category,
            "input": spec.input_label,
            "base_weight": spec.weight,
            "effective_weight": effective_weights.get(spec.name, 0.0),
            "check": spec.check,
            "output_kind": OUTPUT_KIND_BY_CHECK[spec.check],
            "algorithm": spec.algorithm,
            "time_complexity": spec.time_complexity,
            "space_complexity": spec.space_complexity,
            "output_contract": spec.output_contract,
            "fairness_notes": spec.fairness_notes,
            "capabilities": list(spec.capabilities),
            "retained_for": spec.retained_for,
        }
        for spec in benchmarks
    ]


def entry_payloads(active_entries: list[EntrySpec]) -> list[dict[str, object]]:
    return [
        {
            "key": entry.key,
            "label": entry.label,
            "language": entry.language,
            "compiler": entry.compiler,
            "backend": entry.backend,
            "track": entry.track,
            "canonical": entry.canonical,
            "supported_benchmarks": list(entry.supported_benchmarks)
            if entry.supported_benchmarks is not None
            else None,
            "build_profile": entry.build_profile,
            "optimization_notes": list(entry.optimization_notes),
        }
        for entry in active_entries
    ]


def comparative_report(summary: SummaryData) -> bool:
    return len(summary.overall_order) >= 2


def comparative_report_note(summary: SummaryData) -> str | None:
    if comparative_report(summary):
        return None
    if len(summary.overall_order) == 1:
        return "This report is non-comparative: only one scored entry is present, so ranks and normalized scores are placeholders rather than cross-language conclusions."
    return "This report is non-comparative: no scored entries were available, so ranking views are omitted."


def table_section(title: str, headers: list[str], rows: list[list[str]]) -> list[str]:
    return [title, "", markdown_table(headers, rows), ""]


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
    summary = build_summary_data(results, benchmarks)
    profiles = build_profile_summaries(results, benchmarks)
    category_summary = build_category_summary(results, benchmarks)
    content = ["# Benchmark Report", ""]
    content.extend(table_section("## Environment", ["Setting", "Value"], environment_rows(run_args, active_entries, benchmarks)))
    content.extend(table_section("## Entries", ENTRY_TABLE_HEADERS, entry_rows(active_entries, results)))
    content.extend(table_section("## Entry Policies", ENTRY_POLICY_HEADERS, entry_policy_rows(active_entries)))
    source_rows = source_metric_rows(active_entries, benchmarks)
    if source_rows:
        content.extend(table_section("## Source Concision", SOURCE_TABLE_HEADERS, source_rows))
    content.extend(table_section("## Benchmark Coverage", BENCHMARK_COVERAGE_HEADERS, benchmark_coverage_rows(benchmarks)))
    content.extend(table_section("## Benchmarks", BENCHMARK_TABLE_HEADERS, benchmark_rows(benchmarks)))

    excluded = excluded_benchmark_rows(results, benchmarks, active_entries)
    if excluded:
        content.extend(table_section("## Excluded", ["Excluded From Score", "Reason"], excluded))

    note = comparative_report_note(summary)
    if note is not None:
        content.extend(["## Interpretation", "", note, ""])

    if summary.overall_scores:
        content.extend(table_section("## Decision Profiles", profile_headers(), profile_rows(profiles, active_entries)))
        content.extend(table_section("## Categories", category_headers(category_summary), category_rows(category_summary, summary, active_entries)))

    if summary.overall_scores:
        content.extend(
            [
                "## Summary",
                "",
                markdown_table(summary_headers(), summary_rows(summary, active_entries)),
                "",
                "_Displayed scores use median runtime with equal category weighting and benchmark normalization inside each category. Views stay on the same absolute 0..1 scale across report revisions, so regressions remain directly comparable over time._",
                "",
            ]
        )
        for label, _ in SUMMARY_METRICS:
            content.extend(table_section(f"## {label} View", metric_view_headers(label), metric_view_rows(summary, active_entries, label)))

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


def json_data(
    run_args: argparse.Namespace,
    active_entries: list[EntrySpec],
    benchmarks: list[BenchmarkSpec],
    results: list[Result],
) -> dict[str, object]:
    summary = build_summary_data(results, benchmarks)
    profiles = build_profile_summaries(results, benchmarks)
    category_summary = build_category_summary(results, benchmarks)
    return {
        "environment": environment_data(run_args, active_entries, benchmarks),
        "comparative": comparative_report(summary),
        "comparative_note": comparative_report_note(summary),
        "entries": entry_payloads(active_entries),
        "source_metrics": {
            key: {
                "benchmarks": value.benchmarks,
                "source_lines": value.lines,
                "source_chars": value.chars,
            }
            for key, value in aggregate_source_metrics(active_entries, benchmarks).items()
        },
        "benchmarks": benchmark_payloads(benchmarks),
        "category_scores": category_summary.scores,
        "overall_scores": summary.overall_scores,
        "overall_ranks": summary.overall_ranks,
        "metric_scores": summary.metric_scores,
        "metric_ranks": summary.metric_ranks,
        "decision_profiles": [
            {
                "label": profile.label,
                "description": profile.description,
                "overall_scores": profile.summary.overall_scores,
                "overall_ranks": profile.summary.overall_ranks,
                "leaders": profile.summary.overall_order[:3],
            }
            for profile in profiles
        ],
        "results": [
            {
                "benchmark": result.benchmark,
                "entry": result.entry,
                "input": result.input_text,
                "output": result.output_text,
                "reference": result.reference_text,
                "status": result.status,
                "build_time_s": result.build_time,
                "run_time_s": result.exec_time,
                "run_time_relative_spread": result.exec_time_spread,
                "measured_runs": result.measured_runs,
                "peak_memory_kib": result.peak_mem_kib,
                "binary_size_bytes": result.bin_size,
            }
            for result in results
        ],
    }


def finalize_binary(
    entry: EntrySpec,
    binary: Path,
    build_dir: Path,
    build_time: float,
    source: Path,
    build_stdout: str,
) -> BuiltArtifact:
    if entry.language == "moonbit":
        built = find_moonbit_binary(source, build_stdout)
        binary.unlink(missing_ok=True)
        shutil.copy2(built, binary)
        binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    build_time += strip_binary(binary)
    return BuiltArtifact(binary=binary, build_time=build_time)


def write_build_failure_logs(binary: Path, build_proc: subprocess.CompletedProcess[str]) -> None:
    failure_dir = ROOT / ".failures" / binary.name
    failure_dir.mkdir(parents=True, exist_ok=True)
    (failure_dir / "build.stdout.txt").write_text(build_proc.stdout, encoding="utf-8")
    (failure_dir / "build.stderr.txt").write_text(build_proc.stderr, encoding="utf-8")


def build_with_retry(
    entry: EntrySpec,
    command: list[str],
    binary: Path,
    build_dir: Path,
    build_cwd: Path | None,
    cpu_list: str | None,
) -> tuple[subprocess.CompletedProcess[str], float]:
    total_build_time = 0.0
    last_proc = subprocess.CompletedProcess(command, 127, "", "build did not run")
    for attempt in range(3):
        build_proc, build_time, _ = timed(command, cwd=build_cwd, cpu_list=cpu_list)
        total_build_time += build_time
        last_proc = build_proc
        build_succeeded = build_proc.returncode == 0 and (entry.language == "moonbit" or binary.exists())
        if build_succeeded:
            return build_proc, total_build_time
        if attempt == 2:
            write_build_failure_logs(binary, build_proc)
            return build_proc, total_build_time
        binary.unlink(missing_ok=True)
        shutil.rmtree(build_dir, ignore_errors=True)
        build_dir.mkdir(parents=True, exist_ok=True)
    return last_proc, total_build_time


def stage_run_binary(binary: Path) -> Path | None:
    if not binary.exists():
        return None
    BUILD.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=BUILD, prefix="run-", delete=False) as handle:
        staged = Path(handle.name)
    shutil.copy2(binary, staged)
    staged.chmod(staged.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return staged


def should_continue_sampling(exec_times: list[float], min_runs: int, max_runs: int, runtime_target: float, max_relative_spread: float) -> bool:
    if len(exec_times) < min_runs:
        return True
    if len(exec_times) >= max_runs:
        return False
    total_runtime = sum(exec_times)
    if total_runtime < runtime_target:
        return True
    return relative_spread(exec_times) > max_relative_spread


def measured_runtime(exec_times: list[float]) -> float:
    return median(exec_times)


def run_binary(
    spec: BenchmarkSpec,
    binary: Path,
    args: tuple[str, ...],
    stdin_text: str | None,
    min_runs: int,
    max_runs: int,
    runtime_target: float,
    max_relative_spread: float,
    cpu_list: str | None,
) -> RunBinaryResult | None:
    exec_times: list[float] = []
    peak_kibs: list[int] = []
    outputs: list[str] = []
    while should_continue_sampling(exec_times, min_runs, max_runs, runtime_target, max_relative_spread):
        staged = stage_run_binary(binary)
        if staged is None:
            return None
        try:
            run_proc, exec_time, peak_kib = timed([str(staged), *args], stdin_text=stdin_text, cpu_list=cpu_list)
        finally:
            staged.unlink(missing_ok=True)
        if run_proc.returncode != 0:
            return None
        outputs.append(normalize_output(run_proc.stdout))
        exec_times.append(exec_time)
        peak_kibs.append(peak_kib)
    status = ensure_consistent_outputs(spec, outputs)
    if status is not None:
        return RunBinaryResult(exec_times=exec_times, peak_kibs=peak_kibs, output=outputs[-1], status=status)
    return RunBinaryResult(exec_times=exec_times, peak_kibs=peak_kibs, output=outputs[-1], status="ok")


def validate_report_paths(report_path: Path, json_path: Path) -> None:
    if report_path == json_path:
        raise SystemExit("report and json outputs must be different files")
    for path in (report_path, json_path):
        if path.exists() and path.is_dir():
            raise SystemExit(f"output path is a directory: {path}")


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
        temp_path = Path(handle.name)
    temp_path.replace(path)


def build_and_run(spec: BenchmarkSpec, entry: EntrySpec, run_args: argparse.Namespace) -> Result:
    binary = BIN / f"{spec.name}__{entry.key}"
    build_dir = BUILD / f"{spec.name}__{entry.key}"
    build_dir.mkdir(parents=True, exist_ok=True)
    binary.parent.mkdir(parents=True, exist_ok=True)

    source = source_path(spec.name, entry)
    command = build_command(spec, entry, binary, build_dir, run_args.build_jobs)
    build_cwd = source if entry.language == "moonbit" else None

    stdin_text = benchmark_input_text(spec)
    build_proc, build_time = build_with_retry(
        entry,
        command,
        binary,
        build_dir,
        build_cwd,
        run_args.cpu_list,
    )
    if build_proc.returncode != 0:
        return failed_result(spec, entry, benchmark_input_label(spec), "build-fail", build_time, binary)
    if entry.language != "moonbit" and not binary.exists():
        return failed_result(spec, entry, benchmark_input_label(spec), "build-fail", build_time, binary)

    artifact = finalize_binary(
        entry,
        binary,
        build_dir,
        build_time,
        source,
        f"{build_proc.stdout}\n{build_proc.stderr}",
    )
    if not artifact.binary.exists():
        return failed_result(spec, entry, benchmark_input_label(spec), "build-fail", artifact.build_time, artifact.binary)
    artifact_size = artifact.binary.stat().st_size

    args = benchmark_args(spec)
    if run_args.warmup:
        warmup = run_binary(
            spec,
            artifact.binary,
            args,
            stdin_text,
            run_args.warmup,
            run_args.warmup,
            0.0,
            0.0,
            run_args.cpu_list,
        )
        if warmup is None:
            return failed_result(spec, entry, benchmark_input_label(spec), "run-fail", artifact.build_time, artifact.binary)
        if warmup.status != "ok":
            return failed_result(spec, entry, benchmark_input_label(spec), warmup.status, artifact.build_time, artifact.binary)

    measured = run_binary(
        spec,
        artifact.binary,
        args,
        stdin_text,
        run_args.min_runs,
        run_args.runs,
        run_args.runtime_target,
        run_args.max_relative_spread,
        run_args.cpu_list,
    )
    if measured is None:
        return failed_result(spec, entry, benchmark_input_label(spec), "run-fail", artifact.build_time, artifact.binary)
    if measured.status != "ok":
        return failed_result(spec, entry, benchmark_input_label(spec), measured.status, artifact.build_time, artifact.binary)
    exec_times = measured.exec_times
    peak_kibs = measured.peak_kibs
    output = measured.output

    return Result(
        benchmark=spec.name,
        entry=entry.key,
        input_text=benchmark_input_label(spec),
        raw_output=output,
        output_text=compact_output(spec.name, output),
        reference_text="-",
        status="ok",
        build_time=artifact.build_time,
        exec_time=measured_runtime(exec_times),
        exec_time_spread=relative_spread(exec_times),
        measured_runs=len(exec_times),
        peak_mem_kib=max(peak_kibs),
        bin_size=artifact_size,
        binary_path=artifact.binary,
    )


def apply_references(results: list[Result], benchmarks: list[BenchmarkSpec]) -> None:
    rows_by_benchmark: dict[str, list[Result]] = {}
    for row in results:
        rows_by_benchmark.setdefault(row.benchmark, []).append(row)

    for spec in benchmarks:
        benchmark_rows = rows_by_benchmark.get(spec.name, [])
        ok_rows = [row for row in benchmark_rows if row.status == "ok"]
        if not ok_rows:
            continue
        canonical_rows = [(row, canonical_output(spec, row.raw_output)) for row in ok_rows]
        reference_counts: dict[str, int] = {}
        first_seen: dict[str, int] = {}
        for index, (_, canonical) in enumerate(canonical_rows):
            reference_counts[canonical] = reference_counts.get(canonical, 0) + 1
            first_seen.setdefault(canonical, index)
        canonical_reference = max(
            reference_counts,
            key=lambda canonical: (reference_counts[canonical], -first_seen[canonical]),
        )
        for row, canonical in canonical_rows:
            row.output_text = compact_output(spec.name, canonical)
            row.reference_text = compact_output(spec.name, canonical_reference)
            row.status = "ok" if canonical == canonical_reference else "mismatch"
        for row in benchmark_rows:
            if row.status != "ok":
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


def supported_benchmark_names(entries: list[EntrySpec], available_names: list[str]) -> list[str]:
    supported = set(available_names)
    for entry in entries:
        if entry.supported_benchmarks is not None:
            supported &= set(entry.supported_benchmarks)
    return [name for name in available_names if name in supported]


def resolve_selection(run_args: argparse.Namespace, available_entries: list[EntrySpec]) -> Selection:
    compare_entry_overlap = getattr(run_args, "compare_entry_overlap", None)
    if not isinstance(compare_entry_overlap, str) or not compare_entry_overlap:
        compare_entry_overlap = None
    available_entry_keys = [entry.key for entry in available_entries]
    selected_entry_keys = set(selected_keys(run_args.entry, available_entry_keys, "entry"))
    if compare_entry_overlap:
        if compare_entry_overlap not in available_entry_keys:
            raise SystemExit(
                f"unknown entry for --compare-entry-overlap: {compare_entry_overlap}"
            )
        selected_entry_keys.add(compare_entry_overlap)
    chosen_entries = [entry for entry in available_entries if entry.key in selected_entry_keys]
    if not chosen_entries:
        raise SystemExit("no active entries selected")

    available_benchmark_specs = list(benchmark_specs())
    available_benchmark_keys = [spec.name for spec in available_benchmark_specs]
    selected_benchmark_keys = set(selected_keys(run_args.benchmark, available_benchmark_keys, "benchmark"))
    if compare_entry_overlap:
        overlap_entry = next(
            entry for entry in chosen_entries if entry.key == compare_entry_overlap
        )
        overlap_keys = set(
            supported_benchmark_names([overlap_entry], available_benchmark_keys)
        )
        if run_args.benchmark:
            unsupported = sorted(selected_benchmark_keys - overlap_keys)
            if unsupported:
                raise SystemExit(
                    "unsupported benchmark selection for --compare-entry-overlap: "
                    + ", ".join(unsupported)
                )
        selected_benchmark_keys &= overlap_keys
    compatible_benchmark_keys = set(supported_benchmark_names(chosen_entries, available_benchmark_keys))
    if run_args.benchmark:
        unsupported = sorted(selected_benchmark_keys - compatible_benchmark_keys)
        if unsupported:
            raise SystemExit("unsupported benchmark selection for active entries: " + ", ".join(unsupported))
    selected_benchmark_keys &= compatible_benchmark_keys
    chosen_benchmarks = [spec for spec in available_benchmark_specs if spec.name in selected_benchmark_keys]
    if not chosen_benchmarks:
        raise SystemExit("no compatible benchmarks selected")

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
    parser.add_argument("--runs", type=positive_int, default=5, help="Maximum measured runs per benchmark after warmup.")
    parser.add_argument("--min-runs", type=positive_int, default=2, help="Minimum measured runs per benchmark before adaptive stopping.")
    parser.add_argument("--warmup", type=non_negative_int, default=1, help="Warmup runs before timing.")
    parser.add_argument("--runtime-target", type=float, default=0.35, help="Keep sampling until measured runtime reaches this total, unless max runs is hit.")
    parser.add_argument("--max-relative-spread", type=float, default=0.03, help="Adaptive timing stops once relative runtime spread drops to this threshold.")
    parser.add_argument("--build-jobs", type=positive_int, default=cpu_count(), help="Parallel jobs used by supported build tools.")
    parser.add_argument("--report-path", default=str(DEFAULT_REPORT), help="Output path for the generated markdown report.")
    parser.add_argument("--json-path", default=str(DEFAULT_JSON_REPORT), help="Output path for the generated JSON report.")
    parser.add_argument("--entry", action="append", help="Entry key or comma-separated entry keys to include.")
    parser.add_argument("--benchmark", action="append", help="Benchmark name or comma-separated benchmark names to include.")
    parser.add_argument(
        "--compare-entry-overlap",
        help="Include the named entry and restrict benchmarks to its supported overlap with the selected suite.",
    )
    parser.add_argument("--all-entries", action="store_true", help="Include non-canonical compiler/backend variants in the run.")
    parser.add_argument("--experimental-entries", action="store_true", help="Include opt-in experimental language entries outside the canonical main track.")
    parser.add_argument("--cpu-list", help="Optional CPU affinity passed to taskset, for example 2 or 2-3.")
    args = parser.parse_args()
    if args.min_runs > args.runs:
        raise SystemExit("--min-runs must be <= --runs")
    if args.runtime_target < 0:
        raise SystemExit("--runtime-target must be >= 0")
    if args.max_relative_spread < 0:
        raise SystemExit("--max-relative-spread must be >= 0")
    return args


def resolve_report_paths(run_args: argparse.Namespace) -> tuple[Path, Path]:
    report_path = Path(run_args.report_path)
    json_path = Path(run_args.json_path)
    if run_args.experimental_entries:
        if report_path == DEFAULT_REPORT:
            report_path = DEFAULT_EXPERIMENTAL_VARIANT_REPORT if run_args.all_entries else DEFAULT_EXPERIMENTAL_REPORT
        if json_path == DEFAULT_JSON_REPORT:
            json_path = DEFAULT_EXPERIMENTAL_VARIANT_JSON_REPORT if run_args.all_entries else DEFAULT_EXPERIMENTAL_JSON_REPORT
    elif run_args.all_entries:
        if report_path == DEFAULT_REPORT:
            report_path = DEFAULT_VARIANT_REPORT
        if json_path == DEFAULT_JSON_REPORT:
            json_path = DEFAULT_VARIANT_JSON_REPORT
    resolved_report = report_path.resolve()
    resolved_json = json_path.resolve()
    validate_report_paths(resolved_report, resolved_json)
    return resolved_report, resolved_json


def validate_manifest_data() -> None:
    errors = [*benchmark_manifest_data().errors, *entry_manifest_data().errors]
    for loader in (benchmark_specs, entry_specs):
        try:
            loader()
        except ValueError as exc:
            errors.extend(str(exc).splitlines())
    if errors:
        raise SystemExit("manifest errors:\n" + "\n".join(errors))


def main() -> int:
    validate_manifest_data()
    args = parse_args()
    available_entries = entries(
        include_variants=args.all_entries,
        include_experimental=args.experimental_entries,
    )
    if not available_entries:
        raise SystemExit("no supported toolchains found")

    selection = resolve_selection(args, available_entries)
    active_entries = selection.entries
    active_benchmarks = selection.benchmarks
    report_path, json_path = resolve_report_paths(args)

    clean_dirs()
    try:
        prewarm_sarif_native_runtime(active_entries, args.cpu_list)
        results = run_suite(args, active_entries, active_benchmarks)
        apply_references(results, active_benchmarks)
        atomic_write(report_path, render_report(args, active_entries, active_benchmarks, results))
        atomic_write(json_path, json.dumps(json_data(args, active_entries, active_benchmarks, results), indent=2) + "\n")
        print(f"wrote {report_path}", file=sys.stderr)
        print(f"wrote {json_path}", file=sys.stderr)
        return 0
    finally:
        cleanup_source_tree()
        cleanup_generated_dirs()


if __name__ == "__main__":
    sys.exit(main())
