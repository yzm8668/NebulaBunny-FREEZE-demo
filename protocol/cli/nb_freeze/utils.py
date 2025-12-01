import hashlib
import json
import os
import platform
import subprocess
from typing import Any, Dict, List


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp_path, path)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha1_file(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_spec_hash(project_root: str) -> str:
    """
    Compute spec_hash = SHA1(engine_spec.yaml)[:12].
    If engine_spec.yaml is missing, return 'UNKNOWN'.
    """
    spec_path = os.path.join(project_root, "crypt", "core", "spec", "engine_spec.yaml")
    if not os.path.exists(spec_path):
        return "UNKNOWN"
    digest = sha1_file(spec_path)
    return digest[:12]


def compute_code_git_hash(project_root: str) -> str:
    """
    Try to read current git commit hash in the given project root.
    If git is not available or repo is missing, return 'UNKNOWN'.
    """
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8").strip()
    except Exception:
        return "UNKNOWN"


def compute_env_fingerprint() -> str:
    """
    Build a simple, human-readable env fingerprint string.
    Not meant to be cryptographically strong, just stable and descriptive.
    """
    info = {
        "os": platform.platform(),
        "python": platform.python_version(),
        "machine": platform.machine(),
    }
    raw = json.dumps(info, sort_keys=True)
    # Truncate to keep it reasonably short while still unique enough
    return raw[:256]


def build_five_fingerprint(project_root: str) -> Dict[str, Any]:
    """
    Build a minimal five_fingerprint object.

    For now:
    - code_git_hash: from git, or 'UNKNOWN'
    - data_version: left as 'UNKNOWN' (can be wired to your data registry later)
    - spec_hash: SHA1(engine_spec.yaml)[:12] or 'UNKNOWN'
    - random_seed: 0 (placeholder; real runs should inject true seed)
    - env_fingerprint: short JSON dump of environment info
    """
    return {
        "code_git_hash": compute_code_git_hash(project_root),
        "data_version": "UNKNOWN",
        "spec_hash": compute_spec_hash(project_root),
        "random_seed": 0,
        "env_fingerprint": compute_env_fingerprint(),
    }


def collect_project_files(project_root: str) -> List[Dict[str, str]]:
    """
    Minimal file selection for FREEZE-A demo.

    For now we only pick a small set of key JSON files if they exist:
    - crypt/result.json
    - crypt/report.json

    This list可以在后续版本中扩展为更完整的清单。
    """
    candidates = [
        os.path.join("crypt", "result.json"),
        os.path.join("crypt", "report.json"),
    ]
    files: List[Dict[str, str]] = []
    for rel in candidates:
        full = os.path.join(project_root, rel)
        if os.path.exists(full):
            files.append({"rel_path": rel, "full_path": full})
    return files
