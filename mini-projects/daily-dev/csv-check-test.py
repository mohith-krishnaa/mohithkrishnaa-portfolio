"""Smoke tests for csv-check.py."""

from pathlib import Path
import subprocess
import sys
import tempfile


SCRIPT = Path(__file__).with_name("csv-check.py")


def run_cli(*args: str, input_text: str | None = None):
    return subprocess.run(
        [sys.executable, "-S", str(SCRIPT), *args],
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def test_valid_quoted_csv_and_multiline_field() -> None:
    content = 'name,notes\nAlice,"hello, world"\nBob,"two\nlines"\n'
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "valid.csv"
        path.write_text(content, encoding="utf-8", newline="")
        result = run_cli(str(path))
    assert result.returncode == 0, result.stderr
    assert "Rows: 2" in result.stdout
    assert "Columns: 2" in result.stdout
    assert "Header: ['name', 'notes']" in result.stdout
    assert "CSV structure is consistent." in result.stdout


def test_reports_inconsistent_row_width() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "uneven.csv"
        path.write_text("name,age\nAlice,20\nBob\n", encoding="utf-8")
        result = run_cli(str(path))
    assert result.returncode == 1
    assert "Inconsistent rows: 1" in result.stdout
    assert "line 3: expected 2 fields, got 1" in result.stdout


def test_no_header_mode_counts_first_row_as_data() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "numbers.csv"
        path.write_text("1,2\n3,4\n5\n", encoding="utf-8")
        result = run_cli("--no-header", str(path))
    assert result.returncode == 1
    assert "Rows: 3" in result.stdout
    assert "Columns: 2" in result.stdout
    assert "Header:" not in result.stdout
    assert "line 3: expected 2 fields, got 1" in result.stdout


def test_strips_utf8_bom_from_file() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "bom.csv"
        path.write_bytes(b"\xef\xbb\xbfname,age\nAlice,20\n")
        result = run_cli(str(path))
    assert result.returncode == 0, result.stderr
    assert "Header: ['name', 'age']" in result.stdout


def test_reads_from_stdin() -> None:
    result = run_cli(input_text="key,value\na,1\nb,2\n")
    assert result.returncode == 0, result.stderr
    assert "Rows: 2" in result.stdout
    assert "Columns: 2" in result.stdout


def test_empty_file_is_valid() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "empty.csv"
        path.write_text("", encoding="utf-8")
        result = run_cli(str(path))
    assert result.returncode == 0, result.stderr
    assert "Rows: 0" in result.stdout
    assert "Columns: 0" in result.stdout


def test_rejects_malformed_quoting() -> None:
    result = run_cli(input_text='"unterminated field\n')
    assert result.returncode == 1
    assert "csv-check:" in result.stderr


test_valid_quoted_csv_and_multiline_field()
test_reports_inconsistent_row_width()
test_no_header_mode_counts_first_row_as_data()
test_strips_utf8_bom_from_file()
test_reads_from_stdin()
test_empty_file_is_valid()
test_rejects_malformed_quoting()
print("csv-check.py smoke tests passed")
