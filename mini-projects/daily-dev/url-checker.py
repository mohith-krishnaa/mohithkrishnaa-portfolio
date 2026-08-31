"""Check whether URLs are syntactically valid without making network requests."""

import re
import sys
from urllib.parse import urlparse


def is_valid_url(value: str) -> bool:
    parsed = urlparse(value.strip())
    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.netloc)
        and bool(re.fullmatch(r"[^\s]+", value.strip()))
    )


def main() -> None:
    values = sys.argv[1:] or [line.strip() for line in sys.stdin if line.strip()]
    if not values:
        print("Usage: python url-checker.py <url> [url ...]")
        return

    for value in values:
        status = "valid" if is_valid_url(value) else "invalid"
        print(f"{status}: {value}")


if __name__ == "__main__":
    main()
