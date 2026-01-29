# Contributing to VALOR Architecture Pack

Thanks for your interest in contributing.

## Ground Rules

- Always work on `main` (single-branch repo for now).
- Do not commit generated artifacts unless explicitly instructed.
- After any file change, you MUST:
  1. Run `generate_manifest.py`
  2. Run `verify_manifest.py`
  3. Run `smoke_test.py`

Commits that break smoke-test will not be accepted.

## Line Endings

This repo enforces LF via `.gitattributes`.

If you see CRLF warnings:
- Convert to LF
- Re-generate manifest
- Commit both together

## Typical Workflow

1. Edit files
2. Normalize line endings (if needed)
3. Regenerate manifest
4. Run smoke test
5. Commit
6. Push

That’s it.

## CI

Every push runs GitHub Actions smoke-test.
Green = good. Red = fix locally first.
