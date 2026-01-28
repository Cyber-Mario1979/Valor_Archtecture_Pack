---
id: VALOR-block-A09-governance-branching-architecture
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
  - VALOR-block-A04-1-orchestration-architecture
  - VALOR-block-A04-2-work-package-architecture
summary: "Block A09 — Governance & Branching Architecture: CQV-first change control inside Valor (stage/commit gates, branching policies, approvals, and an append-only audit trail of decisions and mutations)."
acceptance_criteria:
  - Defines governance objectives, scope, and what is human-approved vs system-enforced.
  - Defines gating model (stage → validate → commit → apply → export) and required confirmations.
  - Defines branching model (design branches vs execution branches) and merge/closure rules.
  - Defines audit trail event schema (append-only), required event fields, and provenance stamps.
  - Defines approval model (who approves what) without claiming to sign/approve automatically.
  - Defines error semantics and safe failure behaviors aligned with CQV expectations.
---

# Governance & Branching Architecture

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and CQV Objective
Governance is the mechanism by which Valor remains usable in regulated CQV environments:
- It prevents silent changes and undocumented drift.
- It separates proposals/drafts from committed truth.
- It provides an audit trail of what changed, why, by whom, and using which governed versions.

Branching is the mechanism by which Valor supports:
- exploration without contaminating authoritative work,
- parallel alternatives (different presets, durations, or plans),
- controlled merges into a single “committed” WP truth.

Governance is not optional; it is the backbone of CQV trust.

---

## 2. Scope (What Governance Controls)

### 2.1 In Scope
Governance controls:
- WP/task truth mutations (create, stage, commit, update, close),
- schedule application (writing committed dates),
- document finalization (FINAL artifacts),
- export generation (regulated outputs),
- version pinning (preset/profile/task_pool/calendar/standards bundle),
- branching and merge decisions.

### 2.2 Out of Scope (Human/External)
Governance does not replace:
- QMS approvals (change control boards, deviation approvals),
- electronic signatures (e-sign systems),
- vendor contractual actions.

Valor can prepare artifacts for these processes, but cannot execute them.

---

## 3. Governance Model (Gates and Confirmations)

This model is enforced primarily by Orchestration and WP System (see A04.1, A04.2).

### 3.1 Canonical Gates
GATE-1: **Stage**
- Output: PROPOSED changes (staged tasks, staged schedule proposal, staged export request)
- No authoritative IDs committed (unless policy allows provisional IDs; not recommended).

GATE-2: **Validate**
- Output: validation report (errors/warnings/readiness flags)
- Must run before any commit or finalize.

GATE-3: **Commit**
- Output: authoritative WP/task truth mutation (IDs allocated, tasks committed)

GATE-4: **Apply**
- Output: authoritative update of dates/fields based on a proposal (e.g., apply plan)

GATE-5: **Finalize**
- Output: FINAL document artifact (checksum locked), or finalized export artifact

GATE-6: **Close**
- Output: WP closed (restricted mutability)

### 3.2 Mandatory Human Confirmations
Human confirmation is required before:
- committing staged tasks,
- applying schedule proposals to committed dates,
- finalizing documents,
- generating regulated exports (if stamps or readiness checks require confirmation),
- closing a WP.

Minimum confirmation capture:
- confirmation_id
- confirmer_role
- timestamp_utc
- scope (what is being committed/finalized)
- reference to staged object hash/id

### 3.3 Readiness Checks (CQV Default)
Before FINALIZE or EXPORT, system must ensure:
- required stamps present (A02 INV-07),
- WP validation passes or is explicitly overridden with rationale,
- document completeness checks pass (DOC_VALIDATE for docs),
- dependency graph valid (cycle-free),
- missing critical fields are resolved.

If readiness fails, system must block and return actionable remediation.

---

## 4. Branching Model

Branching exists at two levels:
- **Design/Architecture Branches**: spec exploration; not tied to WP truth.
- **Execution Branches**: alternative staged/committed states for a specific WP.

### 4.1 Branch Types
1) **BR-DESIGN**
- Used for: architecture specs, contracts, templates, matrix design.
- Output: documents and controlled assets versions (not WP truth).

2) **BR-EXEC**
- Used for: alternative staging of tasks/plans for a specific WP.
- Output: staged objects, possibly committed WP changes if merged.

### 4.2 Branch Entity Schema
Required fields:
- branch_id (string)
- branch_type (BR-DESIGN | BR-EXEC)
- parent_branch_id (optional)
- wp_id (required for BR-EXEC; null for BR-DESIGN)
- created_at_utc, updated_at_utc
- purpose (string)
- state (ACTIVE | FROZEN | MERGED | CLOSED)
- stamp_context (snapshot of selected asset versions)
- pointers:
  - staged_task_set_id (optional)
  - plan_id (optional)
  - doc_ids (optional)
  - export_ids (optional)

### 4.3 Branch Rules
- BR-EXEC must reference exactly one wp_id.
- A branch carries pinned stamps; changing stamps creates a new branch or a new branch revision.
- Only one “primary execution branch” should be designated for export-ready truth (policy).

---

## 5. Merge and Conflict Rules

### 5.1 Merge Types
- MERGE_STAGED_TASKS: staged task sets merged into primary branch staging
- MERGE_PLAN_PROPOSALS: plan proposal chosen as the plan-to-apply
- MERGE_WP_MUTATIONS: committed WP updates merged (rare; prefer merge before commit)

### 5.2 Conflict Detection
Conflicts occur when branches differ in:
- task list (added/removed tasks),
- dependency edges,
- task field values (owners, durations),
- stamp context (preset/profile/task_pool/calendar/bundle versions),
- committed dates.

Conflict policy:
- Conflicts must be surfaced explicitly.
- No “auto-merge” for CQV by default.
- User must choose resolution strategy:
  - take ours, take theirs, manual merge.
- If stamp context differs, merge is blocked unless user explicitly approves the stamp change and a new provenance record is created.

---

## 6. Approval Model (Who Approves What)

Approvals are represented as governance records, not signatures.

### 6.1 Approval Categories
- APPROVE_STAGE_TO_COMMIT (commit tasks)
- APPROVE_PLAN_APPLY (apply proposed dates)
- APPROVE_DOC_FINALIZE (finalize document)
- APPROVE_EXPORT (generate regulated export)
- APPROVE_WP_CLOSE (close WP)

### 6.2 Role Expectations (Typical CQV)
These are defaults, not enforced identities:
- CQV Lead: plan apply, WP close, execution readiness
- QA: document finalization readiness, export acceptance
- Engineering/Automation: technical content readiness
- Production/QC/SHE: where operational inputs are required

Policy:
- The system stores who approved, but it does not validate real-world authority unless integrated with identity systems.

---

## 7. Audit Trail (Append-Only Event Log)

### 7.1 Audit Event Schema (Canonical)
Every governance-relevant action must write an audit event.

Required fields:
- event_id (string)
- timestamp_utc
- event_type (enum; see §7.2)
- actor: {role, name(optional), id(optional)}
- branch_id
- wp_id (optional for design events)
- action_id (contract action reference)
- before_hash (optional; hash of prior WP snapshot)
- after_hash (optional; hash of resulting WP snapshot)
- stamps (required for execution events; see §7.3)
- rationale (string; required for overrides/conflicts)
- attachments (optional references: doc_id/export_id)

### 7.2 Event Types (Minimum Set)
- EVT_BRANCH_CREATED
- EVT_BRANCH_FROZEN
- EVT_STAGE_CREATED
- EVT_VALIDATION_RUN
- EVT_COMMIT_EXECUTED
- EVT_PLAN_GENERATED
- EVT_PLAN_APPLIED
- EVT_DOC_GENERATED
- EVT_DOC_FINALIZED
- EVT_EXPORT_GENERATED
- EVT_WP_CLOSED
- EVT_OVERRIDE_ACCEPTED
- EVT_MERGE_ATTEMPTED
- EVT_MERGE_RESOLVED

### 7.3 Stamp Requirements on Events
Execution events must include at minimum:
- preset_id/version
- profile_id/version
- task_pool_id/version
- calendar_logic_version

When relevant:
- standards_bundle_id/version
- template_id/version
- planning_logic_version
- contract versions invoked

### 7.4 Integrity Properties
- Append-only: events are never edited; corrections create new events.
- Hash chaining (recommended):
  - each event includes previous_event_hash to create a tamper-evident chain.
- Export artifacts should include the latest_event_hash as provenance.

---

## 8. Overrides and Exceptions (CQV Safe Handling)

### 8.1 Override Types
- readiness_override (export despite warnings)
- duration_override (manual duration not matching profile default)
- dependency_override (rare; typically not allowed)
- stamp_override (changing governed versions mid-stream)

### 8.2 Override Requirements
An override must include:
- explicit confirmation,
- rationale,
- impact statement (what changes in outputs),
- new audit event EVT_OVERRIDE_ACCEPTED.

Default CQV stance:
- overrides are allowed, but visible and traceable.

---

## 9. Error Semantics and Safe Failure

Governance-related failures should be explicit:
- INVARIANT_VIOLATION / STAGING_REQUIRED
- INVARIANT_VIOLATION / MISSING_TRACEABILITY_STAMPS
- CONFLICT / BRANCH_CONFLICT_UNRESOLVED
- VALIDATION_ERROR / READINESS_NOT_MET
- MODE_VIOLATION / WRONG_MODE_FOR_COMMIT

Safe failure rule:
- If the system cannot prove a commit/finalize occurred, it must not claim it did.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
