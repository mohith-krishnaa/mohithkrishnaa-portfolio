"""Smoke tests for run-tests.py timeout handling."""

import argparse
import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch


RUNNER_PATH = Path(__file__).with_name("run-tests.py")
spec = importlib.util.spec_from_file_location("daily_dev_runner", RUNNER_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f"could not load {RUNNER_PATH}")

runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def test_parse_timeout_accepts_positive_finite_values() -> None:
    assert runner.parse_timeout("0.25") == 0.25
    assert runner.parse_timeout("30") == 30.0


def test_parse_timeout_rejects_invalid_values() -> None:
    for value in ("0", "-1", "nan", "inf", "not-a-number"):
        try:
            runner.parse_timeout(value)
        except argparse.ArgumentTypeError:
            continue
        raise AssertionError(f"Invalid timeout was accepted: {value}")


def test_runner_records_timeout_and_continues() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        first = root / "a-slow-test.py"
        second = root / "b-quick-test.py"
        first.touch()
        second.touch()

        calls = []

        def fake_run(command, cwd, timeout):
            calls.append(command[1])
            if command[1] == str(first):
                raise subprocess.TimeoutExpired(command, timeout)
            return subprocess.CompletedProcess(command, 0)

        previous_root = runner.ROOT
        runner.ROOT = root
        output = io.StringIO()
        try:
            with patch.object(runner.subprocess, "run", side_effect=fake_run):
                with redirect_stdout(output):
                    status = runner.main(["--timeout", "0.25"])
        finally:
            runner.ROOT = previous_root

    assert status == 1
    assert calls == [str(first), str(second)]
    assert "[TIMEOUT] a-slow-test.py (>0.25s)" in output.getvalue()
    assert "[PASS] b-quick-test.py" in output.getvalue()
    assert "Failed tests: a-slow-test.py" in output.getvalue()


test_parse_timeout_accepts_positive_finite_values()
test_parse_timeout_rejects_invalid_values()
test_runner_records_timeout_and_continues()
print("run-tests.py smoke tests passed")
