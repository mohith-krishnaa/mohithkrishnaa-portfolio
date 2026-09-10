"""Calculate the percentage change between two numeric values."""


def percent_change(old: float, new: float) -> float:
    """Return the percentage change from old to new.

    Raises:
        ValueError: If the starting value is zero.
    """
    if old == 0:
        raise ValueError("old value must not be zero")
    return ((new - old) / abs(old)) * 100


if __name__ == "__main__":
    old = float(input("Original value: "))
    new = float(input("New value: "))
    try:
        print(f"Percentage change: {percent_change(old, new):.2f}%")
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}")
