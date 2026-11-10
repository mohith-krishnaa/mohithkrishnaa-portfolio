"""Smoke tests for the slugify utility."""

from pathlib import Path
import runpy
import subprocess
import sys


SCRIPT_PATH = Path(__file__).with_name("slugify.py")
MODULE = runpy.run_path(SCRIPT_PATH)
slugify = MODULE["slugify"]


def test_basic_slug() -> None:
    assert slugify("Hello, World!") == "hello-world"


def test_collapses_punctuation_and_whitespace() -> None:
    assert slugify("  Python & Data Science  ") == "python-data-science"


def test_normalizes_accents() -> None:
    assert slugify("Café déjà vu") == "cafe-deja-vu"


def test_empty_input() -> None:
    assert slugify("!!!") == ""


def test_cli_uses_command_line_arguments() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "Mixed", "Case", "123"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == "mixed-case-123\n"


def test_cli_prompts_for_interactive_input() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        input="Hello, Interactive World!\n",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == "Text: hello-interactive-world\n"


if __name__ == "__main__":
    test_basic_slug()
    test_collapses_punctuation_and_whitespace()
    test_normalizes_accents()
    test_empty_input()
    test_cli_uses_command_line_arguments()
    test_cli_prompts_for_interactive_input()
    print("slugify tests passed")
