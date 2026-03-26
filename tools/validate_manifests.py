#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import run

REQUIRED_BENCHMARK_KEYS = {
    "id",
    "order",
    "category",
    "input",
    "weight",
    "check",
    "algorithm",
    "time_complexity",
    "space_complexity",
    "output_contract",
    "fairness_notes",
    "capabilities",
    "retained_for",
    "threads",
    "external_deps",
}
REQUIRED_ENTRY_KEYS = {"language", "canonical_entry", "variants", "build", "policies"}
OPTIONAL_ENTRY_KEYS = {"track", "benchmarks"}
REQUIRED_ENTRY_POLICY_KEYS = {"threads", "external_deps"}
EXPECTED_BENCHMARK_THREADS = 1
EXPECTED_ENTRY_THREADS = 1
EXPECTED_EXTERNAL_DEPS = False


def non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def non_empty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(non_empty_string(item) for item in value)


def has_unique_strings(values: list[object]) -> bool:
    normalized = [item.strip() for item in values if isinstance(item, str)]
    return len(normalized) == len(set(normalized))

def benchmark_specs() -> dict[str, dict[str, object]]:
    return run.benchmark_manifest_data().documents


def entry_specs() -> dict[str, dict[str, object]]:
    return run.entry_manifest_data().documents


def expect_type(path: str, value: object, expected: type) -> str | None:
    if not isinstance(value, expected):
        return f"{path}: expected {expected.__name__}, got {type(value).__name__}"
    return None


def manifest_input(spec: run.BenchmarkSpec) -> dict[str, str]:
    if spec.stdin_fixture is not None:
        return {"kind": "fixture", "path": f"fixtures/{spec.stdin_fixture}"}
    return {"kind": "args", "value": " ".join(spec.args)}


def validate_benchmark_manifest_shape(name: str, manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_BENCHMARK_KEYS - set(manifest))
    if missing:
        errors.append(f"{name}: missing keys {', '.join(missing)}")
    unexpected = sorted(set(manifest) - REQUIRED_BENCHMARK_KEYS)
    if unexpected:
        errors.append(f"{name}: unexpected keys {', '.join(unexpected)}")

    for key in (
        "id",
        "category",
        "check",
        "algorithm",
        "time_complexity",
        "space_complexity",
        "output_contract",
        "fairness_notes",
        "retained_for",
    ):
        if key in manifest:
            if not non_empty_string(manifest[key]):
                errors.append(f"{name}.{key}: expected non-empty string")
    capabilities = manifest.get("capabilities")
    if capabilities is not None:
        if not non_empty_string_list(capabilities):
            errors.append(f"{name}.capabilities: expected non-empty list[str]")
        elif not has_unique_strings(capabilities):
            errors.append(f"{name}.capabilities: duplicate capability names")
    if "order" in manifest:
        if not isinstance(manifest["order"], int) or isinstance(manifest["order"], bool):
            errors.append(f"{name}.order: expected int")
        elif manifest["order"] <= 0:
            errors.append(f"{name}.order: expected positive int")
    if "weight" in manifest:
        weight = manifest["weight"]
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            errors.append(f"{name}.weight: expected int or float")
        elif weight <= 0:
            errors.append(f"{name}.weight: expected positive number")
    if "threads" in manifest:
        error = expect_type(f"{name}.threads", manifest["threads"], int)
        if error:
            errors.append(error)
    if "external_deps" in manifest:
        error = expect_type(f"{name}.external_deps", manifest["external_deps"], bool)
        if error:
            errors.append(error)

    input_spec = manifest.get("input")
    if input_spec is not None:
        error = expect_type(f"{name}.input", input_spec, dict)
        if error:
            errors.append(error)
        else:
            kind = input_spec.get("kind")
            if kind not in {"args", "fixture"}:
                errors.append(f"{name}.input.kind: expected 'args' or 'fixture'")
            if kind == "args" and not non_empty_string(input_spec.get("value")):
                errors.append(f"{name}.input.value: expected non-empty str for args input")
            if kind == "fixture":
                path = input_spec.get("path")
                if not non_empty_string(path):
                    errors.append(f"{name}.input.path: expected non-empty str for fixture input")
                elif not (ROOT / path).exists():
                    errors.append(f"{name}.input.path: missing fixture {path}")

    return errors


def validate_benchmarks() -> list[str]:
    errors: list[str] = []
    manifest_map = benchmark_specs()
    try:
        code_specs = list(run.benchmark_specs())
    except ValueError as exc:
        errors.extend(str(exc).splitlines())
        code_specs = []
    code_map = {spec.name: spec for spec in code_specs}
    canonical_entries = run.canonical_entry_map()

    missing_in_manifest = sorted(set(code_map) - set(manifest_map))
    missing_in_code = sorted(set(manifest_map) - set(code_map))
    if missing_in_manifest:
        errors.append(f"missing benchmark manifests: {', '.join(missing_in_manifest)}")
    if missing_in_code:
        errors.append(f"manifest-only benchmarks: {', '.join(missing_in_code)}")

    for name, spec in code_map.items():
        manifest = manifest_map.get(name)
        if manifest is None:
            continue
        errors.extend(validate_benchmark_manifest_shape(name, manifest))
        if manifest.get("id") != name:
            errors.append(f"{name}: manifest id mismatch")
        if manifest.get("category") != spec.category:
            errors.append(f"{name}: manifest category {manifest.get('category')!r} != code {spec.category!r}")
        if manifest.get("category") not in run.CATEGORY_LABELS:
            errors.append(f"{name}: unknown category {manifest.get('category')!r}")
        if manifest.get("input") != manifest_input(spec):
            errors.append(f"{name}: manifest input {manifest.get('input')!r} != code {manifest_input(spec)!r}")
        if manifest.get("check") != spec.check:
            errors.append(f"{name}: manifest check {manifest.get('check')!r} != code {spec.check!r}")
        if manifest.get("weight") != spec.weight:
            errors.append(f"{name}: manifest weight {manifest.get('weight')!r} != code {spec.weight!r}")
        if manifest.get("algorithm") != spec.algorithm:
            errors.append(f"{name}: manifest algorithm mismatch")
        if manifest.get("time_complexity") != spec.time_complexity:
            errors.append(f"{name}: manifest time_complexity mismatch")
        if manifest.get("space_complexity") != spec.space_complexity:
            errors.append(f"{name}: manifest space_complexity mismatch")
        if manifest.get("output_contract") != spec.output_contract:
            errors.append(f"{name}: manifest output_contract mismatch")
        if manifest.get("fairness_notes") != spec.fairness_notes:
            errors.append(f"{name}: manifest fairness_notes mismatch")
        if tuple(manifest.get("capabilities", [])) != spec.capabilities:
            errors.append(f"{name}: manifest capabilities mismatch")
        if manifest.get("retained_for") != spec.retained_for:
            errors.append(f"{name}: manifest retained_for mismatch")
        if manifest.get("threads") != EXPECTED_BENCHMARK_THREADS:
            errors.append(f"{name}: threads must be {EXPECTED_BENCHMARK_THREADS}")
        if manifest.get("external_deps") is not EXPECTED_EXTERNAL_DEPS:
            errors.append(f"{name}: external_deps must be {EXPECTED_EXTERNAL_DEPS}")
        for language, entry in canonical_entries.items():
            source = run.source_path(name, entry)
            if not source.exists():
                errors.append(f"{name}: missing canonical source for {language} at {source.relative_to(ROOT)}")
    return errors


def validate_entry_manifest_shape(language: str, manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_ENTRY_KEYS - set(manifest))
    if missing:
        errors.append(f"{language}: missing keys {', '.join(missing)}")
    unexpected = sorted(set(manifest) - REQUIRED_ENTRY_KEYS - OPTIONAL_ENTRY_KEYS)
    if unexpected:
        errors.append(f"{language}: unexpected keys {', '.join(unexpected)}")

    for key in ("language", "canonical_entry"):
        if key in manifest:
            if not non_empty_string(manifest[key]):
                errors.append(f"{language}.{key}: expected non-empty string")
    if "track" in manifest:
        if not non_empty_string(manifest["track"]):
            errors.append(f"{language}.track: expected non-empty string")
        elif manifest["track"] not in run.ENTRY_TRACKS:
            errors.append(f"{language}.track: expected one of {sorted(run.ENTRY_TRACKS)!r}")
    if "benchmarks" in manifest:
        benchmarks = manifest.get("benchmarks")
        if not non_empty_string_list(benchmarks):
            errors.append(f"{language}.benchmarks: expected non-empty list[str]")
        elif not has_unique_strings(benchmarks):
            errors.append(f"{language}.benchmarks: duplicate benchmark ids")
        else:
            known = {spec.name for spec in run.benchmark_specs()}
            unknown = sorted(set(benchmarks) - known)
            if unknown:
                errors.append(f"{language}.benchmarks: unknown benchmark ids {', '.join(unknown)}")
    variants = manifest.get("variants")
    if variants is not None:
        error = expect_type(f"{language}.variants", variants, list)
        if error:
            errors.append(error)
        else:
            if not variants:
                errors.append(f"{language}.variants: must not be empty")
            for index, variant in enumerate(variants):
                variant_path = f"{language}.variants[{index}]"
                if not isinstance(variant, dict):
                    errors.append(f"{variant_path}: expected dict")
                    continue
                for key in ("key", "label", "compiler", "backend"):
                    if key not in variant:
                        errors.append(f"{variant_path}: missing key {key}")
                    elif not non_empty_string(variant[key]):
                        errors.append(f"{variant_path}.{key}: expected non-empty string")
                required_tools = variant.get("required_tools")
                if not non_empty_string_list(required_tools):
                    errors.append(f"{variant_path}.required_tools: expected non-empty list")
                elif not has_unique_strings(required_tools):
                    errors.append(f"{variant_path}.required_tools: duplicate tools")
    build = manifest.get("build")
    if build is not None:
        error = expect_type(f"{language}.build", build, dict)
        if error:
            errors.append(error)
        elif not build:
            errors.append(f"{language}.build: must not be empty")
        else:
            profile_label = build.get("profile_label")
            if not non_empty_string(profile_label):
                errors.append(f"{language}.build.profile_label: expected non-empty string")
            low_burden = build.get("low_burden_optimizations")
            if not non_empty_string_list(low_burden):
                errors.append(f"{language}.build.low_burden_optimizations: expected non-empty list")
            elif not has_unique_strings(low_burden):
                errors.append(f"{language}.build.low_burden_optimizations: duplicate optimizations")
    policies = manifest.get("policies")
    if policies is not None:
        error = expect_type(f"{language}.policies", policies, dict)
        if error:
            errors.append(error)
        else:
            missing_policy_keys = sorted(REQUIRED_ENTRY_POLICY_KEYS - set(policies))
            if missing_policy_keys:
                errors.append(f"{language}: missing policy keys {', '.join(missing_policy_keys)}")
    return errors


def validate_entries() -> list[str]:
    errors: list[str] = []
    manifests = entry_specs()
    try:
        code_entries = list(run.entry_specs())
    except ValueError as exc:
        errors.extend(str(exc).splitlines())
        code_entries = []
    canonical = {entry.language: entry for entry in code_entries if entry.canonical}

    missing_in_manifest = sorted(set(canonical) - set(manifests))
    missing_in_code = sorted(set(manifests) - set(canonical))
    if missing_in_manifest:
        errors.append(f"missing entry manifests: {', '.join(missing_in_manifest)}")
    if missing_in_code:
        errors.append(f"manifest-only entries: {', '.join(missing_in_code)}")

    for language, entry in canonical.items():
        manifest = manifests.get(language)
        if manifest is None:
            continue
        errors.extend(validate_entry_manifest_shape(language, manifest))
        if manifest.get("language") != language:
            errors.append(f"{language}: manifest language mismatch")
        if manifest.get("track", "main") != entry.track:
            errors.append(f"{language}: manifest track {manifest.get('track', 'main')!r} != code {entry.track!r}")
        manifest_benchmarks = manifest.get("benchmarks")
        entry_benchmarks = list(entry.supported_benchmarks) if entry.supported_benchmarks is not None else None
        if manifest_benchmarks != entry_benchmarks:
            errors.append(f"{language}: manifest benchmarks {manifest_benchmarks!r} != code {entry_benchmarks!r}")
        if manifest.get("canonical_entry") != entry.key:
            errors.append(f"{language}: canonical_entry {manifest.get('canonical_entry')!r} != code {entry.key!r}")
        variants = manifest.get("variants")
        if isinstance(variants, list):
            manifest_variant_keys = [variant.get("key") for variant in variants if isinstance(variant, dict)]
            code_variant_keys = [candidate.key for candidate in code_entries if candidate.language == language]
            if manifest_variant_keys != code_variant_keys:
                errors.append(f"{language}: variant key order mismatch")

        build = manifest.get("build")
        if isinstance(build, dict):
            if build.get("strip") is not True:
                errors.append(f"{language}: build.strip must be true")
            compiler = build.get("compiler")
            if not isinstance(compiler, str) or not compiler.strip():
                errors.append(f"{language}: build.compiler must be a non-empty string")
            if not isinstance(build.get("profile_label"), str) or not build.get("profile_label", "").strip():
                errors.append(f"{language}: build.profile_label must be a non-empty string")
            low_burden = build.get("low_burden_optimizations")
            if not isinstance(low_burden, list) or not low_burden:
                errors.append(f"{language}: build.low_burden_optimizations must be a non-empty list")

        policies = manifest.get("policies")
        if isinstance(policies, dict):
            if policies.get("threads") != EXPECTED_ENTRY_THREADS:
                errors.append(f"{language}: policies.threads must be {EXPECTED_ENTRY_THREADS}")
            if policies.get("external_deps") is not EXPECTED_EXTERNAL_DEPS:
                errors.append(f"{language}: policies.external_deps must be {EXPECTED_EXTERNAL_DEPS}")
    return errors


def main() -> int:
    errors = [*validate_benchmarks(), *validate_entries()]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("manifest validation ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
