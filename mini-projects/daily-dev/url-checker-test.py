"""Smoke tests for url-checker.py."""

import importlib.util
from pathlib import Path
import subprocess
import sys


MODULE_PATH = Path(__file__).with_name("url-checker.py")
spec = importlib.util.spec_from_file_location("url_checker", MODULE_PATH)
if spec is None or spec.loader is None:
    raise ImportError(f"could not load {MODULE_PATH}")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_accepts_http_and_https_urls() -> None:
    assert module.is_valid_url("https://example.com/path?q=1")
    assert module.is_valid_url("http://localhost:8080/health")


def test_rejects_missing_hosts_and_unsupported_schemes() -> None:
    assert not module.is_valid_url("")
    assert not module.is_valid_url("   ")
    assert not module.is_valid_url("https:///missing-host")
    assert not module.is_valid_url("ftp://example.com")
    assert not module.is_valid_url("/relative/path")


def test_rejects_whitespace_inside_url() -> None:
    assert not module.is_valid_url("https://example.com/a b")


def test_rejects_malformed_or_out_of_range_ports() -> None:
    assert not module.is_valid_url("https://example.com:abc")
    assert not module.is_valid_url("https://example.com:99999")


def test_rejects_malformed_ipv6_authority() -> None:
    assert not module.is_valid_url("http://[::1")


def test_cli_accepts_arguments_and_reports_each_result() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "https://example.com",
            "ftp://example.com",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == [
        "valid: https://example.com",
        "invalid: ftp://example.com",
    ]
    assert result.stderr == ""


def test_cli_reads_urls_from_stdin() -> None:
    result = subprocess.run(
        [sys.executable, str(MODULE_PATH)],
        input="https://example.com\\n\\nhttp://localhost:8080/health\\n",
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == [
        "valid: https://example.com",
        "valid: http://localhost:8080/health",
    ]
    assert result.stderr == ""


test_accepts_http_and_https_urls()
test_rejects_missing_hosts_and_unsupported_schemes()
test_rejects_whitespace_inside_url()
test_rejects_malformed_or_out_of_range_ports()
test_rejects_malformed_ipv6_authority()
test_cli_accepts_arguments_and_reports_each_result()
test_cli_reads_urls_from_stdin()
print("url-checker.py smoke tests passed")
