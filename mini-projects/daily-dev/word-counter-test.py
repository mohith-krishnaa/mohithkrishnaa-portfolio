"""Smoke tests for word-counter.py."""

import importlib.util
from pathlib import Path
import subprocess
import sys


MODULE_PATH = Path(__file__).with_name("word-counter.py")
spec = importlib.util.spec_from_file_location("word_counter", MODULE_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f"could not load {MODULE_PATH}")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_counts_words_characters_and_lines() -> None:
    assert module.count_text("hello world") == {
        "words": 2,
        "characters": 11,
        "characters_no_spaces": 10,
        "lines": 1,
    }


def test_does_not_count_trailing_newline_as_an_extra_line() -> None:
    assert module.count_text("hello\\n")["lines"] == 1
    assert module.count_text("one\\ntwo\\n")["lines"] == 2


def test_counts_cr_and_crlf_line_endings() -> None:
    assert module.count_text("one\\rtwo\\r\\nthree")["lines"] == 3


def test_cli_reads_text_from_stdin() -> None:
    result = subprocess.run(
        [sys.executable, str(MODULE_PATH)],
        input="hello\\n",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.splitlines() == [
        "Words: 1",
        "Characters: 6",
        "Characters No Spaces: 5",
        "Lines: 1",
    ]
    assert result.stderr == ""


test_counts_words_characters_and_lines()
test_does_not_count_trailing_newline_as_an_extra_line()
test_counts_cr_and_crlf_line_endings()
test_cli_reads_text_from_stdin()
print("word-counter.py smoke tests passed")
