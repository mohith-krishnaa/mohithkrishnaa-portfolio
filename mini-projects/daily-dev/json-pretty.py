"""Pretty-print strict JSON from a file or stdin using only the standard library."""

import json
import sys
from pathlib import Path


def _reject_nonstandard_constant(value: str) -> None:
    raise ValueError(f"Non-standard JSON constant: {value}")


def format_json(text: str) -> str:
    data = json.loads(text, parse_constant=_reject_nonstandard_constant)
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        print(f"Usage: {Path(sys.argv[0]).name} [FILE]", file=sys.stderr)
        return 2

    try:
        text = Path(args[0]).read_text(encoding="utf-8") if args else sys.stdin.read()
    except (OSError, UnicodeError) as exc:
        print(f"Could not read input: {exc}", file=sys.stderr)
        return 1

    try:
        print(format_json(text))
    except ValueError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
