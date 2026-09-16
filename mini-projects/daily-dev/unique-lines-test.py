"""Smoke tests for unique-lines.py."""

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("unique-lines.py")
spec = importlib.util.spec_from_file_location("unique_lines", MODULE_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f"could not load {MODULE_PATH}")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_removes_duplicates_and_blank_lines() -> None:
    text = "apple\n\nbanana\napple\n  banana  \n"
    assert module.unique_lines(text) == ["apple", "banana"]


def test_preserves_first_seen_order() -> None:
    assert module.unique_lines("c\na\nb\na\nc\n") == ["c", "a", "b"]


def test_empty_input_returns_empty_list() -> None:
    assert module.unique_lines("") == []


assert module.unique_lines("apple\napple\n") == ["apple"]
assert module.unique_lines("c\na\nb\na\nc\n") == ["c", "a", "b"]
assert module.unique_lines("") == []
print("unique-lines tests passed")
