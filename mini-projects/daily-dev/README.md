# Daily Dev

A collection of tiny developer utilities and experiments.

The purpose is simple: make small, real improvements regularly instead of creating meaningless commits just to fill the contribution graph.

## Rules

- Keep each change small enough to finish in one sitting.
- Every commit should improve, document, test, or extend something.
- Prefer useful utilities over empty placeholder changes.
- Keep experiments dependency-free when practical.

## Utilities

- `word-counter.py` — count words, characters, and lines.
- `password-generator.py` — generate passwords with the standard library's secure random generator.
- `json-pretty.py` — format strict JSON from a file or stdin, rejecting non-standard NaN and infinity constants.
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
- `run-tests.py` — run every dependency-free smoke test in the collection.

## Tests

- `json-pretty-test.py` — checks sorted Unicode formatting, rejection of non-standard numeric constants, and CLI success/failure behavior.
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
- `url-checker-test.py` — checks supported schemes, missing hosts, whitespace, malformed ports, malformed IPv6 authorities, and CLI exit codes for valid, invalid, and empty input.

Run all smoke tests from the repository root with:

```bash
python mini-projects/daily-dev/run-tests.py
```

Run an individual smoke test from the repository root with:

```bash
python mini-projects/daily-dev/bytes-test.py
```

Or run it from inside the collection directory:

```bash
cd mini-projects/daily-dev
python bytes-test.py
```

## Ideas

- String and text utilities
- Date/time helpers
- JSON tools
- Number and statistics helpers
- Small algorithms
- Developer productivity scripts
- Tiny browser experiments
