"""Smoke tests for temperature conversion and absolute-zero validation."""

from importlib.util import module_from_spec, spec_from_file_location
import math
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("temperature.py")
spec = spec_from_file_location("daily_dev_temperature", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load temperature.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)

assert module.celsius_to_fahrenheit(0) == 32
assert module.fahrenheit_to_celsius(212) == 100
assert module.celsius_to_kelvin(0) == 273.15
assert module.kelvin_to_celsius(273.15) == 0

assert math.isclose(module.celsius_to_fahrenheit(-273.15), -459.67)
assert module.celsius_to_kelvin(-273.15) == 0
assert math.isclose(module.fahrenheit_to_celsius(-459.67), -273.15)
assert module.kelvin_to_celsius(0) == -273.15

invalid_inputs = (
    (module.celsius_to_fahrenheit, -273.150001),
    (module.celsius_to_kelvin, -273.150001),
    (module.fahrenheit_to_celsius, -459.670001),
    (module.kelvin_to_celsius, -0.001),
)

for convert, value in invalid_inputs:
    try:
        convert(value)
    except ValueError:
        pass
    else:
        raise AssertionError(
            f"{convert.__name__} should reject {value} below absolute zero"
        )

converters = (
    module.celsius_to_fahrenheit,
    module.fahrenheit_to_celsius,
    module.celsius_to_kelvin,
    module.kelvin_to_celsius,
)
for convert in converters:
    for value in (float("nan"), float("inf"), float("-inf")):
        try:
            convert(value)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"{convert.__name__} should reject non-finite input {value}"
            )

print("temperature.py smoke tests passed")
