import argparse
import os

from nb_freeze.validate_b import validate_b


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Validator wrapper for NebulaBunny FREEZE-B packages."
    )
    parser.add_argument(
        "package_dir",
        help="Path to FREEZE-B package directory (e.g. protocol/examples/freeze_b_example).",
    )
    args = parser.parse_args(argv)

    package_dir = os.path.abspath(args.package_dir)
    ok = validate_b(package_dir)

    if ok:
        print("[validator] FREEZE-B package checks passed.")
    else:
        print("[validator] FREEZE-B package checks FAILED.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
