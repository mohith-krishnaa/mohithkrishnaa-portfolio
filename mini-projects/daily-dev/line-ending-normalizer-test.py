"""Smoke tests for line-ending-normalizer.py."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile


MODULE_PATH = Path(__file__).with_name("line-ending-normalizer.py")
spec = importlib.util.spec_from_file_location("line_ending_normalizer", MODULE_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f"could not load {MODULE_PATH}")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_normalizes_mixed_line_endings_to_lf() -> None:
    assert module.normalize_line_endings("one\r\ntwo\rthree\n") == "one\ntwo\nthree\n"


def test_can_emit_crlf_line_endings() -> None:
    assert module.normalize_line_endings("one\ntwo\rthree", "\r\n") == "one\r\ntwo\r\nthree"


def test_empty_text_stays_empty() -> None:
    assert module.normalize_line_endings("") == ""


def test_rejects_unsupported_newline_style() -> None:
    try:
        module.normalize_line_endings("text", "\r")
    except ValueError:
        pass
    else:
        raise AssertionError("Unsupported newline style should raise ValueError")


def test_cli_in_place_writes_normalized_bytes() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "sample.txt"
        path.write_bytes(b"one\r\ntwo\rthree")
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH), str(path), "--crlf", "--in-place"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert path.read_bytes() == b"one\r\ntwo\r\nthree"
        assert result.stdout == ""


def test_cli_without_in_place_preserves_source_file() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "sample.txt"
        original = b"one\r\ntwo\rthree"
        path.write_bytes(original)
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH), str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert result.stdout == "one\ntwo\nthree"
        assert path.read_bytes() == original


test_normalizes_mixed_line_endings_to_lf()
test_can_emit_crlf_line_endings()
test_empty_text_stays_empty()
test_rejects_unsupported_newline_style()
test_cli_in_place_writes_normalized_bytes()
test_cli_without_in_place_preserves_source_file()
print("line-ending-normalizer.py smoke tests passed")
