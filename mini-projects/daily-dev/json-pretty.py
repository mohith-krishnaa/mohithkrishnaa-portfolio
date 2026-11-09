""""Pretty-print JSON from a file or stdin using only the standard library."""

import json
import sys
from pathlib import Path


def _reject_nonstandard_constant(value: str) -> None:
    raise ValueError(f"Non-standard JSON constant: {value}")


def format_json(text: str) -> str:
    data = json.loads(text, parse_constant=_reject_nonstandard_constant)
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True)


def main() -> None:
    if len(sys.argv) > 1:
        text = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    try:
        print(format_json(text))
    except ValueError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
