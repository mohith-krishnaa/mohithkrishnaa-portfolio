"""Convert byte counts to human-readable binary units."""


def humanize_bytes(value: int) -> str:
    if value < 0:
        raise ValueError("Byte count cannot be negative")

    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    if value < 1024:
        return f"{value} B"

    divisor = 1
    for index, unit in enumerate(units[1:], start=1):
        divisor *= 1024
        # Round to hundredths with integer arithmetic to avoid float overflow.
        hundredths, remainder = divmod(value * 100, divisor)
        if remainder * 2 > divisor or (
            remainder * 2 == divisor and hundredths % 2
        ):
            hundredths += 1

        if hundredths < 102_400 or index == len(units) - 1:
            whole, fraction = divmod(hundredths, 100)
            return f"{whole}.{fraction:02d} {unit}"

    raise RuntimeError("Unexpected unit conversion state")


if __name__ == "__main__":
    try:
        value = int(input("Bytes: "))
        print(humanize_bytes(value))
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}")
