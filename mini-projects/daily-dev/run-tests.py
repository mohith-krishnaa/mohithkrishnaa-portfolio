"""Run every dependency-free smoke test in the Daily Dev collection."""

import argparse
import math
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
DEFAULT_TIMEOUT = 30.0


def parse_timeout(value: str) -> float:
    """Parse a finite, positive per-test timeout in seconds."""
    try:
        seconds = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("timeout must be a number of seconds") from error

    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError(
            "timeout must be a finite number greater than zero"
        )
    return seconds


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--timeout",
        type=parse_timeout,
        default=DEFAULT_TIMEOUT,
        metavar="SECONDS",
        help=f"maximum runtime for each test (default: {DEFAULT_TIMEOUT:g})",
    )
    args = parser.parse_args(argv)

    tests = sorted(ROOT.glob("*-test.py"))
    if not tests:
        print("No smoke tests found.", file=sys.stderr)
        return 1

    failed = []
    for test in tests:
        try:
            result = subprocess.run(
                [sys.executable, str(test)],
                cwd=ROOT,
                timeout=args.timeout,
            )
        except subprocess.TimeoutExpired:
            print(f"[TIMEOUT] {test.name} (>{args.timeout:g}s)")
            failed.append(test.name)
            continue

        status = "PASS" if result.returncode == 0 else "FAIL"
        print(f"[{status}] {test.name}")
        if result.returncode != 0:
            failed.append(test.name)

    if failed:
        print(f"\nFailed tests: {', '.join(failed)}")
        return 1

    print(f"\nAll {len(tests)} smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
