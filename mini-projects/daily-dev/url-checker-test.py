"""Smoke tests for url-checker.py."""

import importlib.util
from pathlib import Path


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


test_accepts_http_and_https_urls()
test_rejects_missing_hosts_and_unsupported_schemes()
test_rejects_whitespace_inside_url()
test_rejects_malformed_or_out_of_range_ports()
test_rejects_malformed_ipv6_authority()
print("url-checker.py smoke tests passed")
