"""Calculate the percentage change between two numeric values."""

import math


def percent_change(old: float, new: float) -> float:
    """Return the percentage change from old to new.

    Raises:
        ValueError: If inputs are non-finite, the starting value is zero,
            or the result is outside the supported float range.
    """
    if not math.isfinite(old) or not math.isfinite(new):
        raise ValueError("old and new values must be finite numbers")
    if old == 0:
        raise ValueError("old value must not be zero")
    scale = abs(old)
    if (old < 0 != new < 0):
        # Opposite-sign subtraction can overflow even when the ratio is small.
        relative_change = new / scale - old / scale
    else:
        # Same-sign subtraction cannot exceed the magnitude of either input.
        relative_change = (new - old) / scale

    result = relative_change * 100
    if not math.isfinite(result):
        raise ValueError("percentage change is outside the supported float range")
    return result


if __name__ == "__main__":
    old = float(input("Original value: "))
    new = float(input("New value: "))
    try:
        print(f"Percentage change: {percent_change(old, new):.2f}%")
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}")
