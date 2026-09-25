"""Convert Unix timestamps to and from UTC ISO 8601 strings."""

from datetime import datetime, timezone
import sys


def timestamp_to_iso(timestamp: float) -> str:
    """Return a UTC ISO 8601 string for a Unix timestamp."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def iso_to_timestamp(value: str) -> float:
    """Return a Unix timestamp from an ISO 8601 string."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python timestamp.py <timestamp|ISO-8601>")

    value = " ".join(sys.argv[1:])
    try:
        print(timestamp_to_iso(float(value)))
    except ValueError:
        try:
            print(iso_to_timestamp(value))
        except ValueError as exc:
            raise SystemExit(f"Invalid timestamp or ISO-8601 value: {exc}")


if __name__ == "__main__":
    main()
