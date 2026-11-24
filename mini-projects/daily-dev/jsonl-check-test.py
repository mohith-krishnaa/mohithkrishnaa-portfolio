"""Smoke tests for jsonl-check.py."""

from pathlib import Path
import subprocess
import sys
import tempfile


SCRIPT = Path(__file__).with_name("jsonl-check.py")


def run_cli(*args: str, input_text: str | None = None):
    return subprocess.run(
        [sys.executable, "-S", str(SCRIPT), *args],
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def test_accepts_json_values_from_stdin() -> None:
    result = run_cli(input_text='{"id": 1}\n"hello"\n[1, 2]\n')
    assert result.returncode == 0, result.stderr
    assert "Valid records: 3" in result.stdout
    assert "Invalid lines: 0" in result.stdout
    assert "JSON Lines is valid." in result.stdout


def test_reports_blank_and_malformed_lines_with_line_numbers() -> None:
    result = run_cli(input_text='{"ok": true}\n\n{"broken": }\n')
    assert result.returncode == 1
    assert "Valid records: 1" in result.stdout
    assert "Invalid lines: 2" in result.stdout
    assert "line 2:" in result.stdout
    assert "line 3:" in result.stdout


def test_rejects_non_standard_numeric_constants() -> None:
    result = run_cli(input_text='{"value": NaN}\n{"value": Infinity}\n')
    assert result.returncode == 1
    assert "Invalid lines: 2" in result.stdout
    assert "non-standard JSON constant: NaN" in result.stdout
    assert "non-standard JSON constant: Infinity" in result.stdout


def test_reads_file_and_accepts_missing_final_newline() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "records.jsonl"
        path.write_text('{"a": 1}\n{"b": 2}', encoding="utf-8")
        result = run_cli(str(path))
    assert result.returncode == 0, result.stderr
    assert "Valid records: 2" in result.stdout


def test_rejects_utf8_bom() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "bom.jsonl"
        path.write_bytes(b'\xef\xbb\xbf{"a": 1}\n')
        result = run_cli(str(path))
    assert result.returncode == 1
    assert "Invalid lines: 1" in result.stdout


def test_reports_unreadable_utf8_file_without_traceback() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "invalid-utf8.jsonl"
        path.write_bytes(b'{"a": "\xff"}\n')
        result = run_cli(str(path))
    assert result.returncode == 1
    assert "jsonl-check: cannot read" in result.stderr
    assert "Traceback" not in result.stderr


def test_limits_error_examples_without_losing_total_count() -> None:
    result = run_cli(input_text="not-json\n" * 7)
    assert result.returncode == 1
    assert "Invalid lines: 7" in result.stdout
    assert result.stdout.count("  line ") == 5
    assert "... 2 more" in result.stdout


def test_reports_deeply_nested_json_without_crashing() -> None:
    deeply_nested = "[" * 10_000 + "0" + "]" * 10_000
    result = run_cli(input_text=deeply_nested + "\\n{\\"ok\\": true}\\n")
    assert result.returncode == 1
    assert "Valid records: 1" in result.stdout
    assert "Invalid lines: 1" in result.stdout
    assert "line 1:" in result.stdout
    assert "Traceback" not in result.stderr


test_reports_deeply_nested_json_without_crashing()
test_accepts_json_values_from_stdin()
test_reports_blank_and_malformed_lines_with_line_numbers()
test_rejects_non_standard_numeric_constants()
test_reads_file_and_accepts_missing_final_newline()
test_rejects_utf8_bom()
test_reports_unreadable_utf8_file_without_traceback()
test_limits_error_examples_without_losing_total_count()
print("jsonl-check.py smoke tests passed (8 tests)")
