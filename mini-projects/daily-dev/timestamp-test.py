"""Smoke tests for Unix timestamp and ISO 8601 conversion."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("timestamp.py")
spec = spec_from_file_location("daily_dev_timestamp", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load timestamp.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)

assert module.timestamp_to_iso(0) == "1970-01-01T00:00:00+00:00"
assert module.timestamp_to_iso(1_700_000_000) == "2023-11-14T22:13:20+00:00"
assert module.iso_to_timestamp("1970-01-01T00:00:00Z") == 0.0
assert module.iso_to_timestamp("1970-01-01T00:00:01+00:00") == 1.0
assert module.iso_to_timestamp("1970-01-01T00:00:00") == 0.0

print("timestamp.py smoke tests passed")
