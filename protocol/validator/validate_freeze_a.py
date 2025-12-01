import argparse
import os

from nb_freeze.validate_a import validate_a


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Validator wrapper for NebulaBunny FREEZE-A packages."
    )
    parser.add_argument(
        "package_dir",
        help="Path to FREEZE-A package directory (e.g. protocol/examples/freeze_a_example).",
    )
    args = parser.parse_args(argv)

    package_dir = os.path.abspath(args.package_dir)
    ok = validate_a(package_dir)

    if ok:
        print("[validator] FREEZE-A package checks passed.")
    else:
        print("[validator] FREEZE-A package checks FAILED.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
