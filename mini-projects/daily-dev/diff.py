"""Show a compact line-by-line diff between two text files."""

from difflib import unified_diff
from pathlib import Path
import sys


def diff_files(first: str, second: str) -> str:
    """Return a unified diff between two UTF-8 text files."""
    left = Path(first).read_text(encoding="utf-8").splitlines(keepends=True)
    right = Path(second).read_text(encoding="utf-8").splitlines(keepends=True)
    return "".join(unified_diff(left, right, fromfile=first, tofile=second))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python diff.py <first-file> <second-file>")
    print(diff_files(sys.argv[1], sys.argv[2]), end="")


if __name__ == "__main__":
    main()
