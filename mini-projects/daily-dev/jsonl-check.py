"""Validate JSON Lines (NDJSON) from a file or standard input."""

import argparse
import json
from pathlib import Path
import sys
from typing import TextIO


SAMPLE_LIMIT = 5


def reject_constant(value: str) -> None:
    """Reject JavaScript constants that are not part of standard JSON."""
    raise ValueError(f"non-standard JSON constant: {value}")


def inspect_jsonl(stream: TextIO) -> tuple[int, int, list[tuple[int, str]]]:
    """Return valid record count, invalid line count, and up to five examples."""
    records = 0
    invalid_lines = 0
    examples = []

    for line_number, line in enumerate(stream, start=1):
        try:
            json.loads(line, parse_constant=reject_constant)
        except (json.JSONDecodeError, ValueError) as error:
            invalid_lines += 1
            if len(examples) < SAMPLE_LIMIT:
                examples.append((line_number, str(error)))
        else:
            records += 1

    return records, invalid_lines, examples


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        metavar="FILE",
        help="JSON Lines file to check; omit or use '-' to read standard input",
    )
    args = parser.parse_args(argv)

    try:
        if args.file == "-":
            report = inspect_jsonl(sys.stdin)
        else:
            with Path(args.file).open("r", encoding="utf-8", newline="") as source:
                report = inspect_jsonl(source)
    except (OSError, UnicodeError) as error:
        print(f"jsonl-check: cannot read {args.file}: {error}", file=sys.stderr)
        return 1

    records, invalid_lines, examples = report
    print(f"Valid records: {records}")
    print(f"Invalid lines: {invalid_lines}")

    if invalid_lines:
        for line_number, message in examples:
            print(f"  line {line_number}: {message}")
        remaining = invalid_lines - len(examples)
        if remaining:
            print(f"  ... {remaining} more")
        return 1

    print("JSON Lines is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
