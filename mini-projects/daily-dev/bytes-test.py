"""Smoke tests for the human-readable byte converter."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("bytes.py")
spec = spec_from_file_location("daily_dev_bytes", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load bytes.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)

assert module.humanize_bytes(0) == "0 B"
assert module.humanize_bytes(1024) == "1.00 KiB"
assert module.humanize_bytes(1024**2) == "1.00 MiB"
assert module.humanize_bytes(1536) == "1.50 KiB"
assert module.humanize_bytes(1_048_575) == "1.00 MiB"
assert module.humanize_bytes(1024**5) == "1.00 PiB"
assert module.humanize_bytes(1024**6) == "1.00 EiB"
assert module.humanize_bytes(1024**7) == "1.00 ZiB"
assert module.humanize_bytes(1024**8) == "1.00 YiB"

try:
    module.humanize_bytes(-1)
except ValueError:
    pass
else:
    raise AssertionError("Negative byte counts should raise ValueError")

print("bytes.py smoke tests passed")
