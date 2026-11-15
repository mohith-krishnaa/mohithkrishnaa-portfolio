"""Smoke tests for file-hash.py."""

import hashlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile


MODULE_PATH = Path(__file__).with_name("file-hash.py")
spec = importlib.util.spec_from_file_location("file_hash", MODULE_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f"could not load {MODULE_PATH}")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_hashes_empty_file() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "empty.bin"
        path.write_bytes(b"")
        assert module.sha256_file(path) == hashlib.sha256(b"").hexdigest()


def test_hashes_binary_file_in_chunks() -> None:
    content = bytes(range(256)) * 4097
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "binary.dat"
        path.write_bytes(content)
        assert module.sha256_file(path, chunk_size=127) == hashlib.sha256(content).hexdigest()


def test_stream_hashing_and_chunk_size_validation() -> None:
    content = b"chunked input\x00with binary bytes"
    stream = io.BytesIO(content)
    assert module.sha256_stream(stream, chunk_size=3) == hashlib.sha256(content).hexdigest()

    try:
        module.sha256_stream(io.BytesIO(content), chunk_size=0)
    except ValueError:
        pass
    else:
        raise AssertionError("A zero chunk size must raise ValueError")


def test_cli_hashes_multiple_files() -> None:
    with tempfile.TemporaryDirectory() as directory:
        first = Path(directory) / "first.txt"
        second = Path(directory) / "second.bin"
        first.write_bytes(b"hello\n")
        second.write_bytes(b"\x00\xff\x10")
        result = subprocess.run(
            [sys.executable, "-S", str(MODULE_PATH), str(first), str(second)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert result.stdout.splitlines() == [
            f"{hashlib.sha256(first.read_bytes()).hexdigest()}  {first}",
            f"{hashlib.sha256(second.read_bytes()).hexdigest()}  {second}",
        ]


def test_cli_reads_binary_stdin() -> None:
    content = b"stdin data\x00\xff"
    result = subprocess.run(
        [sys.executable, "-S", str(MODULE_PATH), "-"],
        input=content,
        capture_output=True,
        check=False,
    )
    expected = f"{hashlib.sha256(content).hexdigest()}  -\n".encode()
    assert result.returncode == 0, result.stderr.decode()
    assert result.stdout == expected


def test_cli_reports_missing_files_and_continues() -> None:
    with tempfile.TemporaryDirectory() as directory:
        existing = Path(directory) / "present.txt"
        missing = Path(directory) / "missing.txt"
        existing.write_text("available", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "-S", str(MODULE_PATH), str(missing), str(existing)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 1
        assert result.stdout == (
            f"{hashlib.sha256(b'available').hexdigest()}  {existing}\n"
        )
        assert f"file-hash: {missing}:" in result.stderr


def test_cli_rejects_repeated_stdin_marker() -> None:
    result = subprocess.run(
        [sys.executable, "-S", str(MODULE_PATH), "-", "-"],
        input=b"data",
        capture_output=True,
        text=False,
        check=False,
    )
    assert result.returncode == 2
    assert b"stdin ('-') may be specified only once" in result.stderr


test_hashes_empty_file()
test_hashes_binary_file_in_chunks()
test_stream_hashing_and_chunk_size_validation()
test_cli_hashes_multiple_files()
test_cli_reads_binary_stdin()
test_cli_reports_missing_files_and_continues()
test_cli_rejects_repeated_stdin_marker()
print("file-hash.py smoke tests passed")
