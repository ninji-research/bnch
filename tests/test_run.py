import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import run


def live_sarif_supported_benchmarks() -> tuple[str, ...]:
    manifest = json.loads((run.ENTRY_SPEC_DIR / "sarif" / "entry.json").read_text())
    return tuple(manifest["benchmarks"])


class RunHelpersTest(unittest.TestCase):
    def test_parse_benchmark_spec_rejects_missing_fixture(self) -> None:
        manifest = {
            "id": "demo",
            "order": 1,
            "category": "numeric_compute",
            "input": {"kind": "fixture", "path": "fixtures/does-not-exist.txt"},
            "weight": 1.0,
            "check": "exact",
            "algorithm": "demo",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "output_contract": "exact text",
            "fairness_notes": "demo",
        }
        with self.assertRaisesRegex(ValueError, "missing fixture"):
            run.parse_benchmark_spec("demo", manifest)

    def test_parse_benchmark_spec_rejects_fractional_order(self) -> None:
        manifest = {
            "id": "demo",
            "order": 1.5,
            "category": "numeric_compute",
            "input": {"kind": "args", "value": "10"},
            "weight": 1.0,
            "check": "exact",
            "algorithm": "demo",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "output_contract": "exact text",
            "fairness_notes": "demo",
            "capabilities": ["numeric_compute"],
            "retained_for": "demo benchmark",
        }
        with self.assertRaisesRegex(ValueError, "expected int"):
            run.parse_benchmark_spec("demo", manifest)

    def test_parse_benchmark_spec_rejects_duplicate_capabilities(self) -> None:
        manifest = {
            "id": "demo",
            "order": 1,
            "category": "numeric_compute",
            "input": {"kind": "args", "value": "10"},
            "weight": 1.0,
            "check": "exact",
            "algorithm": "demo",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "output_contract": "exact text",
            "fairness_notes": "demo",
            "capabilities": ["numeric_compute", "numeric_compute"],
            "retained_for": "demo benchmark",
        }
        with self.assertRaisesRegex(ValueError, "duplicate capabilities"):
            run.parse_benchmark_spec("demo", manifest)

    def test_parse_entry_variant_rejects_duplicate_required_tools(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate tools"):
            run.parse_entry_variant(
                "demo",
                {},
                {
                    "key": "demo__one",
                    "label": "demo",
                    "compiler": "demo",
                    "backend": "native",
                    "required_tools": ["tool", "tool"],
                },
                0,
                "demo__one",
                "main",
                None,
                "demo-profile",
                ("demo optimization",),
            )

    def test_entry_specs_parse_track_metadata(self) -> None:
        manifest = {
            "language": "demo",
            "track": "experimental",
            "canonical_entry": "demo__stage0",
            "variants": [
                {
                    "key": "demo__stage0",
                    "label": "demo",
                    "compiler": "demo",
                    "backend": "native",
                    "required_tools": ["demo-tool"],
                }
            ],
            "build": {
                "compiler": "demo",
                "profile_label": "demo-profile",
                "low_burden_optimizations": ["demo optimization"],
            },
            "policies": {"threads": 1, "external_deps": False},
        }
        run.entry_specs.cache_clear()
        try:
            with mock.patch.object(
                run,
                "entry_manifest_data",
                return_value=run.ManifestLoadResult(documents={"demo": manifest}, errors=[]),
            ):
                specs = list(run.entry_specs())
        finally:
            run.entry_specs.cache_clear()

        self.assertEqual([entry.track for entry in specs], ["experimental"])
        self.assertEqual([entry.supported_benchmarks for entry in specs], [None])

    def test_entries_exclude_experimental_track_by_default(self) -> None:
        entries = (
            run.EntrySpec(
                key="rust__llvm",
                label="rust",
                language="rust",
                compiler="rustc",
                backend="llvm",
                track="main",
                canonical=True,
                supported_benchmarks=None,
                required_tools=("rustc",),
                build_profile="native",
                optimization_notes=("lto",),
            ),
            run.EntrySpec(
                key="sarif__stage0",
                label="sarif",
                language="sarif",
                compiler="sarifc",
                backend="native",
                track="experimental",
                canonical=True,
                supported_benchmarks=None,
                required_tools=("cargo",),
                build_profile="stage0",
                optimization_notes=("native build",),
            ),
        )
        with mock.patch.object(run, "entry_specs", return_value=entries):
            with mock.patch.object(run, "tool", return_value="/usr/bin/tool"):
                self.assertEqual([entry.key for entry in run.entries()], ["rust__llvm"])
                self.assertEqual(
                    [entry.key for entry in run.entries(include_experimental=True)],
                    ["rust__llvm", "sarif__stage0"],
                )

    def test_canonical_entry_map_excludes_experimental_track(self) -> None:
        entries = (
            run.EntrySpec(
                key="rust__llvm",
                label="rust",
                language="rust",
                compiler="rustc",
                backend="llvm",
                track="main",
                canonical=True,
                supported_benchmarks=None,
                required_tools=("rustc",),
                build_profile="native",
                optimization_notes=("lto",),
            ),
            run.EntrySpec(
                key="sarif__stage0",
                label="sarif",
                language="sarif",
                compiler="sarifc",
                backend="native",
                track="experimental",
                canonical=True,
                supported_benchmarks=None,
                required_tools=("cargo",),
                build_profile="stage0",
                optimization_notes=("native build",),
            ),
        )
        with mock.patch.object(run, "entry_specs", return_value=entries):
            self.assertEqual(run.canonical_entry_map(), {"rust": entries[0]})

    def test_resolve_report_paths_uses_experimental_defaults(self) -> None:
        args = mock.Mock(
            report_path=str(run.DEFAULT_REPORT),
            json_path=str(run.DEFAULT_JSON_REPORT),
            all_entries=False,
            experimental_entries=True,
        )
        report, json_report = run.resolve_report_paths(args)
        self.assertEqual(report, run.DEFAULT_EXPERIMENTAL_REPORT.resolve())
        self.assertEqual(json_report, run.DEFAULT_EXPERIMENTAL_JSON_REPORT.resolve())

    def test_supported_benchmark_names_intersects_entry_constraints(self) -> None:
        entries = [
            run.EntrySpec(
                key="sarif__stage0",
                label="sarif",
                language="sarif",
                compiler="sarifc",
                backend="native",
                track="experimental",
                canonical=True,
                supported_benchmarks=("mandelbrot", "nbody"),
                required_tools=("cargo",),
                build_profile="stage0",
                optimization_notes=("native build",),
            ),
            run.EntrySpec(
                key="rust__llvm",
                label="rust",
                language="rust",
                compiler="rustc",
                backend="llvm",
                track="main",
                canonical=True,
                supported_benchmarks=None,
                required_tools=("rustc",),
                build_profile="native",
                optimization_notes=("lto",),
            ),
        ]
        supported = run.supported_benchmark_names(entries, ["binarytrees", "mandelbrot", "nbody"])
        self.assertEqual(supported, ["mandelbrot", "nbody"])

    def test_resolve_selection_rejects_unsupported_benchmark_for_entry(self) -> None:
        entries = [
            run.EntrySpec(
                key="sarif__stage0",
                label="sarif",
                language="sarif",
                compiler="sarifc",
                backend="native",
                track="experimental",
                canonical=True,
                supported_benchmarks=("mandelbrot",),
                required_tools=("cargo",),
                build_profile="stage0",
                optimization_notes=("native build",),
            )
        ]
        args = mock.Mock(entry=["sarif__stage0"], benchmark=["nbody"])
        with self.assertRaisesRegex(SystemExit, "unsupported benchmark selection"):
            run.resolve_selection(args, entries)

    def test_compare_entry_overlap_adds_target_and_limits_benchmarks(self) -> None:
        entries = [
            run.EntrySpec(
                key="rust__llvm",
                label="rust",
                language="rust",
                compiler="rustc",
                backend="llvm",
                track="main",
                canonical=True,
                supported_benchmarks=None,
                required_tools=("rustc",),
                build_profile="native",
                optimization_notes=("lto",),
            ),
            run.EntrySpec(
                key="sarif__stage0",
                label="sarif",
                language="sarif",
                compiler="sarifc",
                backend="native",
                track="experimental",
                canonical=True,
                supported_benchmarks=("mandelbrot", "nbody"),
                required_tools=("cargo",),
                build_profile="stage0",
                optimization_notes=("native build",),
            ),
        ]
        args = mock.Mock(
            entry=["rust__llvm"],
            benchmark=None,
            compare_entry_overlap="sarif__stage0",
        )
        specs = [
            run.BenchmarkSpec(
                name="mandelbrot",
                category="numeric_compute",
                args=("512",),
                stdin_fixture=None,
                input_label="512",
                weight=1.0,
                check="exact",
                algorithm="demo",
                time_complexity="O(1)",
                space_complexity="O(1)",
                output_contract="exact",
                fairness_notes="demo",
                capabilities=("numeric_compute",),
                retained_for="demo",
            ),
            run.BenchmarkSpec(
                name="nbody",
                category="numeric_compute",
                args=("100",),
                stdin_fixture=None,
                input_label="100",
                weight=1.0,
                check="exact",
                algorithm="demo",
                time_complexity="O(1)",
                space_complexity="O(1)",
                output_contract="exact",
                fairness_notes="demo",
                capabilities=("numeric_compute",),
                retained_for="demo",
            ),
            run.BenchmarkSpec(
                name="revcomp",
                category="text_streaming",
                args=(),
                stdin_fixture=None,
                input_label="fixture",
                weight=1.0,
                check="exact",
                algorithm="demo",
                time_complexity="O(1)",
                space_complexity="O(1)",
                output_contract="exact",
                fairness_notes="demo",
                capabilities=("text_parsing",),
                retained_for="demo",
            ),
        ]
        with mock.patch.object(run, "benchmark_specs", return_value=tuple(specs)):
            selection = run.resolve_selection(args, entries)
        self.assertEqual([entry.key for entry in selection.entries], ["rust__llvm", "sarif__stage0"])
        self.assertEqual([spec.name for spec in selection.benchmarks], ["mandelbrot", "nbody"])

    def test_source_path_supports_sarif_sources(self) -> None:
        entry = run.EntrySpec(
            key="sarif__stage0",
            label="sarif",
            language="sarif",
            compiler="sarifc",
            backend="native",
            track="experimental",
            canonical=True,
            supported_benchmarks=("mandelbrot",),
            required_tools=("cargo", "rustc"),
            build_profile="stage0-native",
            optimization_notes=("native build",),
        )
        self.assertEqual(
            run.source_path("mandelbrot", entry),
            run.SRC / "mandelbrot" / "mandelbrot.sarif",
        )

    def test_source_path_supports_sarif_nbody_sources(self) -> None:
        entry = run.EntrySpec(
            key="sarif__stage0",
            label="sarif",
            language="sarif",
            compiler="sarifc",
            backend="native",
            track="experimental",
            canonical=True,
            supported_benchmarks=("mandelbrot", "nbody"),
            required_tools=("cargo", "rustc"),
            build_profile="stage0-native",
            optimization_notes=("native build",),
        )
        self.assertEqual(run.source_path("nbody", entry), run.SRC / "nbody" / "nbody.sarif")

    def test_source_path_supports_sarif_fasta_sources(self) -> None:
        entry = run.EntrySpec(
            key="sarif__stage0",
            label="sarif",
            language="sarif",
            compiler="sarifc",
            backend="native",
            track="experimental",
            canonical=True,
            supported_benchmarks=("mandelbrot", "fasta", "nbody"),
            required_tools=("cargo", "rustc"),
            build_profile="stage0-native",
            optimization_notes=("native build",),
        )
        self.assertEqual(run.source_path("fasta", entry), run.SRC / "fasta" / "fasta.sarif")

    def test_source_path_supports_sarif_revcomp_sources(self) -> None:
        entry = run.EntrySpec(
            key="sarif__stage0",
            label="sarif",
            language="sarif",
            compiler="sarifc",
            backend="native",
            track="experimental",
            canonical=True,
            supported_benchmarks=("mandelbrot", "fasta", "nbody", "revcomp"),
            required_tools=("cargo",),
            build_profile="stage0",
            optimization_notes=("native build",),
        )
        self.assertEqual(run.source_path("revcomp", entry), run.SRC / "revcomp" / "revcomp.sarif")

    def test_source_path_supports_sarif_spectralnorm_sources(self) -> None:
        entry = run.EntrySpec(
            key="sarif__stage0",
            label="sarif",
            language="sarif",
            compiler="sarifc",
            backend="native",
            track="experimental",
            canonical=True,
            supported_benchmarks=("mandelbrot", "fasta", "nbody", "revcomp", "spectralnorm"),
            required_tools=("cargo",),
            build_profile="stage0",
            optimization_notes=("native build",),
        )
        self.assertEqual(
            run.source_path("spectralnorm", entry),
            run.SRC / "spectralnorm" / "spectralnorm.sarif",
        )

    def test_build_command_prefers_repo_sarifc_binary(self) -> None:
        entry = run.EntrySpec(
            key="sarif__stage0",
            label="sarif",
            language="sarif",
            compiler="sarifc",
            backend="native",
            track="experimental",
            canonical=True,
            supported_benchmarks=("mandelbrot",),
            required_tools=("cargo", "rustc"),
            build_profile="stage0-native",
            optimization_notes=("native build",),
        )
        spec = run.BenchmarkSpec(
            name="mandelbrot",
            category="numeric_compute",
            args=("512",),
            stdin_fixture=None,
            input_label="512",
            weight=1.0,
            check="exact",
            algorithm="demo",
            time_complexity="O(1)",
            space_complexity="O(1)",
            output_contract="exact text",
            fairness_notes="demo",
            capabilities=("numeric_compute",),
            retained_for="demo",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_bin = Path(temp_dir) / "sarifc"
            fake_bin.write_text("", encoding="utf-8")
            fake_bin.chmod(0o755)
            with mock.patch.object(run, "tool", return_value=None):
                with mock.patch.object(run, "sarif_bin_candidates", return_value=(fake_bin,)):
                    command = run.build_command(spec, entry, Path("/tmp/out"), Path("/tmp/build"), 1)
        self.assertEqual(
            command,
            [str(fake_bin), "build", str(run.SRC / "mandelbrot" / "mandelbrot.sarif"), "--print-main", "-o", "/tmp/out"],
        )

    def test_sarifc_driver_command_prefers_repo_checkout_over_installed_tool(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_bin = Path(temp_dir) / "sarifc"
            fake_bin.write_text("", encoding="utf-8")
            fake_bin.chmod(0o755)
            with mock.patch.object(run, "tool", return_value="/usr/bin/sarifc"):
                with mock.patch.object(run, "sarif_bin_candidates", return_value=(fake_bin,)):
                    self.assertEqual(run.sarifc_driver_command(), [str(fake_bin)])

    def test_sarif_repo_candidates_default_to_sibling_checkouts(self) -> None:
        self.assertEqual(run.sarif_repo_candidates()[:2], (Path("/home/user/sarif"), Path("/home/user/sarif-main")))

    def test_sarif_repo_candidates_prefer_env_override(self) -> None:
        with mock.patch.dict(run.os.environ, {"BNCH_SARIF_REPO": "/tmp/custom-sarif"}, clear=False):
            self.assertEqual(run.sarif_repo_candidates()[0], Path("/tmp/custom-sarif"))

    def test_build_command_falls_back_to_cargo_run_for_sarif(self) -> None:
        entry = run.EntrySpec(
            key="sarif__stage0",
            label="sarif",
            language="sarif",
            compiler="sarifc",
            backend="native",
            track="experimental",
            canonical=True,
            supported_benchmarks=("mandelbrot",),
            required_tools=("cargo", "rustc"),
            build_profile="stage0-native",
            optimization_notes=("native build",),
        )
        spec = run.BenchmarkSpec(
            name="mandelbrot",
            category="numeric_compute",
            args=("512",),
            stdin_fixture=None,
            input_label="512",
            weight=1.0,
            check="exact",
            algorithm="demo",
            time_complexity="O(1)",
            space_complexity="O(1)",
            output_contract="exact text",
            fairness_notes="demo",
            capabilities=("numeric_compute",),
            retained_for="demo",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_manifest = Path(temp_dir) / "Cargo.toml"
            fake_manifest.write_text("[workspace]\n", encoding="utf-8")
            with mock.patch.object(
                run,
                "tool",
                side_effect=lambda name: "/usr/bin/fake" if name in {"cargo", "rustc"} else None,
            ):
                with mock.patch.object(run, "sarif_bin_candidates", return_value=(Path(temp_dir) / "missing",)):
                    with mock.patch.object(run, "sarif_manifest_candidates", return_value=(fake_manifest,)):
                        command = run.build_command(spec, entry, Path("/tmp/out"), Path("/tmp/build"), 1)
        self.assertEqual(
            command,
            [
                "cargo",
                "run",
                "--quiet",
                "--manifest-path",
                str(fake_manifest),
                "-p",
                "sarifc",
                "--",
                "build",
                str(run.SRC / "mandelbrot" / "mandelbrot.sarif"),
                "--print-main",
                "-o",
                "/tmp/out",
            ],
        )

    def test_entries_exclude_sarif_when_driver_is_unavailable(self) -> None:
        sarif_entry = run.EntrySpec(
            key="sarif__stage0",
            label="sarif",
            language="sarif",
            compiler="sarifc",
            backend="native",
            track="experimental",
            canonical=True,
            supported_benchmarks=("mandelbrot",),
            required_tools=("cargo", "rustc"),
            build_profile="stage0-native",
            optimization_notes=("native build",),
        )
        with mock.patch.object(run, "entry_specs", return_value=(sarif_entry,)):
            with mock.patch.object(run, "sarifc_driver_command", side_effect=ValueError("missing sarifc")):
                self.assertEqual(run.entries(include_experimental=True), [])

    def test_sarifc_version_or_dash_uses_driver_command(self) -> None:
        with mock.patch.object(run, "sarifc_driver_command", return_value=["/tmp/sarifc"]):
            with mock.patch.object(
                run,
                "sh",
                return_value=mock.Mock(stdout="sarifc 0.1.0\n", stderr=""),
            ):
                self.assertEqual(run.sarifc_version_or_dash(), "sarifc 0.1.0")

    def test_environment_data_includes_sarifc_when_active(self) -> None:
        args = mock.Mock(
            runs=1,
            min_runs=1,
            warmup=0,
            runtime_target=0.0,
            max_relative_spread=0.0,
            build_jobs=1,
            all_entries=False,
            experimental_entries=True,
            cpu_list=None,
        )
        entries = [
            run.EntrySpec(
                key="sarif__stage0",
                label="sarif",
                language="sarif",
                compiler="sarifc",
                backend="native",
                track="experimental",
                canonical=True,
                supported_benchmarks=("mandelbrot",),
                required_tools=("cargo", "rustc"),
                build_profile="stage0-native",
                optimization_notes=("native build",),
            )
        ]
        with mock.patch.object(run, "host_cpu_model", return_value="-"):
            with mock.patch.object(run, "host_memory_gib", return_value="-"):
                with mock.patch.object(run, "cpu_count", return_value=1):
                    with mock.patch.object(run, "memory_measurement", return_value=run.MemoryMeasurement("ru_maxrss", "-")):
                        with mock.patch.object(run, "version_or_dash", return_value="-"):
                            with mock.patch.object(run, "sarifc_version_or_dash", return_value="sarifc 0.1.0"):
                                data = run.environment_data(args, entries, [])
        self.assertEqual(data["tool_versions"]["sarifc"], "sarifc 0.1.0")
        self.assertEqual(data["experimental_entries"], True)
        self.assertEqual(data["selected_benchmarks"], "")

    def test_benchmark_specs_are_manifest_driven(self) -> None:
        specs = list(run.benchmark_specs())
        self.assertEqual(specs[0].name, "binarytrees")
        self.assertEqual(specs[-1].name, "sortuniq")
        self.assertEqual(run.benchmark_map()["revcomp"].check, "fasta_casefold")
        self.assertIn("allocation", run.benchmark_map()["binarytrees"].capabilities)
        self.assertTrue(run.benchmark_map()["binarytrees"].retained_for)

    def test_entry_specs_include_variants_from_manifests(self) -> None:
        specs = [entry for entry in run.entry_specs() if entry.language == "nim"]
        self.assertEqual([entry.key for entry in specs], ["nim__gcc", "nim__clang"])
        self.assertTrue(specs[1].canonical)
        self.assertEqual(specs[1].required_tools, ("nim", "clang"))
        self.assertTrue(specs[1].build_profile)
        self.assertTrue(specs[1].optimization_notes)

    def test_live_sarif_manifest_stays_pinned_to_truthful_benchmark_coverage(self) -> None:
        specs = [entry for entry in run.entry_specs() if entry.language == "sarif"]
        self.assertEqual([entry.key for entry in specs], ["sarif__stage0"])
        self.assertEqual(specs[0].track, "main")
        self.assertEqual(specs[0].supported_benchmarks, live_sarif_supported_benchmarks())

    def test_ensure_consistent_outputs_accepts_equivalent_float_outputs(self) -> None:
        spec = run.benchmark_map()["spectralnorm"]
        status = run.ensure_consistent_outputs(spec, ["1.234567890\n", "1.2345678904\n"])
        self.assertIsNone(status)

    def test_ensure_consistent_outputs_rejects_divergent_outputs(self) -> None:
        spec = run.benchmark_map()["binarytrees"]
        status = run.ensure_consistent_outputs(spec, ["alpha\n", "beta\n"])
        self.assertEqual(status, "output-unstable")

    def test_ensure_consistent_outputs_rejects_invalid_float_output(self) -> None:
        spec = run.benchmark_map()["nbody"]
        status = run.ensure_consistent_outputs(spec, ["not-a-number\n"])
        self.assertEqual(status, "output-invalid")

    def test_validate_report_paths_rejects_same_file(self) -> None:
        path = Path("/tmp/same-report-path")
        with self.assertRaises(SystemExit):
            run.validate_report_paths(path, path)

    def test_validate_report_paths_rejects_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            with self.assertRaises(SystemExit):
                run.validate_report_paths(directory, directory / "report.json")

    def test_atomic_write_replaces_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "report.md"
            run.atomic_write(path, "first")
            run.atomic_write(path, "second")
            self.assertEqual(path.read_text(encoding="utf-8"), "second")

    def test_selected_keys_preserves_order_and_deduplicates(self) -> None:
        values = ["rust__llvm,go__gc", "go__gc", "c__clang"]
        selected = run.selected_keys(values, ["c__clang", "go__gc", "rust__llvm"], "entry")
        self.assertEqual(selected, ["rust__llvm", "go__gc", "c__clang"])

    def test_memory_measurement_resets_cgroup_peak_file(self) -> None:
        run.memory_measurement.cache_clear()
        with tempfile.TemporaryDirectory() as temp_dir:
            cgroup_dir = Path(temp_dir)
            peak_path = cgroup_dir / "memory.peak"
            peak_path.write_text("12345\n", encoding="utf-8")
            with mock.patch("run.current_cgroup_path", return_value=cgroup_dir):
                measurement = run.memory_measurement()
            self.assertEqual(measurement.mode, "cgroupv2-memory.peak")
            self.assertEqual(peak_path.read_text(encoding="utf-8"), "0\n")

    def test_apply_references_updates_all_rows_for_benchmark(self) -> None:
        spec = run.benchmark_map()["binarytrees"]
        ok = run.Result(
            benchmark=spec.name,
            entry="c__clang",
            input_text="20",
            raw_output="alpha\n",
            output_text="-",
            reference_text="-",
            status="ok",
            build_time=1.0,
            exec_time=2.0,
            exec_time_spread=0.0,
            measured_runs=3,
            peak_mem_kib=3,
            bin_size=4,
            binary_path=Path("/tmp/alpha"),
        )
        mismatch = run.Result(
            benchmark=spec.name,
            entry="rust__llvm",
            input_text="20",
            raw_output="beta\n",
            output_text="-",
            reference_text="-",
            status="ok",
            build_time=1.0,
            exec_time=2.0,
            exec_time_spread=0.0,
            measured_runs=3,
            peak_mem_kib=3,
            bin_size=4,
            binary_path=Path("/tmp/beta"),
        )
        failed = run.Result(
            benchmark=spec.name,
            entry="go__gc",
            input_text="20",
            raw_output="",
            output_text="-",
            reference_text="-",
            status="build-fail",
            build_time=0.0,
            exec_time=0.0,
            exec_time_spread=0.0,
            measured_runs=0,
            peak_mem_kib=0,
            bin_size=0,
            binary_path=Path("/tmp/fail"),
        )

        run.apply_references([ok, mismatch, failed], [spec])

        self.assertEqual(ok.status, "ok")
        self.assertEqual(mismatch.status, "mismatch")
        self.assertEqual(ok.reference_text, run.compact_output(spec.name, "alpha"))
        self.assertEqual(failed.reference_text, run.compact_output(spec.name, "alpha"))

    def test_load_manifest_dir_reports_invalid_json_and_non_object_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            invalid_dir = root / "invalid"
            invalid_dir.mkdir()
            (invalid_dir / "spec.json").write_text("{\n", encoding="utf-8")
            list_dir = root / "list"
            list_dir.mkdir()
            (list_dir / "spec.json").write_text('["not", "an", "object"]\n', encoding="utf-8")
            valid_dir = root / "valid"
            valid_dir.mkdir()
            (valid_dir / "spec.json").write_text('{"id":"ok"}\n', encoding="utf-8")

            result = run.load_manifest_dir(root, "spec.json")

        self.assertEqual(result.documents, {"valid": {"id": "ok"}})
        self.assertEqual(len(result.errors), 2)
        self.assertIn("invalid/spec.json: invalid JSON", result.errors[0])
        self.assertIn("list/spec.json: expected top-level object, got list", result.errors[1])

    def test_measured_runtime_uses_median(self) -> None:
        self.assertEqual(run.measured_runtime([0.1, 0.2, 1.5]), 0.2)

    def test_relative_spread_uses_median_scale(self) -> None:
        self.assertAlmostEqual(run.relative_spread([1.0, 1.1, 1.2]), 0.2 / 1.1)

    def test_should_continue_sampling_respects_limits_and_stability(self) -> None:
        self.assertTrue(run.should_continue_sampling([], 2, 5, 0.35, 0.03))
        self.assertTrue(run.should_continue_sampling([0.1], 2, 5, 0.35, 0.03))
        self.assertFalse(run.should_continue_sampling([0.2, 0.2], 2, 5, 0.35, 0.03))
        self.assertTrue(run.should_continue_sampling([0.05, 0.06], 2, 5, 0.35, 0.03))
        self.assertFalse(run.should_continue_sampling([0.1, 0.11, 0.1, 0.1, 0.1], 2, 5, 0.35, 0.03))

    def test_category_benchmark_weights_balance_families(self) -> None:
        specs = list(run.benchmark_specs())
        weights = run.category_benchmark_weights(specs)
        self.assertAlmostEqual(sum(weights.values()), 1.0)
        numeric_weight = sum(weights[spec.name] for spec in specs if spec.category == "numeric_compute")
        text_weight = sum(weights[spec.name] for spec in specs if spec.category == "text_streaming")
        parse_weight = sum(weights[spec.name] for spec in specs if spec.category == "parse_aggregate")
        self.assertAlmostEqual(numeric_weight, 1.0 / len(run.CATEGORY_LABELS))
        self.assertAlmostEqual(text_weight, 1.0 / len(run.CATEGORY_LABELS))
        self.assertAlmostEqual(parse_weight, 1.0 / len(run.CATEGORY_LABELS))

    def test_build_summary_data_tracks_metric_rankings(self) -> None:
        spec = run.benchmark_map()["binarytrees"]
        c = run.Result(
            benchmark=spec.name,
            entry="c__clang",
            input_text="20",
            raw_output="ok\n",
            output_text="ok",
            reference_text="ok",
            status="ok",
            build_time=1.0,
            exec_time=2.0,
            exec_time_spread=0.0,
            measured_runs=2,
            peak_mem_kib=100,
            bin_size=100,
            binary_path=Path("/tmp/c"),
        )
        r = run.Result(
            benchmark=spec.name,
            entry="rust__llvm",
            input_text="20",
            raw_output="ok\n",
            output_text="ok",
            reference_text="ok",
            status="ok",
            build_time=2.0,
            exec_time=1.0,
            exec_time_spread=0.0,
            measured_runs=2,
            peak_mem_kib=200,
            bin_size=200,
            binary_path=Path("/tmp/r"),
        )
        summary = run.build_summary_data([c, r], [spec])
        self.assertEqual(summary.metric_orders["Speed"][0], "rust__llvm")
        self.assertEqual(summary.metric_ranks["Speed"]["rust__llvm"], 1)
        self.assertEqual(summary.metric_orders["Build"][0], "c__clang")

    def test_build_profile_summaries_exposes_named_profiles(self) -> None:
        spec = run.benchmark_map()["binarytrees"]
        result = run.Result(
            benchmark=spec.name,
            entry="c__clang",
            input_text="20",
            raw_output="ok\n",
            output_text="ok",
            reference_text="ok",
            status="ok",
            build_time=1.0,
            exec_time=1.0,
            exec_time_spread=0.0,
            measured_runs=2,
            peak_mem_kib=1,
            bin_size=1,
            binary_path=Path("/tmp/c"),
        )
        profiles = run.build_profile_summaries([result], [spec])
        self.assertEqual(profiles[0].label, "Balanced")
        self.assertIn("Speed First", [profile.label for profile in profiles])

    def test_single_entry_summary_is_marked_non_comparative(self) -> None:
        spec = run.benchmark_map()["binarytrees"]
        result = run.Result(
            benchmark=spec.name,
            entry="c__clang",
            input_text="20",
            raw_output="ok\n",
            output_text="ok",
            reference_text="ok",
            status="ok",
            build_time=1.0,
            exec_time=1.0,
            exec_time_spread=0.0,
            measured_runs=2,
            peak_mem_kib=1,
            bin_size=1,
            binary_path=Path("/tmp/c"),
        )
        summary = run.build_summary_data([result], [spec])
        self.assertFalse(run.comparative_report(summary))
        self.assertIn("non-comparative", run.comparative_report_note(summary))

    def test_benchmark_coverage_rows_include_weights_and_unique_coverage(self) -> None:
        specs = [run.benchmark_map()["binarytrees"], run.benchmark_map()["mandelbrot"]]
        rows = run.benchmark_coverage_rows(specs)
        self.assertEqual(rows[0][0], "binarytrees")
        self.assertEqual(rows[0][2], "1.00")
        self.assertIn("allocation", rows[0][4])
        self.assertIn("allocation", rows[0][5])

    def test_entry_policy_rows_include_build_profiles(self) -> None:
        rows = run.entry_policy_rows([entry for entry in run.entry_specs() if entry.language == "rust"])
        self.assertEqual(rows[0][0], "rust (rustc/llvm)")
        self.assertIn("native", rows[0][1])
        self.assertIn("LTO", rows[0][2])


if __name__ == "__main__":
    unittest.main()
