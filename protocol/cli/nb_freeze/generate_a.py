import argparse
import os
import shutil
import time
from typing import Any, Dict

from .utils import (
    build_five_fingerprint,
    collect_project_files,
    dump_json,
    sha256_file,
)


def build_metadata(project_root: str, package_id: str) -> Dict[str, Any]:
    five_fp = build_five_fingerprint(project_root)
    return {
        "proto_version": "1.0.0",
        "package_type": "FREEZE_A",
        "metadata": {
            "id": package_id,
            "description": "NebulaBunny FREEZE-A demo package",
            "five_fingerprint": five_fp,
        },
    }


def build_manifest_and_hashes(
    project_root: str, files_info, payload_root: str
) -> Dict[str, Any]:
    manifest_files = []
    hashes: Dict[str, Any] = {}

    for item in files_info:
        rel_path = item["rel_path"]
        src = item["full_path"]
        dst = os.path.join(payload_root, rel_path)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

        digest = sha256_file(src)
        hash_key = rel_path  # simple: use relative path as hash key

        manifest_files.append(
            {
                "path": rel_path,
                "role": "result" if "result" in rel_path else "report",
                "hash_key": hash_key,
            }
        )
        hashes[hash_key] = {
            "algorithm": "sha256",
            "value": digest,
        }

    manifest = {"files": manifest_files}
    return {"manifest": manifest, "hashes": hashes}


def generate_a(project_root: str, output_dir: str) -> None:
    project_root = os.path.abspath(project_root)
    output_dir = os.path.abspath(output_dir)

    os.makedirs(output_dir, exist_ok=True)
    payload_root = os.path.join(output_dir, "payload")
    os.makedirs(payload_root, exist_ok=True)

    package_id = f"freeze_a_{int(time.time())}"
    files_info = collect_project_files(project_root)

    if not files_info:
        print("[nb-freeze] WARNING: no known files found in project, FREEZE-A will be very minimal.")

    meta_root = build_metadata(project_root, package_id)
    mh = build_manifest_and_hashes(project_root, files_info, payload_root)

    metadata_path = os.path.join(output_dir, "metadata.json")
    manifest_path = os.path.join(output_dir, "manifest.json")
    hashes_path = os.path.join(output_dir, "hashes.json")

    dump_json(metadata_path, meta_root)
    dump_json(manifest_path, mh["manifest"])
    dump_json(hashes_path, {"hashes": mh["hashes"]})

    print(f"[nb-freeze] FREEZE-A generated at: {output_dir}")
    print(f"[nb-freeze] files: metadata.json, manifest.json, hashes.json, payload/")


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Generate a minimal NebulaBunny FREEZE-A package.")
    parser.add_argument(
        "--project",
        required=True,
        help="Path to the project root (e.g. /home/ubuntu/vnpy_project).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for the FREEZE-A package.",
    )
    args = parser.parse_args(argv)
    generate_a(args.project, args.output)


if __name__ == "__main__":
    main()
