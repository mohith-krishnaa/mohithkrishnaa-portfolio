"""Tiny dependency-free word and character counter."""

import re
import sys


def count_text(text: str) -> dict[str, int]:
    words = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
    return {
        "words": len(words),
        "characters": len(text),
        "characters_no_spaces": sum(not char.isspace() for char in text),
        "lines": 0 if not text else text.count("\n") + 1,
    }


def main() -> None:
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    if not text:
        print("Usage: python word-counter.py <text>")
        return

    for key, value in count_text(text).items():
        print(f"{key.replace('_', ' ').title()}: {value}")


if __name__ == "__main__":
    main()
