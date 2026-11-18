"""Smoke tests for env-check.py."""

from pathlib import Path
import subprocess
import sys
import tempfile


SCRIPT = Path(__file__).with_name("env-check.py")


def run_cli(*args: str, input_text: str | None = None):
    return subprocess.run(
        [sys.executable, "-S", str(SCRIPT), *args],
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def test_accepts_comments_export_and_values() -> None:
    content = (
        "# local settings\n"
        "\n"
        "APP_NAME=Daily Dev\n"
        "export API_URL =https://example.com/path?a=b\n"
        "EMPTY_VALUE=\n"
        "TOKEN='do-not-print-this' # inline text remains a value\n"
    )
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / ".env"
        path.write_text(content, encoding="utf-8")
        result = run_cli(str(path))
    assert result.returncode == 0, result.stderr
    assert "Assignments: 4" in result.stdout
    assert "Environment file syntax is consistent." in result.stdout
    assert "do-not-print-this" not in result.stdout


def test_reports_malformed_assignment_and_invalid_key() -> None:
    result = run_cli(input_text="MISSING_EQUALS\nBAD-KEY=value\n")
    assert result.returncode == 1
    assert "line 1: expected KEY=VALUE assignment" in result.stdout
    assert "line 2: invalid variable name" in result.stdout


def test_reports_duplicate_keys_without_values() -> None:
    result = run_cli(input_text="SECRET=first-value\nSECRET=second-value\n")
    assert result.returncode == 1
    assert "duplicate variable 'SECRET' (first defined on line 1)" in result.stdout
    assert "first-value" not in result.stdout
    assert "second-value" not in result.stdout


def test_reads_from_stdin() -> None:
    result = run_cli(input_text="ONE=1\nTWO=2\n")
    assert result.returncode == 0, result.stderr
    assert "Assignments: 2" in result.stdout


def test_strips_utf8_bom_from_file() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / ".env"
        path.write_bytes(b"\xef\xbb\xbfAPP_MODE=dev\n")
        result = run_cli(str(path))
    assert result.returncode == 0, result.stderr
    assert "Assignments: 1" in result.stdout


def test_empty_file_is_valid() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / ".env"
        path.write_text("", encoding="utf-8")
        result = run_cli(str(path))
    assert result.returncode == 0, result.stderr
    assert "Assignments: 0" in result.stdout


def test_missing_file_returns_input_error() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "missing.env"
        result = run_cli(str(path))
    assert result.returncode == 2
    assert "env-check:" in result.stderr


test_accepts_comments_export_and_values()
test_reports_malformed_assignment_and_invalid_key()
test_reports_duplicate_keys_without_values()
test_reads_from_stdin()
test_strips_utf8_bom_from_file()
test_empty_file_is_valid()
test_missing_file_returns_input_error()
print("env-check.py smoke tests passed")
