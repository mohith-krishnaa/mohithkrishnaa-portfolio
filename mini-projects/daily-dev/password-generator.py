"""Generate a secure random password using Python's standard library."""

import secrets
import string


def generate_password(length: int = 16) -> str:
    if length < 4:
        raise ValueError("Password length must be at least 4")

    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)
        ):
            return password


if __name__ == "__main__":
    try:
        length = int(input("Password length (default 16): ") or 16)
        print(generate_password(length))
    except ValueError as exc:
        print(f"Error: {exc}")
