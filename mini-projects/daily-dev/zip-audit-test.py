"""Smoke tests for the ZIP archive path auditor."""

from pathlib import Path
import runpy
import stat
import subprocess
import sys
import tempfile
import zipfile


SCRIPT_PATH = Path(__file__).with_name("zip-audit.py")
MODULE = runpy.run_path(SCRIPT_PATH)
audit_archive = MODULE["audit_archive"]


def make_archive(path: Path, entries: list[tuple[str, str]]) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in entries:
            archive.writestr(name, content)


def test_safe_nested_archive() -> None:
    with tempfile.TemporaryDirectory() as directory:
        archive_path = Path(directory) / "safe.zip"
        make_archive(
            archive_path,
            [("docs/readme.txt", "hello"), ("assets/icon.svg", "<svg />")],
        )
        count, issues = audit_archive(archive_path)
    assert count == 2
    assert issues == []


def test_detects_posix_traversal_and_absolute_paths() -> None:
    with tempfile.TemporaryDirectory() as directory:
        archive_path = Path(directory) / "unsafe.zip"
        make_archive(archive_path, [("../escape.txt", "x"), ("/absolute.txt", "x")])
        _, issues = audit_archive(archive_path)
    assert issues == [
        ("../escape.txt", "parent-directory traversal"),
        ("/absolute.txt", "absolute path"),
    ]


def test_detects_windows_paths_and_backslash_traversal() -> None:
    with tempfile.TemporaryDirectory() as directory:
        archive_path = Path(directory) / "windows.zip"
        make_archive(
            archive_path,
            [(r"C:\outside.txt", "x"), (r"folder\..\escape.txt", "x")],
        )
        _, issues = audit_archive(archive_path)
    assert issues == [
        (r"C:\outside.txt", "Windows drive-qualified path"),
        (r"folder\..\escape.txt", "parent-directory traversal"),
    ]


def test_detects_symbolic_link_entries() -> None:
    with tempfile.TemporaryDirectory() as directory:
        archive_path = Path(directory) / "symlink.zip"
        link = zipfile.ZipInfo("shortcut")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr(link, "../../outside.txt")
        _, issues = audit_archive(archive_path)
    assert issues == [("shortcut", "symbolic link")]


def test_detects_duplicate_normalized_destinations() -> None:
    with tempfile.TemporaryDirectory() as directory:
        archive_path = Path(directory) / "duplicates.zip"
        make_archive(
            archive_path,
            [("docs//readme.txt", "first"), ("docs/./readme.txt", "second")],
        )
        _, issues = audit_archive(archive_path)
    assert issues == [
        ("docs/./readme.txt", "duplicate normalized destination")
    ]


def test_cli_returns_failure_for_invalid_zip() -> None:
    with tempfile.TemporaryDirectory() as directory:
        archive_path = Path(directory) / "not-a-zip.zip"
        archive_path.write_text("not a zip", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(archive_path)],
            capture_output=True,
            text=True,
            check=False,
        )
    assert result.returncode == 1
    assert "cannot inspect" in result.stderr
    assert "Traceback" not in result.stderr


test_safe_nested_archive()
test_detects_posix_traversal_and_absolute_paths()
test_detects_windows_paths_and_backslash_traversal()
test_detects_symbolic_link_entries()
test_detects_duplicate_normalized_destinations()
test_cli_returns_failure_for_invalid_zip()
print("zip-audit tests passed (6 tests)")
