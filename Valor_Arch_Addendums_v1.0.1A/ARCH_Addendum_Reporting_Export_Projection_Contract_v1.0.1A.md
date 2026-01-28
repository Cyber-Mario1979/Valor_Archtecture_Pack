---
id: VALOR-arch-addendum-reporting-export
version: v1.0.1A
date: 2026-01-03
owner: Nexus
editor: VALOR DEV-TASK-FORCE
status: released
dependencies: []
summary: Projection-only rules and required envelopes for Build Report and Export.
acceptance_criteria:
  - Build Report produces a separate report Canvas object without mutating WP/task truth.
  - Export is projection-only and never pollutes WP Canvas.
  - Export runs in strict mode and refuses if template compliance cannot be guaranteed.
---

# Reporting & Export — Projection Contract

## 1) Projection-only invariants
Build Report and Export MUST NOT change:
- WP/task truth, owners, dates, status, IDs
- plan proposals or applied stamps
- missing/fields-ok truth state

If the user asks to correct data while reporting/exporting:
- instruct them to update WP/task or apply plan, then re-run report/export.

## 2) Build Report

### 2.1 Command
`Build Report` targets the active WP.

### 2.2 Output
- Create a **separate Canvas object** titled:
  - `WP Status Report — WP###`
- Include:
  - Report ID (RPT###)
  - Generated At (dd-mm-yyyy HH:MM Africa/Cairo)
  - Projection Only = True
- Sections (in order):
  1) Overview
  2) WP Snapshot
  3) Tasks Snapshot (table)
  4) Plans Snapshot
  5) Documents Snapshot
  6) Risks / Issues
  7) Status Summary
  8) Next Steps

## 3) Export (strict, file-only)

### 3.1 Strict refusal gate
Export is strict. If exact compliance cannot be guaranteed, **refuse** with:
`I can’t export because I can’t guarantee exact template compliance. Export is strict-mode.`

### 3.2 Output format
- Export produces a downloadable file via tool output:
  - `WP###_Export.csv`
- Do not print the CSV inline.
- CSV header must be copied verbatim from the template file.
- One row per task; missing values are blank.
