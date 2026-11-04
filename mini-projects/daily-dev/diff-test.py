"""Smoke tests for the text diff utility."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory

MODULE_PATH = Path(__file__).with_name("diff.py")
spec = spec_from_file_location("daily_dev_diff", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load diff.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)

NO_NEWLINE_MARKER = "\\ No newline at end of file\n"


def test_reports_added_and_removed_lines() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        first = root / "first.txt"
        second = root / "second.txt"
        first.write_text("alpha\nbeta\n", encoding="utf-8")
        second.write_text("alpha\ngamma\n", encoding="utf-8")

        result = module.diff_files(str(first), str(second))
        assert "-beta\n" in result
        assert "+gamma\n" in result


def test_identical_files_produce_no_diff() -> None:
    with TemporaryDirectory() as directory:
        first = Path(directory) / "first.txt"
        second = Path(directory) / "second.txt"
        first.write_text("same\ncontent\n", encoding="utf-8")
        second.write_text("same\ncontent\n", encoding="utf-8")

        assert module.diff_files(str(first), str(second)) == ""


def test_marks_missing_final_newlines_without_joining_diff_lines() -> None:
    with TemporaryDirectory() as directory:
        first = Path(directory) / "first.txt"
        second = Path(directory) / "second.txt"
        first.write_text("alpha", encoding="utf-8")
        second.write_text("beta", encoding="utf-8")

        result = module.diff_files(str(first), str(second))
        assert f"-alpha\n{NO_NEWLINE_MARKER}" in result
        assert f"+beta\n{NO_NEWLINE_MARKER}" in result


def test_reports_newline_difference() -> None:
    with TemporaryDirectory() as directory:
        first = Path(directory) / "first.txt"
        second = Path(directory) / "second.txt"
        first.write_text("alpha\n", encoding="utf-8")
        second.write_text("alpha", encoding="utf-8")

        result = module.diff_files(str(first), str(second))
        assert "-alpha\n" in result
        assert f"+alpha\n{NO_NEWLINE_MARKER}" in result


test_reports_added_and_removed_lines()
test_identical_files_produce_no_diff()
test_marks_missing_final_newlines_without_joining_diff_lines()
test_reports_newline_difference()
print("diff.py smoke tests passed")
