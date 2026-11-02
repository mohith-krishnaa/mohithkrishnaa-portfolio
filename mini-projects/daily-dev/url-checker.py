"""Check whether URLs are syntactically valid without making network requests."""

import re
import sys
from urllib.parse import urlparse


def is_valid_url(value: str) -> bool:
    candidate = value.strip()
    if not candidate or not re.fullmatch(r"[^\s]+", candidate):
        return False

    try:
        parsed = urlparse(candidate)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return False
        # Accessing .port validates that a supplied port is numeric and in range.
        _ = parsed.port
    except ValueError:
        return False

    return True


def main() -> int:
    values = sys.argv[1:] or [line.strip() for line in sys.stdin if line.strip()]
    if not values:
        print("Usage: python url-checker.py <url> [url ...]", file=sys.stderr)
        return 2

    has_invalid_url = False
    for value in values:
        valid = is_valid_url(value)
        status = "valid" if valid else "invalid"
        print(f"{status}: {value}")
        has_invalid_url = has_invalid_url or not valid

    # Make the CLI useful in shell scripts and CI pipelines.
    return 1 if has_invalid_url else 0


if __name__ == "__main__":
    raise SystemExit(main())
