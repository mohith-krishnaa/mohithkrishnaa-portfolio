"""Smoke tests for secure password generation and CLI failure handling."""

import importlib.util
from pathlib import Path
import string
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "password_generator", ROOT / "password-generator.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def check_password(password: str, length: int) -> None:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    assert len(password) == length
    assert all(char in alphabet for char in password)
    assert any(char.islower() for char in password)
    assert any(char.isupper() for char in password)
    assert any(char.isdigit() for char in password)
    assert any(char in string.punctuation for char in password)


for requested_length in (4, 16, 32):
    for _ in range(5):
        check_password(MODULE.generate_password(requested_length), requested_length)

try:
    MODULE.generate_password(3)
except ValueError as exc:
    assert str(exc) == "Password length must be at least 4"
else:
    raise AssertionError("Expected short passwords to be rejected")

invalid = subprocess.run(
    [sys.executable, str(ROOT / "password-generator.py")],
    input="3\n",
    text=True,
    capture_output=True,
    cwd=ROOT,
)
assert invalid.returncode == 2
assert "Error: Password length must be at least 4" in invalid.stderr

malformed = subprocess.run(
    [sys.executable, str(ROOT / "password-generator.py")],
    input="not-a-number\n",
    text=True,
    capture_output=True,
    cwd=ROOT,
)
assert malformed.returncode == 2
assert "Error:" in malformed.stderr

valid = subprocess.run(
    [sys.executable, str(ROOT / "password-generator.py")],
    input="8\n",
    text=True,
    capture_output=True,
    cwd=ROOT,
)
assert valid.returncode == 0, valid.stderr
check_password(valid.stdout.rsplit(": ", 1)[-1].strip(), 8)

print("password-generator tests passed")
