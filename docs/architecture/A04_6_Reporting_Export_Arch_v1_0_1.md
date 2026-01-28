---
id: VALOR-block-A04-6-reporting-export-architecture
block type: Arch
version: v1.0.1
owner: Nexus
editor: Senior Architect
status: released
date: 2025-12-23
dependencies:
  - VALOR-block-A00-specs-architecture-pack
  - VALOR-block-A01-sos-context-capability
  - VALOR-block-A02-principles-invariants
  - VALOR-block-A03-subsystems-authority
  - VALOR-block-A04-2-work-package-architecture
summary: "Block A04.6 — Reporting & Export System Architecture: projection layer that generates audit-grade reports/exports from WP truth, enforces traceability stamps, and provides schema-locked outputs without mutating authoritative data."
acceptance_criteria:
  - Defines Reporting/Export as projection-only with no mutation authority.
  - Defines output artifact types (report, CSV export) and required schema/stamps.
  - Defines traceability stamping rules (preset/profile/task_pool/calendar versions and more).
  - Defines metrics computation policy and calendar-aligned date arithmetic consistency.
  - Defines contract actions, response envelopes, and error semantics.
  - Defines reproducibility/determinism requirements for exports and reports.
---

# Reporting & Export System Architecture

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
Reporting & Export (RPT) is Valor’s **projection and publishing layer** for:
- structured exports (CSV/JSON) for downstream tooling,
- human-readable reports (status, readiness, traceability, metrics),
- audit-grade traceability stamps attached to each artifact.

RPT is authoritative for:
- report/export artifact content and formatting,
- computed metrics derived from WP truth (with declared rules),
- stamping and provenance for outputs.

RPT is not authoritative for:
- WP/task truth (it reads; cannot mutate),
- schedule truth (planning proposals are inputs, not truth),
- standards/templates (unless a report explicitly embeds references by ID/version).

Invariant alignment:
- Projection-only (A02 INV-09)
- Mandatory stamps for regulated outputs (A02 INV-07)

---

## 2. Inputs and Output Types

### 2.1 Canonical Inputs
RPT consumes:
- WP snapshot (WP_GET) including tasks, dependencies, statuses, dates
- session traceability context (stamps)
- optional: plan_id (if a plan proposal is being reported as “proposed”)
- export schema version (for CSV/JSON)

### 2.2 Output Types
1) **Report Artifact**
   - human-readable (Markdown/PDF)
   - focuses on governance and readiness

2) **Export Artifact**
   - schema-locked (CSV baseline)
   - designed for integration with spreadsheets/PM tooling

3) **Traceability Ledger Extract** (optional)
   - list of action IDs, stamps, and versions used across a WP lifecycle

---

## 3. Traceability Stamping (Hard Requirement)

### 3.1 Minimum Required Stamp Set
Every report/export must include:
- preset_id/version
- profile_id/version
- task_pool_id/version
- calendar_logic_version

If any is missing:
- refuse generation with INVARIANT_VIOLATION / MISSING_TRACEABILITY_STAMPS

### 3.2 Recommended Additional Stamps
When available, RPT should also stamp:
- standards_bundle_id/version (if docs/standards referenced)
- template_id/version (if report based on a template)
- planning_logic_version (if reporting plan proposals)
- contract_id/version(s) used in generating the artifact
- architecture_pack_id/version

### 3.3 Stamp Placement
Stamps must appear in:
- the report header (document control)
- the export header row or metadata section (for CSV, first N rows as metadata block, or a separate .json sidecar if allowed)
- the artifact metadata record (RPT artifact registry)

---

## 4. Output Schemas (Implementation-Ready)

### 4.1 CSV Export (Baseline)
CSV columns must be stable per schema_version.

Recommended baseline columns:
- wp_id
- task_id
- task_name
- phase
- task_type
- owner_role
- status
- predecessor_ids (comma-separated)
- dependency_type (FS)
- lag_days
- planned_duration_days
- proposed_start_date
- proposed_end_date
- committed_start_date
- committed_end_date
- actual_start_date
- actual_end_date
- notes

Export header metadata (either as separate file or leading commented rows):
- export_schema_version
- generated_at_utc
- stamp set (preset/profile/task_pool/calendar + others)

### 4.2 Report Types
RPT supports named report types with deterministic layouts:
- RPT_STATUS_SUMMARY
- RPT_READINESS_CHECK
- RPT_TRACEABILITY_STAMPS
- RPT_SCHEDULE_OVERVIEW (proposed vs committed)
- RPT_CRITICAL_PATH (optional if planning provides)

Each report type has a stable section list to avoid drift.

---

## 5. Metrics Computation Policy

### 5.1 Metrics Are Derived, Not Assumed
RPT computes metrics strictly from WP truth and declared rules:
- percent_complete (tasks DONE / total committed tasks)
- open_tasks_by_phase
- overdue_tasks (committed_end_date < today and status != DONE)
- cycle_time estimates (if actual dates exist)
- schedule variance (committed vs actual; proposed vs committed)

### 5.2 Calendar Consistency
If RPT computes working-day deltas:
- it must use the same calendar_logic_version declared in stamps.
- if calendar logic is missing or unsupported, it must either:
  - refuse (strict mode), or
  - compute in calendar days and label explicitly (policy choice)

Default for CQV: refuse if calendar version missing for working-day metrics.

---

## 6. Reporting & Export Contract (Implementation-Ready)

RPT is invoked via `VALOR-contract-orch-rpt`.

### 6.1 Actions
READ:
- RPT_LIST_ARTIFACTS (filters by wp_id/type)
- RPT_GET_ARTIFACT (artifact_id)

GENERATE:
- RPT_GENERATE_REPORT
- RPT_GENERATE_EXPORT

VALIDATE:
- RPT_VALIDATE_STAMPS (pre-check)
- RPT_VALIDATE_SCHEMA (pre-check export schema)

### 6.2 Canonical Request Envelope (Generate Export)
```json
{
  "contract": "VALOR-contract-orch-rpt",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000420",
  "action_type": "RPT_GENERATE_EXPORT",
  "mode": "M2",
  "target": {"wp_id": "WP-0007"},
  "payload": {
    "export_type": "CSV",
    "export_schema_version": "v1.0.1",
    "include_fields": ["baseline"],
    "stamps": {
      "preset_id": "PRESET-PE-HIGH",
      "preset_version": "v1.0.1",
      "profile_id": "PROF-PE-HIGH",
      "profile_version": "v1.0.1",
      "task_pool_id": "TP-CORE",
      "task_pool_version": "v1.0.1",
      "calendar_logic_version": "v1.0.1"
    }
  },
  "options": {"return_content": true},
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 6.3 Canonical Response Envelope
<!-- NOTE: Example is illustrative, not complete. Refer to schema for full structure. -->
```json
{
  "contract": "VALOR-contract-orch-rpt",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000420",
  "ok": true,
  "result": {
    "artifact_id": "RPT-EXP-0002",
    "artifact_type": "EXPORT",
    "format": "CSV",
    "schema_version": "v1.0.1",
    "generated_at_utc": "2025-12-22T00:00:00Z",
    "stamps": {"calendar_logic_version": "v1.0.1"},
    "content": "wp_id,task_id,...\nWP-0007,T-0001,...\n"
  },
  "error": null
}
```

---

## 7. Error Semantics (Reporting/Export)

Standard codes:
- VALIDATION_ERROR: invalid schema request, missing required fields
- INVARIANT_VIOLATION: missing stamps, attempt to mutate truth
- MODE_VIOLATION: wrong mode (policy)
- NOT_FOUND: wp/artifact not found
- CONFLICT: schema version unsupported, ambiguous version_ref
- UNSUPPORTED_OPERATION: format not supported
- INTERNAL_ERROR: unexpected

RPT-specific subcodes:
- MISSING_TRACEABILITY_STAMPS
- SCHEMA_VERSION_UNSUPPORTED
- FORMAT_NOT_SUPPORTED
- CALENDAR_LOGIC_MISSING
- METRIC_RULE_UNDEFINED

Example error:
```json
{
  "code": "INVARIANT_VIOLATION",
  "subcode": "MISSING_TRACEABILITY_STAMPS",
  "message": "Export blocked: missing task_pool_id/version.",
  "field": "task_pool_id",
  "entity": "traceability",
  "remediation": "Select a preset/task pool and retry export."
}
```

---

## 8. Determinism and Reproducibility
Given the same:
- WP snapshot,
- stamps,
- schema_version,
- report type,
RPT must produce the same output content.

If any input changes:
- a new artifact_id must be generated.

RPT must record:
- wp_snapshot_hash,
- schema_version,
- stamps,
- generation timestamp and action_id.

---

## 9. Integration Points
- Orchestration gates export generation using stamps and global invariants.
- WP System provides authoritative snapshots.
- Planning may provide plan proposals for “schedule overview” reports; outputs must clearly label PROPOSED vs COMMITTED.
- Document Factory outputs (doc metadata) may be referenced by RPT for traceability reports.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
