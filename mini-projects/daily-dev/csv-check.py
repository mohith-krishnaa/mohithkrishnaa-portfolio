"""Check CSV row widths and summarize a CSV file or standard input."""

import argparse
import csv
from pathlib import Path
import sys
from typing import TextIO


SAMPLE_LIMIT = 5


def inspect_csv(stream: TextIO, has_header: bool = True):
    """Return header, column count, data-row count, and width mismatches."""
    reader = csv.reader(stream, strict=True)
    header = None
    column_count = None
    data_rows = 0
    mismatch_count = 0
    mismatch_examples = []

    for row in reader:
        if not row:
            continue

        if column_count is None:
            column_count = len(row)
            if has_header:
                header = row
                continue

        data_rows += 1
        if len(row) != column_count:
            mismatch_count += 1
            if len(mismatch_examples) < SAMPLE_LIMIT:
                mismatch_examples.append((reader.line_num, len(row)))

    return header, column_count or 0, data_rows, mismatch_count, mismatch_examples


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        metavar="FILE",
        help="CSV file to check; omit or use '-' to read standard input",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="treat the first non-empty row as data instead of a header",
    )
    args = parser.parse_args(argv)

    try:
        if args.file == "-":
            report = inspect_csv(sys.stdin, has_header=not args.no_header)
        else:
            with Path(args.file).open(
                "r", encoding="utf-8-sig", newline=""
            ) as source:
                report = inspect_csv(source, has_header=not args.no_header)
    except (OSError, UnicodeError, csv.Error) as error:
        print(f"csv-check: {error}", file=sys.stderr)
        return 1

    header, column_count, data_rows, mismatch_count, examples = report
    print(f"Rows: {data_rows}")
    print(f"Columns: {column_count}")
    if header is not None:
        print(f"Header: {header!r}")

    if mismatch_count:
        print(f"Inconsistent rows: {mismatch_count}")
        for line_number, actual_count in examples:
            print(
                f"  line {line_number}: expected {column_count} fields, "
                f"got {actual_count}"
            )
        remaining = mismatch_count - len(examples)
        if remaining:
            print(f"  ... {remaining} more")
        return 1

    print("CSV structure is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
