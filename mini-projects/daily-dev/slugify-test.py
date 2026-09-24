"""Smoke tests for the slugify utility."""

from pathlib import Path
import runpy


MODULE = runpy.run_path(Path(__file__).with_name("slugify.py"))
slugify = MODULE["slugify"]


def test_basic_slug() -> None:
    assert slugify("Hello, World!") == "hello-world"


def test_collapses_punctuation_and_whitespace() -> None:
    assert slugify("  Python & Data Science  ") == "python-data-science"


def test_normalizes_accents() -> None:
    assert slugify("Café déjà vu") == "cafe-deja-vu"


def test_empty_input() -> None:
    assert slugify("!!!") == ""


if __name__ == "__main__":
    test_basic_slug()
    test_collapses_punctuation_and_whitespace()
    test_normalizes_accents()
    test_empty_input()
    print("slugify tests passed")
