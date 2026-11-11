"""Convert byte counts to human-readable binary units."""


def humanize_bytes(value: int) -> str:
    if value < 0:
        raise ValueError("Byte count cannot be negative")

    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    size = float(value)

    for index, unit in enumerate(units):
        # Promote values that would round up to 1024.00 in the current unit.
        if round(size, 2) < 1024 or index == len(units) - 1:
            return f"{size:.2f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024

    raise RuntimeError("Unexpected unit conversion state")


if __name__ == "__main__":
    try:
        value = int(input("Bytes: "))
        print(humanize_bytes(value))
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}")
