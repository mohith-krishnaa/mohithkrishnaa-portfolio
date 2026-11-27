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

def test_extreme_opposite_sign_values_avoid_intermediate_overflow() -> None:
    assert module.percent_change(-1e308, 1e308) == 200.0
    assert module.percent_change(1e308, -1e308) == -200.0
    assert module.percent_change(1e308, 1e308) == 0.0


def test_unrepresentable_percentage_is_rejected() -> None:
    for old, new in ((1e-308, 1e308), (1e-308, -1e308)):
        try:
            module.percent_change(old, new)
        except ValueError as exc:
            assert str(exc) == "percentage change is outside the supported float range"
        else:
            raise AssertionError("unrepresentable result should raise ValueError")


test_extreme_opposite_sign_values_avoid_intermediate_overflow()
test_unrepresentable_percentage_is_rejected()
print("percent-change tests passed")
