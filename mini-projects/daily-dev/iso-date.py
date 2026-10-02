"""Convert an ISO 8601 date to YYYY-MM-DD without external dependencies."""

from datetime import datetime
import sys


def date_only(value: str) -> str:
    """Return the calendar date portion of a valid ISO 8601 datetime."""
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python iso-date.py <ISO-8601-datetime>")
    print(date_only(sys.argv[1]))


if __name__ == "__main__":
    main()
