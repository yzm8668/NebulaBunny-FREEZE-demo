import argparse
import os
from typing import Any, Dict, List

from .utils import load_json


def _check_required_files(package_dir: str, names: List[str], errors: List[str]) -> Dict[str, str]:
    paths: Dict[str, str] = {}
    for name in names:
        p = os.path.join(package_dir, name)
        if not os.path.exists(p):
            errors.append(f"[validate-b] missing required file: {p}")
        else:
            paths[name] = p
    return paths


def validate_b(package_dir: str) -> bool:
    package_dir = os.path.abspath(package_dir)
    errors: List[str] = []

    required_json_files = [
        "metadata.json",
        "drift.json",
        "execution_audit.json",
        "quantile_distribution.json",
        "stress_windows.json",
        "stability_gates.json",
        "manifest.json",
        "hashes.json",
    ]
    paths = _check_required_files(package_dir, required_json_files, errors)

    if errors:
        for e in errors:
            print(e)
        return False

    # Load and do very lightweight structural checks
    metadata = load_json(paths["metadata.json"])
    manifest = load_json(paths["manifest.json"])
    hashes_root = load_json(paths["hashes.json"])

    if metadata.get("package_type") != "FREEZE_B":
        print("[metadata_root] package_type should be 'FREEZE_B'")
        errors.append("package_type mismatch for FREEZE_B")

    ff = metadata.get("metadata", {}).get("five_fingerprint", {})
    for k in ["code_git_hash", "data_version", "spec_hash", "random_seed", "env_fingerprint"]:
        if k not in ff:
            errors.append(f"[five_fingerprint] missing key: {k}")

    if not isinstance(manifest.get("files", []), list):
        errors.append("[manifest] 'files' must be a list")

    hashes = hashes_root.get("hashes", {})
    if not isinstance(hashes, dict):
        errors.append("[hashes] must be an object/dict")

    # Smoke-load the JSON result components just to ensure they are valid JSON
    for name in [
        "drift.json",
        "execution_audit.json",
        "quantile_distribution.json",
        "stress_windows.json",
        "stability_gates.json",
    ]:
        _ = load_json(paths[name])

    if errors:
        print("[nb-freeze] FREEZE-B validation FAILED:")
        for e in errors:
            print("  -", e)
        return False

    print("[nb-freeze] FREEZE-B structure looks OK.")
    print("[nb-freeze] (Note: numeric thresholds and semantics are not checked here.)")
    return True


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Validate a NebulaBunny FREEZE-B package (structure only).")
    parser.add_argument(
        "package_dir",
        help="Path to the FREEZE-B package directory.",
    )
    args = parser.parse_args(argv)
    ok = validate_b(args.package_dir)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
