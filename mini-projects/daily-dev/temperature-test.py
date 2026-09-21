"""Smoke tests for temperature conversion helpers."""

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("temperature.py")
spec = importlib.util.spec_from_file_location("temperature", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


assert module.celsius_to_fahrenheit(0) == 32
assert module.fahrenheit_to_celsius(212) == 100
assert module.celsius_to_kelvin(0) == 273.15
assert module.kelvin_to_celsius(273.15) == 0

try:
    module.kelvin_to_celsius(-0.01)
except ValueError:
    pass
else:
    raise AssertionError("negative Kelvin should raise ValueError")

print("temperature tests passed")
