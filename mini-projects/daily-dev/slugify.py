"""Convert text into a URL-friendly slug using only the standard library."""

import re
import sys
import unicodedata


def slugify(text: str) -> str:
    """Return a lowercase, hyphen-separated slug from arbitrary text."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[a-zA-Z0-9]+", ascii_text.lower())
    return "-".join(words)


def main() -> None:
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Text: ")
    print(slugify(text))


if __name__ == "__main__":
    main()
