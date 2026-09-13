"""Small smoke tests for unique-lines.py."""

from unique_lines import unique_lines


def test_removes_duplicates_and_blank_lines() -> None:
    text = "apple\n\nbanana\napple\n  banana  \n"
    assert unique_lines(text) == ["apple", "banana"]


def test_preserves_first_seen_order() -> None:
    assert unique_lines("c\na\nb\na\nc\n") == ["c", "a", "b"]


def test_empty_input_returns_empty_list() -> None:
    assert unique_lines("") == []
