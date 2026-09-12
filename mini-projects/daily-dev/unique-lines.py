"""Print unique non-empty lines from text while preserving their order."""

import sys


def unique_lines(text: str) -> list[str]:
    """Return non-empty lines with duplicates removed, keeping first-seen order."""
    seen: set[str] = set()
    result: list[str] = []

    for line in text.splitlines():
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            result.append(line)

    return result


if __name__ == "__main__":
    text = sys.stdin.read()
    for line in unique_lines(text):
        print(line)
