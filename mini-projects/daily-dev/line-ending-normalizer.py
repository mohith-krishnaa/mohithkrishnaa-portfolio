"""Normalize line endings in a UTF-8 text file."""

from pathlib import Path
import argparse


def normalize_line_endings(text: str, newline: str = "\n") -> str:
    """Replace CRLF and lone CR endings with the requested newline."""
    if newline not in ("\n", "\r\n"):
        raise ValueError("newline must be '\\n' or '\\r\\n'")
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", newline)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="UTF-8 text file to normalize")
    parser.add_argument("--crlf", action="store_true", help="use Windows CRLF endings")
    parser.add_argument("--in-place", action="store_true", help="overwrite the input file")
    args = parser.parse_args()

    try:
        original = args.file.read_text(encoding="utf-8", newline="")
    except TypeError:
        # Path.read_text lacks a newline argument on some supported Python versions.
        with args.file.open("r", encoding="utf-8", newline="") as source:
            original = source.read()
    updated = normalize_line_endings(original, "\r\n" if args.crlf else "\n")
    if args.in_place:
        args.file.write_bytes(updated.encode("utf-8"))
    else:
        print(updated, end="")


if __name__ == "__main__":
    main()
