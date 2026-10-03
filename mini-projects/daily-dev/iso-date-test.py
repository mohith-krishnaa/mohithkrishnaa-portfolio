"""Smoke tests for the ISO 8601 date utility."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("iso-date.py")
spec = spec_from_file_location("daily_dev_iso_date", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load iso-date.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)

assert module.date_only("2026-10-03T17:58:22+05:30") == "2026-10-03"
assert module.date_only("2026-10-03T12:28:22Z") == "2026-10-03"
assert module.date_only("2000-02-29") == "2000-02-29"

print("iso-date.py smoke tests passed")
