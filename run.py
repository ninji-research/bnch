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
REPORT = ROOT / "REPORT.md"

METRIC_WEIGHTS = {
    "exec_time": 0.50,
    "peak_mem": 0.20,
    "build_time": 0.15,
    "bin_size": 0.10,
    "chars": 0.05,
}


@dataclass(frozen=True)
class BenchmarkSpec:
    name: str
    args: tuple[str, ...]
    weight: float
    check: str


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
    chars: int
    binary_path: Path


BENCHMARKS: tuple[BenchmarkSpec, ...] = (
    BenchmarkSpec("ackermann", ("3", "11"), 0.50, "exact"),
    BenchmarkSpec("binarytrees", ("21",), 1.25, "exact"),
    BenchmarkSpec("mandelbrot", ("4000",), 1.50, "exact"),
    BenchmarkSpec("spectralnorm", ("5500",), 1.50, "float"),
    BenchmarkSpec("fannkuch", ("10",), 1.00, "exact"),
    BenchmarkSpec("nbody", ("10000000",), 1.50, "float"),
    BenchmarkSpec("picalc", ("50000000",), 1.25, "pi"),
    BenchmarkSpec("startup", (), 0.50, "exact"),
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


def source_chars(source: Path, entry: EntrySpec) -> int:
    if entry.language == "moonbit":
        total = 0
        for path in sorted(source.rglob("*.mbt")):
            total += len(path.read_text(encoding="utf-8"))
        return total
    return len(source.read_text(encoding="utf-8"))


def benchmark_args(spec: BenchmarkSpec, entry: EntrySpec, workers: int) -> tuple[str, ...]:
    if spec.name == "picalc":
        thread_count = 1 if entry.language == "moonbit" else max(1, workers)
        return spec.args + (str(thread_count),)
    return spec.args


def build_command(spec: BenchmarkSpec, entry: EntrySpec, binary: Path, build_dir: Path, jobs: int) -> list[str]:
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
            str(jobs),
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


def compare_output(spec: BenchmarkSpec, reference: str, output: str) -> bool:
    if spec.check == "exact":
        return output == reference
    if spec.check == "float":
        return math.isclose(parse_first_float(output), parse_first_float(reference), rel_tol=0.0, abs_tol=1e-9)
    if spec.check == "pi":
        return abs(parse_first_float(output) - math.pi) <= 0.01
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


def comment_text(path: Path) -> str:
    proc = sh(["readelf", "-p", ".comment", str(path)])
    if proc.returncode != 0:
        return "-"
    lines: list[str] = []
    for raw in proc.stdout.splitlines():
        line = raw.strip()
        if "]" not in line:
            continue
        lines.append(line.split("]", 1)[1].strip())
    unique: list[str] = []
    for line in lines:
        if line and line not in unique:
            unique.append(line)
    text = " | ".join(unique)
    return text if text else "-"


def metric_value(result: Result, metric: str) -> float:
    if metric == "exec_time":
        return result.exec_time
    if metric == "peak_mem":
        return float(result.peak_mem_kib)
    if metric == "build_time":
        return result.build_time
    if metric == "bin_size":
        return float(result.bin_size)
    if metric == "chars":
        return float(result.chars)
    raise ValueError(metric)


def scores(results: list[Result], benchmarks: list[BenchmarkSpec]) -> dict[str, float]:
    by_benchmark: dict[str, list[Result]] = {}
    for result in results:
        if result.status == "ok":
            by_benchmark.setdefault(result.benchmark, []).append(result)

    complete_entries = {
        result.entry
        for result in results
        if all(
            any(item.entry == result.entry and item.benchmark == spec.name and item.status == "ok" for item in results)
            for spec in benchmarks
        )
    }
    if not complete_entries:
        return {}

    totals = {entry: 0.0 for entry in complete_entries}
    total_weight = 0.0
    for spec in benchmarks:
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
        ["workers", str(run_args.workers)],
        ["entries", str(len(active_entries))],
        ["benchmarks", str(len(benchmarks))],
        ["cpu_count", str(cpu_count())],
        ["gcc", version_line(["gcc", "--version"]) if tool("gcc") else "-"],
        ["clang", version_line(["clang", "--version"]) if tool("clang") else "-"],
        ["rustc", version_line(["rustc", "--version"]) if tool("rustc") else "-"],
        ["nim", version_line(["nim", "--version"]) if tool("nim") else "-"],
        ["ocamlopt", version_line(["ocamlopt", "-version"]) if tool("ocamlopt") else "-"],
        ["moon", version_line(["moon", "version"]) if tool("moon") else "-"],
        ["ld.lld", version_line(["ld.lld", "--version"]) if tool("ld.lld") else "-"],
        ["as", version_line(["as", "--version"]) if tool("as") else "-"],
        ["ocaml c_compiler", ocaml_config_value("c_compiler") if tool("ocamlopt") else "-"],
        ["ocaml native_pack_linker", ocaml_config_value("native_pack_linker") if tool("ocamlopt") else "-"],
        ["ocaml flambda", ocaml_config_value("flambda") if tool("ocamlopt") else "-"],
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
        binary = str(sample.binary_path) if sample else "-"
        comment = comment_text(sample.binary_path) if sample and sample.binary_path.exists() else "-"
        rows.append(
            [
                entry.label,
                entry.compiler,
                entry.backend,
                entry.linker,
                binary,
                sample.build_command if sample else "-",
                comment,
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
                result.reference_text,
                fmt_seconds(result.build_time),
                fmt_seconds(result.exec_time),
                fmt_mib(result.peak_mem_kib),
                fmt_kib(result.bin_size),
                str(result.chars),
                str(result.binary_path),
                result.status,
            ]
        )
    return rows


def weight_rows(benchmarks: list[BenchmarkSpec]) -> list[list[str]]:
    rows = [[f"metric:{name}", f"{weight:.2f}"] for name, weight in METRIC_WEIGHTS.items()]
    rows.extend([["benchmark:" + spec.name, f"{spec.weight:.2f}"] for spec in benchmarks])
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
            ["Entry", "Compiler", "Backend", "Linker", "Binary", "Build Command", ".comment"],
            entry_rows(active_entries, results),
        ),
        "",
    ]

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
            ["Benchmark", "Entry", "Input", "Output", "Reference", "Build s", "Run s", "Peak MiB", "Size KiB", "Chars", "Binary", "Status"],
            result_rows(results, active_entries),
        )
    )
    content.append("")
    return "\n".join(content)


def build_and_run(spec: BenchmarkSpec, entry: EntrySpec, run_args: argparse.Namespace) -> tuple[Result, str]:
    binary = BIN / f"{spec.name}__{entry.key}"
    build_dir = BUILD / f"{spec.name}__{entry.key}"
    build_dir.mkdir(parents=True, exist_ok=True)
    binary.parent.mkdir(parents=True, exist_ok=True)

    source = source_path(spec.name, entry)
    chars = source_chars(source, entry)
    command = build_command(spec, entry, binary, build_dir, run_args.workers)
    command_text = shlex.join(command)
    build_cwd = source if entry.language == "moonbit" else None

    build_proc, build_time, _ = timed(command, cwd=build_cwd)
    if build_proc.returncode != 0:
        stderr = build_proc.stderr or build_proc.stdout or "build failed"
        return (
            Result(
                benchmark=spec.name,
                entry=entry.key,
                input_text=format_input(benchmark_args(spec, entry, run_args.workers)),
                raw_output="",
                output_text="-",
                reference_text="-",
                status="build-fail",
                build_command=command_text,
                build_time=build_time,
                exec_time=0.0,
                peak_mem_kib=0,
                bin_size=0,
                chars=chars,
                binary_path=binary,
            ),
            command_text + " // " + textwrap.shorten(stderr.replace("\n", " "), width=160, placeholder="..."),
        )

    if entry.language == "moonbit":
        built = find_moonbit_binary(build_dir)
        shutil.copy2(built, binary)
        binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    args = benchmark_args(spec, entry, run_args.workers)
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
                    chars=chars,
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
                    chars=chars,
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
            chars=chars,
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
        exact_references[spec.name] = reference
        for row in rows:
            normalized = row.raw_output
            row.reference_text = compact_output(spec.name, reference) if spec.check != "pi" else f"{math.pi:.5f}"
            row.status = "ok" if compare_output(spec, reference, normalized) else "mismatch"
        for row in results:
            if row.benchmark == spec.name and row.status != "ok":
                if spec.check == "pi":
                    row.reference_text = f"{math.pi:.5f}"
                elif spec.name in exact_references:
                    row.reference_text = compact_output(spec.name, exact_references[spec.name])


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
    parser.add_argument("--workers", type=int, default=cpu_count())
    parser.add_argument("--entry", action="append")
    parser.add_argument("--benchmark", action="append")
    parser.add_argument("--toolchain-report", action="store_true", help=argparse.SUPPRESS)
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

    clean_dirs()
    results: list[Result] = []
    for spec in active_benchmarks:
        for entry in active_entries:
            result, _ = build_and_run(spec, entry, args)
            results.append(result)

    apply_references(results, active_benchmarks)
    cleanup_source_tree()
    REPORT.write_text(render_report(args, active_entries, active_benchmarks, results), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
