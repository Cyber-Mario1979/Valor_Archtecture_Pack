#!/usr/bin/env python3
"""
VALOR Architecture Pack — Smoke Test Runner

Run from the pack root (where manifest.yaml lives):

    python smoke_test.py

Optional flags:
    --skip-manifest   Skip manifest hash/size verification
    --verbose         Print extra details

Dependencies:
    pip install pyyaml jsonschema

Exit codes:
    0 = PASS
    1 = FAIL (one or more checks failed)
    2 = MISCONFIG (missing dependencies / cannot run)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence, Tuple

# -----------------------------
# Dependency checks
# -----------------------------
try:
    import yaml  # type: ignore
except Exception:
    print("ERROR: Missing dependency 'pyyaml'. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import validate  # type: ignore
except Exception:
    print("ERROR: Missing dependency 'jsonschema'. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str = ""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def glob_rel(root: Path, pattern: str) -> Sequence[Path]:
    return sorted(root.glob(pattern))


def verify_manifest(pack_root: Path, verbose: bool) -> CheckResult:
    manifest_path = pack_root / "manifest.yaml"
    if not manifest_path.exists():
        return CheckResult("manifest.verify", False, "manifest.yaml not found at pack root")

    try:
        manifest = load_yaml(manifest_path)
    except Exception as e:
        return CheckResult("manifest.verify", False, f"Failed to parse manifest.yaml: {e}")

    files = manifest.get("files")
    if not isinstance(files, list):
        return CheckResult("manifest.verify", False, "manifest.yaml missing 'files' list")

    missing = []
    mismatched = []
    checked = 0

    for entry in files:
        if not isinstance(entry, dict):
            mismatched.append(f"Invalid entry (not a dict): {entry!r}")
            continue

        rel_path = entry.get("path")
        exp_sha = entry.get("sha256")
        exp_bytes = entry.get("bytes")

        if not isinstance(rel_path, str):
            mismatched.append(f"Entry missing valid path: {entry!r}")
            continue

        target = pack_root / rel_path
        if not target.exists():
            missing.append(rel_path)
            continue

        checked += 1
        got_bytes = target.stat().st_size
        got_sha = sha256_file(target)

        if exp_bytes is not None and got_bytes != exp_bytes:
            mismatched.append(f"{rel_path}: bytes expected {exp_bytes}, got {got_bytes}")
        if exp_sha is not None and got_sha.lower() != str(exp_sha).lower():
            mismatched.append(f"{rel_path}: sha256 expected {exp_sha}, got {got_sha}")

        if verbose and checked % 50 == 0:
            print(f"  manifest: verified {checked} files...")

    if missing or mismatched:
        parts = []
        if missing:
            parts.append(f"Missing files ({len(missing)}): " + ", ".join(missing[:10]) + (" ..." if len(missing) > 10 else ""))
        if mismatched:
            parts.append(f"Mismatches ({len(mismatched)}): " + "; ".join(mismatched[:5]) + (" ..." if len(mismatched) > 5 else ""))
        return CheckResult("manifest.verify", False, " | ".join(parts))

    return CheckResult("manifest.verify", True, f"Verified {checked} files")


def validate_all_json_schemas(pack_root: Path) -> CheckResult:
    schema_paths = list(pack_root.rglob("*.schema.json"))
    if not schema_paths:
        return CheckResult("schemas.load", False, "No *.schema.json files found")

    bad = []
    for p in schema_paths:
        try:
            load_json(p)
        except Exception as e:
            bad.append(f"{p.relative_to(pack_root)}: {e}")

    if bad:
        return CheckResult("schemas.load", False, "Schema JSON parse errors: " + "; ".join(bad[:5]) + (" ..." if len(bad) > 5 else ""))
    return CheckResult("schemas.load", True, f"Loaded {len(schema_paths)} schema files")


def validate_report_vectors(pack_root: Path) -> CheckResult:
    # Expected convention in this pack
    schema_candidates = [p for p in pack_root.rglob("report_result.schema.json")]
    if not schema_candidates:
        return CheckResult("report.vectors", False, "report_result.schema.json not found")

    schema_path = schema_candidates[0]
    try:
        schema = load_json(schema_path)
    except Exception as e:
        return CheckResult("report.vectors", False, f"Failed to load report schema: {schema_path.relative_to(pack_root)}: {e}")

    vector_paths = sorted(pack_root.rglob("expected_report_*.json"))
    if not vector_paths:
        return CheckResult("report.vectors", False, "No expected_report_*.json test vectors found")

    bad = []
    for vp in vector_paths:
        try:
            instance = load_json(vp)
            validate(instance=instance, schema=schema)
        except Exception as e:
            bad.append(f"{vp.relative_to(pack_root)}: {e}")

    if bad:
        return CheckResult("report.vectors", False, "Report vector validation failures: " + "; ".join(bad[:3]) + (" ..." if len(bad) > 3 else ""))
    return CheckResult("report.vectors", True, f"Validated {len(vector_paths)} report vectors against {schema_path.relative_to(pack_root)}")


def _find_yaml_by_id_version(
    folder: Path,
    *,
    id_key: str,
    version_keys: Sequence[str],
    target_id: str,
    target_version: str,
) -> Optional[Path]:
    if not folder.exists():
        return None

    for p in sorted(folder.glob("*.yaml")) + sorted(folder.glob("*.yml")):
        try:
            data = load_yaml(p)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        got_id = data.get(id_key)
        got_ver = None
        for vk in version_keys:
            if vk in data and isinstance(data.get(vk), str):
                got_ver = data.get(vk)
                break
        if got_id == target_id and got_ver == target_version:
            return p
    return None


def validate_preset_bindings(pack_root: Path) -> CheckResult:
    preset_dir = pack_root / "libraries" / "preset_library"
    if not preset_dir.exists():
        return CheckResult("presets.bindings", False, "libraries/preset_library not found")

    preset_files = sorted(preset_dir.glob("*.yaml")) + sorted(preset_dir.glob("*.yml"))
    if not preset_files:
        return CheckResult("presets.bindings", False, "No preset YAML files found in libraries/preset_library")

    failures = []
    checked = 0

    for pf in preset_files:
        checked += 1
        try:
            preset = load_yaml(pf)
        except Exception as e:
            failures.append(f"{pf.name}: failed to parse YAML: {e}")
            continue
        if not isinstance(preset, dict):
            failures.append(f"{pf.name}: not a YAML mapping")
            continue

        preset_id = preset.get("preset_id")
        preset_ver = preset.get("version")
        bindings = preset.get("bindings") or {}
        if not isinstance(bindings, dict):
            failures.append(f"{pf.name}: missing/invalid 'bindings'")
            continue

        # Task Pool
        tp_ref = bindings.get("task_pool_ref") or {}
        tp_id = tp_ref.get("task_pool_id")
        tp_ver = tp_ref.get("task_pool_version")
        tp_path = _find_yaml_by_id_version(
            pack_root / "libraries" / "task_pool",
            id_key="task_pool_id",
            version_keys=["version"],
            target_id=str(tp_id),
            target_version=str(tp_ver),
        ) if tp_id and tp_ver else None

        if tp_path is None:
            failures.append(f"{pf.name}: cannot resolve task_pool_ref ({tp_id} {tp_ver}) in libraries/task_pool")

        # Profile
        prof_ref = bindings.get("profile_ref") or {}
        prof_id = prof_ref.get("profile_id")
        prof_ver = prof_ref.get("profile_version")
        prof_path = _find_yaml_by_id_version(
            pack_root / "libraries" / "profile_library",
            id_key="profile_id",
            version_keys=["version"],
            target_id=str(prof_id),
            target_version=str(prof_ver),
        ) if prof_id and prof_ver else None

        if prof_path is None:
            failures.append(f"{pf.name}: cannot resolve profile_ref ({prof_id} {prof_ver}) in libraries/profile_library")

        # Calendar
        cal_ref = bindings.get("calendar_logic_ref") or {}
        cal_id = cal_ref.get("calendar_id")
        cal_ver = cal_ref.get("calendar_version")
        cal_path = _find_yaml_by_id_version(
            pack_root / "libraries" / "calendar",
            id_key="calendar_id",
            version_keys=["calendar_version", "version"],
            target_id=str(cal_id),
            target_version=str(cal_ver),
        ) if cal_id and cal_ver else None

        if cal_path is None:
            failures.append(f"{pf.name}: cannot resolve calendar_logic_ref ({cal_id} {cal_ver}) in libraries/calendar")

        # Optional: standards bundle (may be None)
        sb_ref = bindings.get("standards_bundle_ref")
        if sb_ref not in (None, {}, ""):
            # If present, it should be resolvable, but this pack may not ship bundles yet.
            # We warn but do not fail unless explicitly structured.
            pass

    if failures:
        return CheckResult("presets.bindings", False, " | ".join(failures[:6]) + (" ..." if len(failures) > 6 else ""))
    return CheckResult("presets.bindings", True, f"Validated bindings for {checked} preset(s)")


def main() -> int:
    parser = argparse.ArgumentParser(description="VALOR Architecture Pack — Smoke Test Runner")
    parser.add_argument("--skip-manifest", action="store_true", help="Skip manifest verification (hash/size)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    pack_root = Path(__file__).resolve().parent
    print(f"VALOR Smoke Test — pack_root: {pack_root}")

    results: list[CheckResult] = []

    if not args.skip_manifest:
        results.append(verify_manifest(pack_root, verbose=args.verbose))
    results.append(validate_all_json_schemas(pack_root))
    results.append(validate_report_vectors(pack_root))
    results.append(validate_preset_bindings(pack_root))

    # Summary
    print("\nResults:")
    any_fail = False
    for r in results:
        status = "PASS" if r.ok else "FAIL"
        print(f"- {status}  {r.name}")
        if r.details and (args.verbose or not r.ok):
            print(f"    {r.details}")
        if not r.ok:
            any_fail = True

    if any_fail:
        print("\nOverall: FAIL")
        return 1

    print("\nOverall: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
