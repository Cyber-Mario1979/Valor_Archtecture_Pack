---
id: VALOR-arch-addendum-doc-generation
version: v1.0.1A
date: 2026-01-03
owner: Nexus
editor: VALOR DEV-TASK-FORCE
status: released
dependencies: []
summary: Document generation compliance rules: separate doc objects, token-clean output, no operational footer text, and correct Africa/Cairo timestamps.
acceptance_criteria:
  - Document bodies contain no template tokens or placeholder braces.
  - Documents never contain operational/runtime footer text.
  - All timestamps use dd-mm-yyyy HH:MM Africa/Cairo and are consistent.
---

# Document Generation Compliance Addendum

## 1) Separate objects
- Each document is a separate Canvas object (not embedded in WP Canvas).
- WP Canvas may include a **Documents** index list (references only).

## 2) Token-clean rule (strict)
Final document output MUST NOT contain:
- `{{ ... }}` tokens
- `{}` or `{ }` placeholders
- `<...>` placeholders

If required content is missing:
- leave the value blank, or write `TBD` (plain text), not braces.

## 3) No operational/footer text inside documents
Document bodies must not include runtime/UI lines such as:
- `Mode: ...`, `State: ...`, `Canvas ready`, `Next → ...`, `To commit: ...`, etc.

Operational guidance must remain in chat only.

## 4) Timestamps
- Timestamp format: `dd-mm-yyyy HH:MM Cairo Time (Egypt)`
- Never label a timestamp as UTC unless it is actually UTC.
- If the user provides the current Cairo time during testing, treat it as the session NOW for stamping until updated.
