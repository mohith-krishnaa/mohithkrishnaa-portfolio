"""Smoke tests for strict JSON parsing and CLI behavior."""

import importlib.util
from pathlib import Path
import subprocess
import sys


MODULE_PATH = Path(__file__).with_name("json-pretty.py")
spec = importlib.util.spec_from_file_location("json_pretty", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load json-pretty.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

assert module.format_json('{"b": 1, "a": "café"}') == '{\n  "a": "café",\n  "b": 1\n}'

for constant in ("NaN", "Infinity", "-Infinity"):
    try:
        module.format_json('{"value": ' + constant + '}')
    except ValueError as exc:
        assert constant in str(exc)
    else:
        raise AssertionError(f"{constant} should be rejected as non-standard JSON")

valid = subprocess.run(
    [sys.executable, str(MODULE_PATH)],
    input='{"ok": true}',
    text=True,
    capture_output=True,
    check=False,
)
assert valid.returncode == 0
assert valid.stdout == '{\n  "ok": true\n}\n'
assert valid.stderr == ""

invalid = subprocess.run(
    [sys.executable, str(MODULE_PATH)],
    input='{"value": NaN}',
    text=True,
    capture_output=True,
    check=False,
)
assert invalid.returncode == 1
assert invalid.stdout == ""
assert "Invalid JSON: Non-standard JSON constant: NaN" in invalid.stderr

print("json-pretty.py smoke tests passed")
