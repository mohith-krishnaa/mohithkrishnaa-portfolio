"""Smoke tests for percent-change.py."""

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("percent-change.py")
spec = importlib.util.spec_from_file_location("percent_change", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


assert module.percent_change(100, 110) == 10.0
assert module.percent_change(100, 90) == -10.0
assert module.percent_change(-100, -110) == -10.0

try:
    module.percent_change(0, 10)
except ValueError:
    pass
else:
    raise AssertionError("zero starting value should raise ValueError")

for non_finite in (float("nan"), float("inf"), float("-inf")):
    for old, new in ((non_finite, 10), (10, non_finite)):
        try:
            module.percent_change(old, new)
        except ValueError:
            pass
        else:
            raise AssertionError("non-finite values should raise ValueError")

print("percent-change tests passed")
