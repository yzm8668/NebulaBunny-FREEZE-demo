import argparse
import os
import subprocess
from typing import List


def list_ots_files(ots_dir: str) -> List[str]:
    if not os.path.isdir(ots_dir):
        return []
    result: List[str] = []
    for name in sorted(os.listdir(ots_dir)):
        if name.endswith(".ots"):
            result.append(os.path.join(ots_dir, name))
    return result


def verify_ots(package_dir: str) -> None:
    ots_dir = os.path.join(package_dir, "ots")
    files = list_ots_files(ots_dir)

    if not files:
        print("[ots-verifier] no OTS evidence found (this is fine for demo packages).")
        return

    print(f"[ots-verifier] found {len(files)} OTS file(s):")
    for path in files:
        print(f"  - {path}")
        try:
            out = subprocess.check_output(
                ["ots", "info", path],
                stderr=subprocess.STDOUT,
            )
            print(out.decode("utf-8", errors="ignore"))
        except FileNotFoundError:
            print("    [warn] 'ots' binary not found in PATH, skipping detailed check.")
        except subprocess.CalledProcessError as exc:
            print("    [warn] ots info failed:")
            print(exc.output.decode("utf-8", errors="ignore"))


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Verify OpenTimestamps (.ots) files inside a FREEZE package."
    )
    parser.add_argument(
        "package_dir",
        help="Path to FREEZE-A/B package directory.",
    )
    args = parser.parse_args(argv)
    verify_ots(os.path.abspath(args.package_dir))


if __name__ == "__main__":
    main()
