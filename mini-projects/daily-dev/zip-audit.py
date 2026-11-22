"""Check ZIP archives for paths that can escape or conflict in the extraction directory."""

import argparse
import ntpath
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


def audit_archive(path: Path) -> tuple[int, list[tuple[str, str]]]:
    """Return the entry count and unsafe or colliding member paths found."""
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()

    issues = []
    seen_destinations: dict[str, bool] = {}
    seen_files: set[str] = set()
    required_directories: set[str] = set()

    for entry in entries:
        name = entry.filename
        portable_name = name.replace("\\", "/")
        member_path = PurePosixPath(portable_name)
        drive, _ = ntpath.splitdrive(name)
        mode = entry.external_attr >> 16

        if drive:
            reason = "Windows drive-qualified path"
        elif member_path.is_absolute():
            reason = "absolute path"
        elif ".." in member_path.parts:
            reason = "parent-directory traversal"
        elif stat.S_ISLNK(mode):
            reason = "symbolic link"
        else:
            destination = member_path.as_posix().rstrip("/")
            is_directory = entry.is_dir()

            if destination in seen_destinations:
                if seen_destinations[destination] != is_directory:
                    reason = "file/directory destination collision"
                else:
                    reason = "duplicate normalized destination"
            elif any(
                parent.as_posix() in seen_files
                for parent in member_path.parents
                if parent.as_posix() != "."
            ):
                reason = "file/directory path collision"
            elif not is_directory and destination in required_directories:
                reason = "file/directory path collision"
            else:
                reason = ""

            if not reason:
                seen_destinations[destination] = is_directory
                if not is_directory:
                    seen_files.add(destination)
                required_directories.update(
                    parent.as_posix()
                    for parent in member_path.parents
                    if parent.as_posix() != "."
                )
                continue

            if destination not in seen_destinations:
                seen_destinations[destination] = is_directory
                if not is_directory:
                    seen_files.add(destination)
            required_directories.update(
                parent.as_posix()
                for parent in member_path.parents
                if parent.as_posix() != "."
            )

        issues.append((name, reason))

    return len(entries), issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="ZIP archive to inspect")
    args = parser.parse_args(argv)

    try:
        entry_count, issues = audit_archive(args.archive)
    except (OSError, zipfile.BadZipFile) as error:
        print(f"error: cannot inspect {args.archive}: {error}", file=sys.stderr)
        return 1

    if issues:
        print(f"UNSAFE: found {len(issues)} unsafe entr{'y' if len(issues) == 1 else 'ies'}:")
        for name, reason in issues:
            print(f"- {name!r}: {reason}")
        return 1

    print(f"OK: {entry_count} ZIP entr{'y' if entry_count == 1 else 'ies'}; no unsafe paths found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
