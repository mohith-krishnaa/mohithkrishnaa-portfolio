"""Small statistics helpers for numeric data."""

from __future__ import annotations

from math import isfinite
from statistics import mean, median, multimode


def summarize(values: list[float]) -> dict[str, int | float | list[float]]:
    """Return common descriptive statistics for a non-empty list of finite numbers."""
    if not values:
        raise ValueError("values must not be empty")
    if not all(isfinite(value) for value in values):
        raise ValueError("values must all be finite numbers")

    return {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "mode": multimode(values),
        "minimum": min(values),
        "maximum": max(values),
        "range": max(values) - min(values),
    }


if __name__ == "__main__":
    raw = input("Enter numbers separated by spaces: ")
    try:
        numbers = [float(value) for value in raw.split()]
        for name, value in summarize(numbers).items():
            print(f"{name.title()}: {value}")
    except ValueError as exc:
        print(f"Error: {exc}")
