"""Smoke tests for stats.py."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("stats.py")
spec = spec_from_file_location("stats", MODULE_PATH)
assert spec and spec.loader
module = module_from_spec(spec)
spec.loader.exec_module(module)


summary = module.summarize([1, 2, 2, 4])
assert summary["count"] == 4
assert summary["mean"] == 2.25
assert summary["median"] == 2.0
assert summary["mode"] == [2]
assert summary["minimum"] == 1
assert summary["maximum"] == 4
assert summary["range"] == 3

try:
    module.summarize([])
except ValueError as exc:
    assert str(exc) == "values must not be empty"
else:
    raise AssertionError("summarize([]) should reject empty input")

print("stats smoke tests passed")
