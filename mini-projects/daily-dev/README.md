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
- `json-pretty.py` — format JSON from a file or stdin.
- `url-checker.py` — validate HTTP and HTTPS URL syntax without making network requests.
- `slugify.py` — convert text into lowercase, hyphen-separated URL slugs.
- `stats.py` — calculate common descriptive statistics for numeric data.
- `temperature.py` — convert temperatures between Celsius, Fahrenheit, and Kelvin.
- `text-stats.py` — report word, line, character, and non-whitespace counts.

## Tests

- `text-stats-test.py` — smoke tests for normal, multiline, and empty text input.

Run the smoke test with:

```bash
python text-stats-test.py
```

## Ideas

- String and text utilities
- Date/time helpers
- JSON tools
- Number and statistics helpers
- Small algorithms
- Developer productivity scripts
- Tiny browser experiments
