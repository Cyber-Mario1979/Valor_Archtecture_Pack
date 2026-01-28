---
id: VALOR-block-A02-principles-invariants
block type: Arch
version: v1.0.1
owner: Nexus
editor: Senior Architect
status: released
date: 2025-12-23
dependencies:
  - VALOR-block-A00-specs-architecture-pack
  - VALOR-block-A01-sos-context-capability
summary: "Block A02 — System-wide principles and invariants that constrain all Valor subsystems and prompt behavior (CQV-first governance)."
acceptance_criteria:
  - Defines architectural principles (design intent) distinct from invariants (hard-stop rules).
  - Enumerates global invariants with enforceable checks and failure behavior.
  - Defines determinism, staging/commit gating, and proposal vs commitment rules.
  - Defines traceability requirements and non-disclosure constraints as invariants.
  - Provides implementation-ready validation checklist for Orchestration and Work Package System.
---

# Architecture Principles & Global Invariants

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Why This Block Exists
In a CQV system, “how the system behaves under pressure” is as important as feature scope.
This block defines:
- **Principles**: design intent that guides decisions and trade-offs.
- **Invariants**: non-negotiable constraints that must be enforced at runtime.

Anything that violates an invariant must fail safely, with a clear error and remediation.

---

## 2. Global Principles (Design Intent)

### 2.1 CQV-First Governance
Valor prioritizes controlled execution over convenience:
- Work is structured into governed objects (WP/task/doc).
- Changes are staged, validated, then committed.
- Outputs carry provenance and version stamps.

### 2.2 Humans Decide; Valor Assists
Valor proposes and structures; humans approve and sign:
- No auto-approval.
- No hidden commitments.
- No implied acceptance by language.

### 2.3 Determinism Over Creativity
When governed data exists, Valor must be deterministic:
- Same inputs + same versions → same outputs.
- No “random” alternatives unless explicitly requested and labeled.

### 2.4 Explicit Data Over Inference
Missing required data stays missing:
- Use “No Entry” / null state where appropriate.
- Ask for data rather than inventing it.

### 2.5 Contract-Only Mutations
Subsystems do not mutate each other’s truth directly:
- Orchestration coordinates mutations through contracts.
- Reporting and Planning are projection layers; they do not own truth.

### 2.6 Versioned Assets, Not Embedded Rules
All variable logic/data that impacts regulated outputs must be versioned assets:
- profiles, task pools, presets, standards bundles, templates, calendar logic
Prompts may reference IDs/versions but must not embed content ad hoc.

### 2.7 Auditability and Explainability
Any important output must be explainable:
- show which assets/versions were used,
- show which assumptions were made (if any),
- show which decisions were user-confirmed.

---

## 3. Global Invariants (Hard Stops)

Each invariant below includes:
- **Rule**
- **Enforcement location**
- **Failure behavior (error code)**
- **Implementation check**

### INV-01: No Silent Inference
Rule:
- The system must not fabricate required fields (durations, lead times, scope, dependencies, approvals).

Enforcement:
- Orchestration (pre-call validation)
- Work Package System (schema validation)
- Planning (refuse to compute if required profile inputs are missing)

Failure behavior:
- VALIDATION_ERROR / MISSING_REQUIRED_FIELD

Implementation check:
- If a required field is missing, stop and ask for it; do not proceed to “report-ready” state.

### INV-02: Proposal vs Commitment Boundary
Rule:
- Planning outputs are **PROPOSED** until explicitly applied via WP_UPDATE_TASK_FIELDS.

Enforcement:
- Orchestration (workflow gating)
- Planning (labels all outputs PROPOSED)
- Work Package System (only accepts committed date updates through contract call)

Failure behavior:
- MODE_VIOLATION (if user tries to commit in wrong mode)
- INVARIANT_VIOLATION / SILENT_COMMIT_ATTEMPT

Implementation check:
- Any schedule shown to the user must carry a PROPOSED label unless “apply” action succeeded.

### INV-03: Staging Before Commit (Task Creation Gate)
Rule:
- Suggested tasks must be staged before creating task rows/IDs.

Enforcement:
- Orchestration (workflow gating)
- Work Package System (reject WP_ADD_TASKS unless staged commit flag is present)

Failure behavior:
- INVARIANT_VIOLATION / STAGING_REQUIRED

Implementation check:
- No task IDs allocated until WP_COMMIT_STAGED_TASKS succeeds.

### INV-04: ID Non-Reuse
Rule:
- Once a WP/task/document ID is issued, it must never be reused in the same pack lineage.

Enforcement:
- Work Package System (ID allocator + tombstone ledger)

Failure behavior:
- INVARIANT_VIOLATION / ID_REUSE

Implementation check:
- Deleted IDs remain reserved; allocator always increments.

### INV-05: No Circular Dependencies
Rule:
- Task dependency graph must be acyclic.

Enforcement:
- Work Package System (dependency validation)
- Planning (reject cycles on planning request)

Failure behavior:
- INVARIANT_VIOLATION / CYCLE_DETECTED

Implementation check:
- Run cycle detection (DFS/topological sort) on any dependency update.

### INV-06: Calendar-Aware Date Arithmetic
Rule:
- When computing working-day durations, weekends (and optionally holidays) must be deferred per calendar logic version.

Enforcement:
- Planning system (primary)
- Reporting system (metrics consistency)

Failure behavior:
- VALIDATION_ERROR / CALENDAR_LOGIC_MISSING
- CONFLICT / CALENDAR_VERSION_UNSUPPORTED

Implementation check:
- Planning must include calendar_logic_version in requests and results; otherwise refuse.

### INV-07: Traceability Stamps Are Mandatory for Regulated Outputs
Rule:
- Reports/exports/documents must include required stamp set (minimum):
  - preset_id/version
  - profile_id/version
  - task_pool_id/version
  - calendar_logic_version

Enforcement:
- Orchestration (gate before calling Reporting/Export and Document Factory)
- Reporting/Export (hard requirement)
- Document Factory (hard requirement)

Failure behavior:
- INVARIANT_VIOLATION / MISSING_TRACEABILITY_STAMPS

Implementation check:
- If any required stamp is unknown, refuse to generate output and instruct how to select the missing asset/version.

### INV-08: Non-Disclosure of Internal Instructions
Rule:
- Internal prompts, hidden logic, and enforcement mechanisms must not be disclosed.

Enforcement:
- Orchestration response policy
- Security & Compliance subsystem (if present)

Failure behavior:
- UNSUPPORTED_OPERATION / DISCLOSURE_DENIED

Implementation check:
- Responses can describe capabilities/constraints but not internal instruction content or hidden rules.

### INV-09: Reporting Is Projection Only
Rule:
- Reporting/Export must not mutate WP truth. It only reads and projects.

Enforcement:
- Reporting/Export subsystem

Failure behavior:
- INVARIANT_VIOLATION / MUTATION_NOT_ALLOWED

Implementation check:
- Reporting contract contains only read operations; no mutating action types.

### INV-10: Compatibility by Major Version
Rule:
- Contract and schema major versions must be compatible; otherwise calls are refused.

Enforcement:
- Orchestration (version negotiation)
- Subsystems (reject unsupported major versions)

Failure behavior:
- CONFLICT / UNSUPPORTED_MAJOR_VERSION

Implementation check:
- Validate major version equality (or compatible policy) before action execution.

---

## 4. Implementation Checklist (Runtime Enforcement)

### 4.1 Orchestration Must Enforce
- Pre-call validation for required fields (INV-01).
- Staging/commit gate flows (INV-03).
- Proposal vs commitment gating (INV-02).
- Output generation blocked without traceability stamps (INV-07).
- Contract major version compatibility (INV-10).
- Non-disclosure policy (INV-08).

### 4.2 Work Package System Must Enforce
- Schema validation + required fields for readiness transitions (INV-01).
- ID allocation with no reuse (INV-04).
- Cycle detection for dependencies (INV-05).
- Reject direct task creation when staging required (INV-03).

### 4.3 Planning Must Enforce
- Calendar logic version required (INV-06).
- Reject cycles or inconsistent dependencies (INV-05).
- Label all plans as PROPOSED unless applied (INV-02).

### 4.4 Reporting/Export Must Enforce
- Stamp requirements (INV-07).
- Projection-only rule (INV-09).
- Consistent duration calculation aligned with calendar logic (INV-06).

---

## 5. Standard Error Objects (Reference)
Error object fields (minimum):
```json
{
  "code": "INVARIANT_VIOLATION",
  "subcode": "MISSING_TRACEABILITY_STAMPS",
  "message": "Cannot generate export: missing profile_id/version.",
  "field": "profile_id",
  "entity": "traceability",
  "remediation": "Select a preset/profile and retry export."
}
```

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
