"""Convert byte counts to human-readable binary units."""


def humanize_bytes(value: int) -> str:
    if value < 0:
        raise ValueError("Byte count cannot be negative")

    units = ("B", "KiB", "MiB", "GiB", "TiB")
    size = float(value)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024

    raise RuntimeError("Unexpected unit conversion state")


if __name__ == "__main__":
    try:
        value = int(input("Bytes: "))
        print(humanize_bytes(value))
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}")
