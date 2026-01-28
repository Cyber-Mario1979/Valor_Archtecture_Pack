---
id: VALOR-block-A04-2-work-package-architecture
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
summary: "Block A04.2 — Work Package System Architecture: authoritative WP/task truth, lifecycle state machine, deterministic ID allocation, dependency integrity, and enforcement of CQV invariants."
acceptance_criteria:
  - Defines authoritative WP and Task entities, required fields, and mutability rules.
  - Defines lifecycle state machine for WP and tasks (stage, commit, close) with allowed transitions.
  - Defines deterministic ID allocation with non-reuse and tombstoning.
  - Defines dependency model and validation (acyclic graph, allowed dependency types).
  - Defines contract actions (read, stage, commit, update, validate) and error semantics.
  - Defines invariants enforcement aligned with global invariants (A02).
---

# Work Package System Architecture

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
The Work Package (WP) System is Valor’s **single source of truth** for:
- Work Package objects,
- Task objects (including dependencies and statuses),
- committed task dates (when applied),
- lifecycle transitions (stage → commit → close),
- deterministic ID issuance and non-reuse.

Any plan, report, or document is derived from WP truth. If it is not reflected in WP truth, it is not authoritative.

---

## 2. Core Entities (Authoritative Data Model)

### 2.1 Work Package (WP)
A WP represents a controlled scope of work, typically bound to:
- equipment/system/facility scope,
- CQV stage,
- owner functions and interfaces,
- governance state.

**Required fields (minimum)**
- wp_id (string, immutable once assigned)
- title (string)
- scope (string)
- wp_type (enum): Equipment | Utility | Facility | Project
- complexity (enum): Low | Medium | High
- lifecycle_state (enum; see §3)
- created_at_utc, updated_at_utc
- owner_function (string)
- references (optional): vendor_id, project_id, change_control_id

**Optional fields**
- preset_ref: {preset_id, preset_version}
- profile_ref: {profile_id, profile_version}
- standards_bundle_ref: {bundle_id, version}
- calendar_logic_ref: {calendar_id, calendar_version}

### 2.2 Task
A Task is the atomic unit of execution within a WP.

**Required fields (minimum)**
- task_id (string, immutable once assigned)
- wp_id (string, parent)
- name (string)
- task_type (enum): AUTHORING | REVIEW | APPROVAL | EXECUTION | REPORTING | VENDOR_WAIT | PROCUREMENT_WAIT | LEAD_TIME
- phase (enum): VMP | URS | RA | RTM | DQ | IQ | OQ | PQ | VSR | OTHER
- status (enum; see §3)
- dependencies (array of dependency edges; can be empty)
- planned_duration_days (number; may be empty until profile/preset applied)
- owner_role (string; e.g., CQV, QA, ENG, AUTO, PROD, QC, SHE)
- created_at_utc, updated_at_utc

**Date fields**
- proposed_start_date, proposed_end_date (optional; advisory)
- committed_start_date, committed_end_date (optional; authoritative once set)
- actual_start_date, actual_end_date (optional; execution evidence)

Rule:
- “proposed_*” may be written during staging.
- “committed_*” is only written during an explicit APPLY/COMMIT action.

### 2.3 Dependency Edge
Dependencies are explicit edges between tasks.

Fields:
- predecessor_task_id
- successor_task_id
- dependency_type (enum): FS | SS | FF | SF
- lag_days (integer; default 0)
- notes (optional)

Baseline (as per current plan):
- Support FS only initially (FS), but model is future-proofed for SS/FF/SF.

---

## 3. Lifecycle State Machine

### 3.1 WP Lifecycle States
- WP_DRAFT: WP created, tasks may be staged but not committed.
- WP_STAGED: staged task set exists (PROPOSED), awaiting commit.
- WP_COMMITTED: tasks exist with allocated IDs (authoritative list).
- WP_IN_EXECUTION: execution underway (optional; can be derived from task statuses).
- WP_CLOSED: WP closed; further mutations are restricted.

### 3.2 Task Status States
- TASK_STAGED (PROPOSED, no final ID unless policy allows provisional IDs)
- TASK_COMMITTED (authoritative task exists)
- TASK_IN_PROGRESS
- TASK_DONE
- TASK_BLOCKED
- TASK_CANCELLED

### 3.3 Allowed Transitions (WP)
| From | To | Trigger | Gate |
|---|---|---|---|
| WP_DRAFT | WP_STAGED | Stage tasks | validation OK |
| WP_STAGED | WP_COMMITTED | Commit staged tasks | user confirmation required |
| WP_COMMITTED | WP_IN_EXECUTION | Start execution | optional |
| WP_IN_EXECUTION | WP_CLOSED | Close WP | closure criteria met |
| WP_COMMITTED | WP_CLOSED | Close WP (no execution) | closure criteria met |

Hard rules:
- Cannot commit without staging (A02 INV-03).
- Cannot close with unresolved required tasks unless explicitly cancelled with rationale.

### 3.4 Allowed Transitions (Task)
| From | To | Trigger |
|---|---|---|
| TASK_STAGED | TASK_COMMITTED | WP_COMMIT_STAGED_TASKS |
| TASK_COMMITTED | TASK_IN_PROGRESS | execution start |
| TASK_IN_PROGRESS | TASK_DONE | execution complete |
| TASK_* | TASK_BLOCKED | blocker recorded |
| TASK_* | TASK_CANCELLED | cancellation with rationale |

---

## 4. Deterministic ID Allocation

### 4.1 ID Format (Implementation Guidance)
- WP IDs: `WP-0001`, `WP-0002`, ...
- Task IDs: `T-0001`, `T-0002`, ... (or WP-scoped `WP-0001-T-0001`)

The specific format can vary, but must satisfy:
- uniqueness,
- determinism,
- non-reuse.

### 4.2 Non-Reuse and Tombstoning
Invariant (A02 INV-04):
- IDs are never reused.
- If an item is deleted or cancelled, its ID is tombstoned.

Implementation check:
- Maintain an append-only ID ledger.

---

## 5. Dependency Integrity and Validation

### 5.1 Acyclic Graph
Invariant (A02 INV-05):
- Dependency graph must be acyclic.

Validation:
- On any dependency update, run cycle detection and reject loops.

### 5.2 Allowed Dependency Types (Initial)
For v0.1.x baseline:
- Allow FS only.
- If other types appear, reject as UNSUPPORTED_OPERATION unless explicitly enabled.

### 5.3 Lag Rules
- lag_days defaults to 0
- negative lags are rejected unless explicitly supported by policy.

---

## 6. Mutability Rules (What Can Change When)

### 6.1 WP Mutability
- wp_id immutable.
- lifecycle_state transitions must follow §3.
- references may be added/updated in DRAFT/COMMITTED; restricted in CLOSED.

### 6.2 Task Mutability
- task_id immutable.
- name/type/phase/owner_role can be edited in COMMITTED until execution starts (policy).
- dependencies editable until execution starts (policy).
- committed dates editable only through explicit APPLY (with justification if changed after execution starts).

---

## 7. WP Contract Actions (Implementation-Ready)

The WP System exposes actions to Orchestration via `VALOR-contract-orch-wp`.

### 7.1 Read Operations
- WP_GET (wp_id)
- WP_LIST (filters)
- TASK_GET (task_id)
- TASK_LIST (wp_id)

### 7.2 Stage Operations (No Truth Commitment)
- WP_STAGE_TASKS
  - Inputs: wp_id, preset_ref or task list references, selection context
  - Output: staged_task_set (hash/id) + preview tasks (no committed IDs)

- WP_VALIDATE_STAGE
  - Validates required fields, dependency integrity, duplicate tasks, etc.

### 7.3 Commit Operations (Truth Mutation)
- WP_COMMIT_STAGED_TASKS
  - Requires: staged_task_set_id + user confirmation recorded by Orchestration
  - Output: committed tasks with allocated task_ids

### 7.4 Update Operations (Truth Mutation with Rules)
- WP_UPDATE_TASK_FIELDS
  - Used for applying schedule dates, changing owners, updating statuses
  - Must reject changes violating mutability rules (e.g., illegal state transition)

- WP_UPDATE_DEPENDENCIES
  - Must validate cycle-free graph

### 7.5 Close Operations
- WP_CLOSE
  - Requires: closure checklist satisfied (policy-driven)
  - Output: lifecycle_state = WP_CLOSED

### 7.6 Validation Operations
- WP_VALIDATE (wp_id)
  - Returns: errors/warnings, readiness flags for export/doc generation

---

## 8. Error Semantics (WP System)

Standard codes:
- VALIDATION_ERROR: missing or invalid required fields
- INVARIANT_VIOLATION: violates global invariants (cycle, staging required, ID reuse)
- MODE_VIOLATION: wrong mode for mutation request
- NOT_FOUND: unknown wp_id/task_id
- CONFLICT: version/selection conflicts (e.g., preset/profile mismatch)
- UNSUPPORTED_OPERATION: unsupported dependency type, negative lag, etc.
- INTERNAL_ERROR: unexpected

WP-specific subcodes:
- STAGING_REQUIRED
- CYCLE_DETECTED
- ILLEGAL_STATE_TRANSITION
- MUTABILITY_RESTRICTED
- DUPLICATE_TASK
- MISSING_REQUIRED_FIELD

Example error:
```json
{
  "code": "INVARIANT_VIOLATION",
  "subcode": "CYCLE_DETECTED",
  "message": "Dependency update rejected: cycle detected involving T-0007 → T-0009 → T-0007.",
  "entity": "dependency_graph",
  "remediation": "Remove one edge to break the cycle and retry."
}
```

---

## 9. Integration Points
- Orchestration uses WP actions for all truth mutations and gating.
- Planning reads committed tasks/dependencies and returns PROPOSED schedule; Orchestration applies via WP_UPDATE_TASK_FIELDS.
- Document Factory reads WP truth and produces documents; WP may store doc references.
- Reporting reads WP truth and produces projection outputs; does not mutate WP.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
