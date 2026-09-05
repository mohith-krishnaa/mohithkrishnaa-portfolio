"""Report basic statistics for a piece of text."""

import sys


def text_stats(text: str) -> dict[str, int]:
    words = text.split()
    return {
        "words": len(words),
        "lines": 0 if not text else len(text.splitlines()),
        "characters": len(text),
        "non_whitespace": sum(not char.isspace() for char in text),
    }


def main() -> None:
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    if not text:
        print("Usage: python text-stats.py <text>")
        return

    for name, value in text_stats(text).items():
        print(f"{name.replace('_', ' ').title()}: {value}")


if __name__ == "__main__":
    main()
