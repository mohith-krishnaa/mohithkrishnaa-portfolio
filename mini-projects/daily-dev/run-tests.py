"""Run every dependency-free smoke test in the Daily Dev collection."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def main() -> int:
    tests = sorted(ROOT.glob("*-test.py"))
    if not tests:
        print("No smoke tests found.")
        return 0

    failed = []
    for test in tests:
        result = subprocess.run([sys.executable, str(test)], cwd=ROOT)
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
