"""Compute SHA-256 checksums for files or standard input."""

import argparse
import hashlib
from pathlib import Path
import sys


CHUNK_SIZE = 1024 * 1024


def sha256_stream(stream, chunk_size: int = CHUNK_SIZE) -> str:
    """Return the SHA-256 hex digest of a binary stream."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    digest = hashlib.sha256()
    while chunk := stream.read(chunk_size):
        digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: Path, chunk_size: int = CHUNK_SIZE) -> str:
    """Hash a file without reading the whole file into memory."""
    with path.open("rb") as source:
        return sha256_stream(source, chunk_size)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="file paths to hash; use '-' once to read binary data from stdin",
    )
    args = parser.parse_args(argv)

    if args.files.count("-") > 1:
        parser.error("stdin ('-') may be specified only once")

    failed = False
    for filename in args.files:
        try:
            if filename == "-":
                checksum = sha256_stream(sys.stdin.buffer)
            else:
                checksum = sha256_file(Path(filename))
        except OSError as error:
            print(f"file-hash: {filename}: {error}", file=sys.stderr)
            failed = True
            continue

        print(f"{checksum}  {filename}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
