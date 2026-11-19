"""Smoke tests for strict JSON parsing and CLI behavior."""

from pathlib import Path
import subprocess
import sys
import tempfile


SCRIPT = Path(__file__).with_name("json-pretty.py")


def run_cli(*args: str, input_text: str | None = None):
    return subprocess.run(
        [sys.executable, "-S", str(SCRIPT), *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_formats_sorted_unicode_json() -> None:
    result = run_cli(input_text='{"b": 1, "a": "café"}')
    assert result.returncode == 0, result.stderr
    assert result.stdout == '{\n  "a": "café",\n  "b": 1\n}\n'
    assert result.stderr == ""


def test_rejects_nonstandard_numeric_constants() -> None:
    for constant in ("NaN", "Infinity", "-Infinity"):
        result = run_cli(input_text='{"value": ' + constant + '}')
        assert result.returncode == 1
        assert result.stdout == ""
        assert f"Non-standard JSON constant: {constant}" in result.stderr


def test_missing_file_returns_clean_read_error() -> None:
    with tempfile.TemporaryDirectory() as directory:
        missing = Path(directory) / "missing.json"
        result = run_cli(str(missing))
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.startswith("Could not read input:")
    assert "Traceback" not in result.stderr


def test_invalid_utf8_file_returns_clean_read_error() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "invalid.json"
        path.write_bytes(b'{"value": "\xff"}')
        result = run_cli(str(path))
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.startswith("Could not read input:")
    assert "Traceback" not in result.stderr


def test_rejects_extra_file_arguments() -> None:
    result = run_cli("first.json", "second.json")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "Usage:" in result.stderr


def test_reports_invalid_json() -> None:
    result = run_cli(input_text='{"value":')
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.startswith("Invalid JSON:")


test_formats_sorted_unicode_json()
test_rejects_nonstandard_numeric_constants()
test_missing_file_returns_clean_read_error()
test_invalid_utf8_file_returns_clean_read_error()
test_rejects_extra_file_arguments()
test_reports_invalid_json()
print("json-pretty.py smoke tests passed")
