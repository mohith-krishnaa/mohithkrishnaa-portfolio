"""Convert temperatures between Celsius, Fahrenheit, and Kelvin."""

import math


def _validate_temperature(value: float, unit: str, absolute_zero: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{unit} must be finite")
    if value < absolute_zero:
        raise ValueError(f"{unit} cannot be below absolute zero")


def celsius_to_fahrenheit(celsius: float) -> float:
    _validate_temperature(celsius, "Celsius", -273.15)
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    _validate_temperature(fahrenheit, "Fahrenheit", -459.67)
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius: float) -> float:
    _validate_temperature(celsius, "Celsius", -273.15)
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    _validate_temperature(kelvin, "Kelvin", 0)
    return kelvin - 273.15


if __name__ == "__main__":
    value = float(input("Temperature: "))
    unit = input("Unit (C/F/K): ").strip().upper()

    if unit == "C":
        print(f"Fahrenheit: {celsius_to_fahrenheit(value):.2f}")
        print(f"Kelvin: {celsius_to_kelvin(value):.2f}")
    elif unit == "F":
        celsius = fahrenheit_to_celsius(value)
        print(f"Celsius: {celsius:.2f}")
        print(f"Kelvin: {celsius_to_kelvin(celsius):.2f}")
    elif unit == "K":
        celsius = kelvin_to_celsius(value)
        print(f"Celsius: {celsius:.2f}")
        print(f"Fahrenheit: {celsius_to_fahrenheit(celsius):.2f}")
    else:
        raise SystemExit("Unit must be C, F, or K")
