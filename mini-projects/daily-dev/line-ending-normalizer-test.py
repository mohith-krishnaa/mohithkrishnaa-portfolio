"""Smoke tests for line-ending-normalizer.py."""

import importlib.util
from pathlib import Path


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


try:
    module.normalize_line_endings("text", "\r")
except ValueError:
    pass
else:
    raise AssertionError("Unsupported newline style should raise ValueError")

test_normalizes_mixed_line_endings_to_lf()
test_can_emit_crlf_line_endings()
test_empty_text_stays_empty()
print("line-ending-normalizer.py smoke tests passed")
