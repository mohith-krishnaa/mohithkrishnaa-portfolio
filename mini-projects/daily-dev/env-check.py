"""Check a .env file for malformed assignments and duplicate variable names."""

import argparse
from pathlib import Path
import re
import sys
from typing import TextIO


KEY_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def inspect_env(stream: TextIO) -> tuple[int, list[tuple[int, str]]]:
    """Return the assignment count and line-numbered syntax issues."""
    seen: dict[str, int] = {}
    assignments = 0
    issues: list[tuple[int, str]] = []

    for line_number, raw_line in enumerate(stream, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()

        if "=" not in line:
            issues.append((line_number, "expected KEY=VALUE assignment"))
            continue

        key, _value = line.split("=", 1)
        key = key.strip()
        if not KEY_PATTERN.fullmatch(key):
            issues.append((line_number, "invalid variable name"))
            continue

        assignments += 1
        if key in seen:
            issues.append(
                (line_number, f"duplicate variable {key!r} (first defined on line {seen[key]})")
            )
        else:
            seen[key] = line_number

    return assignments, issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        metavar="FILE",
        help="environment file to check; omit or use '-' to read standard input",
    )
    args = parser.parse_args(argv)

    try:
        if args.file == "-":
            report = inspect_env(sys.stdin)
        else:
            with Path(args.file).open("r", encoding="utf-8-sig") as source:
                report = inspect_env(source)
    except (OSError, UnicodeError) as error:
        print(f"env-check: {error}", file=sys.stderr)
        return 2

    assignments, issues = report
    print(f"Assignments: {assignments}")
    if issues:
        print(f"Issues: {len(issues)}")
        for line_number, message in issues:
            print(f"  line {line_number}: {message}")
        return 1

    print("Environment file syntax is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
