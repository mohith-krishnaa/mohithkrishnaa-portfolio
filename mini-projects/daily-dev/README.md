# Daily Dev

A collection of tiny developer utilities and experiments.

The purpose is simple: make small, real improvements regularly instead of creating meaningless commits just to fill the contribution graph.

## Rules

- Keep each change small enough to finish in one sitting.
- Every commit should improve, document, test, or extend something.
- Prefer useful utilities over empty placeholder changes.
- Keep experiments dependency-free when practical.

## Utilities

- `word-counter.py` — count words, characters, and logical lines across LF, CRLF, or CR text.
- `password-generator.py` — generate passwords with the standard library's secure random generator; rejects lengths below four and returns a nonzero CLI status for invalid input.
- `json-pretty.py` — format strict JSON from a file or stdin, rejecting non-standard NaN and infinity constants and reporting file/encoding errors cleanly.
- `url-checker.py` — validate HTTP and HTTPS URLs, including host and port syntax, without making network requests; returns exit code `1` if any URL is invalid and `2` when no URLs are supplied.
- `slugify.py` — convert text into lowercase, hyphen-separated URL slugs.
- `stats.py` — calculate common descriptive statistics for numeric data, rejecting non-finite values.
- `temperature.py` — convert temperatures between Celsius, Fahrenheit, and Kelvin while rejecting values below absolute zero and non-finite inputs.
- `text-stats.py` — report word, line, character, and non-whitespace counts.
- `percent-change.py` — calculate percentage change between two numeric values, rejecting non-finite inputs.
- `unique-lines.py` — remove duplicate and blank lines while preserving first-seen order.
- `bytes.py` — convert byte counts into human-readable binary units.
- `timestamp.py` — convert Unix timestamps to and from UTC ISO 8601 strings.
- `iso-date.py` — normalize ISO 8601 date/time input to a consistent UTC representation.
- `diff.py` — show a compact unified diff between two UTF-8 text files.
- `file-hash.py` — calculate streaming SHA-256 checksums for files or binary stdin.
- `csv-check.py` — inspect CSV headers and row widths, reporting inconsistent records without loading the whole file.
- `env-check.py` — check `.env` assignment syntax and duplicate variable names without displaying values.
- `zip-audit.py` — inspect ZIP member paths for traversal, absolute paths, Windows drive paths, and symlink entries before extraction; it does not scan file contents for malware.
- `run-tests.py` — run every dependency-free smoke test with a 30-second per-test timeout by default; supports a custom `--timeout` in seconds.

## Tests

- `word-counter-test.py` — checks word and character counts, trailing newlines, LF/CRLF/CR line endings, and stdin behavior.
- `json-pretty-test.py` — checks sorted Unicode formatting, non-standard numeric constants, missing files, invalid UTF-8, extra arguments, and CLI error handling.
- `password-generator-test.py` — checks generated password length and required character classes, minimum-length validation, and CLI success/error exit codes.
- `slugify-test.py` — checks punctuation and whitespace handling, accent normalization, empty input, and CLI argument/interactive input behavior.
- `text-stats-test.py` — smoke tests for normal, multiline, and empty text input.
- `stats-test.py` — checks descriptive statistics, empty-input handling, and rejection of NaN and infinite values.
- `percent-change-test.py` — checks positive, negative, zero-start, and non-finite input cases.
- `unique-lines-test.py` — checks duplicate/blank-line removal, order preservation, and CLI stdin behavior.
- `bytes-test.py` — checks byte conversion, fractional units, and negative-input validation.
- `temperature-test.py` — checks standard conversions, absolute-zero boundaries, and rejection of non-finite inputs.
- `timestamp-test.py` — checks Unix/ISO 8601 conversion, timezone offsets, negative fractional timestamps, and rejection of non-finite or out-of-range values.
- `iso-date-test.py` — checks timezone-aware, UTC, and leap-day ISO 8601 input.
- `line-ending-normalizer-test.py` — checks mixed line endings, LF/CRLF output, empty input, and invalid newline styles.
- `diff-test.py` — checks added/removed lines, identical files, and missing final newlines in temporary-file diffs.
- `file-hash-test.py` — checks empty and binary files, chunked hashing, stdin, multiple paths, and file errors.
- `env-check-test.py` — checks comments, `export` assignments, invalid lines, duplicate keys, stdin, UTF-8 BOMs, empty files, and unreadable paths without exposing values.
- `csv-check-test.py` — checks quoted and multiline fields, inconsistent rows, headerless input, UTF-8 BOMs, stdin, empty files, and malformed quoting.
- `url-checker-test.py` — checks supported schemes, missing hosts, whitespace, malformed ports, malformed IPv6 authorities, and CLI exit codes for valid, invalid, and empty input.
- `run-tests-test.py` — checks timeout parsing and verifies that a timed-out test is reported while later tests continue.
- `zip-audit-test.py` — checks safe archives, POSIX and Windows traversal paths, symlink entries, and invalid ZIP handling.

Run all smoke tests from the repository root with:

```bash
python mini-projects/daily-dev/run-tests.py
```

Set a different per-test timeout in seconds:

```bash
python mini-projects/daily-dev/run-tests.py --timeout 60
```

Run an individual smoke test from the repository root with:

```bash
python mini-projects/daily-dev/bytes-test.py
```

Check a CSV file or pipe data through standard input:

```bash
python mini-projects/daily-dev/csv-check.py data.csv
python mini-projects/daily-dev/csv-check.py --no-header data.csv
```

Or run a smoke test from inside the collection directory:

```bash
cd mini-projects/daily-dev
python bytes-test.py
```

Check a `.env` file without printing its values:

```bash
python mini-projects/daily-dev/env-check.py .env
python mini-projects/daily-dev/env-check.py < .env
```

Inspect a ZIP archive before extracting it (this checks member paths, not file contents):

```bash
python mini-projects/daily-dev/zip-audit.py downloads/archive.zip
```

## Ideas

- String and text utilities
- Date/time helpers
- JSON tools
- Number and statistics helpers
- Small algorithms
- Developer productivity scripts
- Tiny browser experiments
