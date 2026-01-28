---
id: VALOR-block-A05-task-pool-architecture
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
summary: "Block A05 — Task Pool Library Architecture: governed catalog of atomic tasks with metadata, default dependency wiring, and deterministic selection rules used to stage WP tasks."
acceptance_criteria:
  - Defines Task Pool as the authoritative source of atomic task definitions and metadata.
  - Defines atomic task entity schema (required fields, tags, applicability, default durations refs).
  - Defines selection rules (filters, presets binding, inclusion/exclusion, version determinism).
  - Defines default dependency wiring and “insertion blocks” (e.g., RTM, vendor wait, procurement wait).
  - Defines contracts/interfaces to list/read tasks and to resolve a task set for staging.
  - Defines governance/change control expectations and integrity invariants.
---

# Task Pool Library Architecture (Atomic Tasks + Metadata + Selection Rules)

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
The Task Pool Library (TP) is Valor’s **authoritative catalog** of reusable, atomic tasks.
It exists to:
- standardize CQV task decomposition (authoring, review, approvals, execution, reporting, vendor waits),
- enable deterministic task suggestion and staging,
- provide consistent metadata for planning, reporting, and document generation.

TP is authoritative for:
- atomic task definitions (what the task is),
- task metadata (phase/type/tags/applicability),
- default dependency wiring patterns (when applicable),
- versioned change control (library updates are governed).

TP is not authoritative for:
- WP/task truth instances (owned by WP System),
- committed dates (owned by WP System; proposed by Planning),
- project-specific scope and tailoring decisions (user + Orchestration).

---

## 2. Core Entities (Authoritative Data Model)

### 2.1 TaskPool
A TaskPool is a versioned collection of atomic tasks.

Required fields:
- task_pool_id (string, stable)
- version (semver)
- revision_date (YYYY-MM-DD)
- description (string)
- owner_function (string; e.g., CQV/QA)
- tasks (array of AtomicTask)
- integrity:
  - checksum (optional)
  - schema_version (string)
- governance:
  - change_control_ref (optional)

### 2.2 AtomicTask
An AtomicTask is a reusable definition (not a WP instance).

Required fields:
- atomic_task_id (string, stable within pool)
- name (string)
- phase (enum): VMP | URS | RA | RTM | DQ | IQ | OQ | PQ | VSR | OTHER
- task_type (enum): AUTHORING | REVIEW | APPROVAL | EXECUTION | REPORTING | VENDOR_WAIT | PROCUREMENT_WAIT | LEAD_TIME
- owner_role_default (string; e.g., CQV, QA, ENG, AUTO, PROD, QC, SHE)
- applicability_tags (array of strings)
  - examples: ProcessEquipment, Utilities, Facility, HighComplexity, LowComplexity, SingleEquipment, Project
- required_inputs (array of strings) (what must exist in WP before task is “ready”)
- outputs (array of strings) (expected deliverables: protocol, report, RTM table, etc.)
- duration_ref (object) (points to governed profile duration keys; does not embed numbers)
  - {profile_key: "URS_AUTHORING_DAYS"} or similar
- dependency_wiring (optional) (see §2.3)
- flags (optional):
  - is_milestone (bool)
  - is_insertion_block (bool)
  - is_optional (bool)
- notes (optional)

### 2.3 DependencyWiring (Default)
Dependency wiring expresses default relationships when atomic tasks are instantiated into a WP.

Fields:
- predecessors (array of wiring refs)
  - each: {atomic_task_id, dependency_type="FS", lag_days=0}
- successor_hints (optional) (rare; usually defined from successors’ predecessor lists)

Invariant:
- Wiring must be cycle-free within the pool graph.

---

## 3. Metadata Taxonomy (Standard Tags)

### 3.1 Capability Tags
Used for selection and applicability:
- Domain: ProcessEquipment | Utilities | Facility
- Complexity: LowComplexity | MediumComplexity | HighComplexity
- Scope: SingleEquipment | Project
- Lifecycle: Procurement | Vendor | Commissioning | Qualification
- Department: CQV | QA | ENG | AUTO | PROD | QC | SHE

### 3.2 Task Semantics
Task types encode behavior:
- VENDOR_WAIT: waiting for vendor response (quotation, FAT slot, etc.)
- PROCUREMENT_WAIT: PO processing, approvals, commercial lead
- LEAD_TIME: manufacturing/construction lead time blocks
These are first-class tasks, not hidden assumptions, because they dominate real project timelines.

---

## 4. Selection Rules (Deterministic Task Set Resolution)

Task selection is deterministic and governed by:
- explicit preset binding (preferred),
- selection context (equipment type, complexity, scope),
- include/exclude rules and optionality,
- version pinning (task_pool_version).

### 4.1 Selection Context
Orchestration passes a selection context object:
- equipment_domain: ProcessEquipment | Utilities | Facility
- complexity: Low | Medium | High
- scope: SingleEquipment | Project
- optional: system_type (e.g., RollerCompactor, BlisterLine)
- optional: site constraints (working week, holidays)
- optional: departments in scope (CQV, QA, ENG, AUTO, PROD, QC, SHE)

### 4.2 Rule Types
- FILTER: include tasks whose applicability_tags match context
- REQUIRED: always include core tasks for a given phase
- OPTIONAL: include only if user enables (e.g., additional assessments)
- INSERT: insert “block tasks” between phases (e.g., RTM block, quotation wait)
- EXCLUDE: remove tasks that conflict with a selection flag

### 4.3 Determinism Requirements
- Given the same task_pool_id/version and selection context, resolution must return the same ordered task set.
- Any ambiguity (multiple pools match without explicit ID/version) must result in CONFLICT, not guessing.

### 4.4 Ordering Policy
Ordering is derived by:
1) dependency graph topological order (FS baseline)
2) stable tie-break by phase order then atomic_task_id

---

## 5. Default Dependency Wiring Patterns (CQV-Relevant)

Examples of wiring patterns that must be represented explicitly as tasks + edges:

### 5.1 VMP Optional Predecessor to URS
- If scope=Project:
  - VMP_AUTHORING → VMP_REVIEW → VMP_APPROVAL → URS_AUTHORING
- If scope=SingleEquipment:
  - URS_AUTHORING may start without VMP (preset decides).

### 5.2 Vendor Quotation and URS Deviation Flow (Realistic Wait)
- URS_ISSUE_TO_VENDOR (milestone or execution task)
  → VENDOR_WAIT_QUOTATION
  → QUOTATION_REVIEW
  → URS_DEVIATION_LIST
  → RTM_BLOCK (if required)

### 5.3 PO and Lead-Time Blocks
- PO_ISSUED (milestone)
  → LEAD_TIME_MANUFACTURING (e.g., 6–8 months for blister line)
  → FAT_PREP
  → FAT_EXECUTION
  → SHIPMENT
  → SITE_RECEIPT

These are modeled as tasks to prevent “IQ tomorrow after PO today” unrealistic plans.

---

## 6. Task Pool Contracts (Implementation-Ready)

TP is accessed via `VALOR-contract-orch-tp` (or equivalent naming in your pack).

### 6.1 Actions
READ:
- TP_LIST_POOLS (filters)
- TP_READ_POOL (task_pool_id + version)
- TP_LIST_TASKS (filters by tags/phase/type)
- TP_READ_TASK (atomic_task_id)

RESOLVE:
- TP_RESOLVE_TASK_SET
  - Inputs: task_pool_ref + selection context + optional preset rules
  - Output: ordered list of atomic tasks + resolved wiring graph + stamps

VALIDATE:
- TP_VALIDATE_POOL_INTEGRITY (cycle checks, schema checks)

### 6.2 Canonical Request (Resolve Task Set)
```json
{
  "contract": "VALOR-contract-orch-tp",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000520",
  "action_type": "TP_RESOLVE_TASK_SET",
  "mode": "M2",
  "payload": {
    "task_pool_ref": {"task_pool_id": "TP-CORE", "task_pool_version": "v1.0.1"},
    "selection_context": {
      "equipment_domain": "ProcessEquipment",
      "complexity": "High",
      "scope": "Project",
      "departments": ["CQV","QA","ENG","AUTO","PROD","QC","SHE"]
    }
  },
  "options": {"return_wiring": true},
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 6.3 Canonical Response
```json
{
  "contract": "VALOR-contract-orch-tp",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000520",
  "ok": true,
  "result": {
    "task_set_id": "TPSET-0007",
    "tasks": [
      {"atomic_task_id": "AT-URS-AUTH", "phase": "URS", "task_type": "AUTHORING"}
    ],
    "wiring": [
      {"pre": "AT-VMP-APP", "succ": "AT-URS-AUTH", "type": "FS", "lag_days": 0}
    ],
    "stamps": {"task_pool_id": "TP-CORE", "task_pool_version": "v1.0.1"}
  },
  "error": null
}
```

---

## 7. Error Semantics (Task Pool)

Standard codes:
- VALIDATION_ERROR: invalid context, invalid filters
- INVARIANT_VIOLATION: pool contains cycles, missing required fields, duplicate IDs
- NOT_FOUND: pool/task not found
- CONFLICT: ambiguous match, incompatible version refs
- UNSUPPORTED_OPERATION: unsupported dependency type requested
- INTERNAL_ERROR: unexpected

TP-specific subcodes:
- POOL_CYCLE_DETECTED
- DUPLICATE_ATOMIC_TASK_ID
- CONTEXT_INSUFFICIENT
- VERSION_UNSUPPORTED

Example error:
```json
{
  "code": "INVARIANT_VIOLATION",
  "subcode": "POOL_CYCLE_DETECTED",
  "message": "Task pool wiring is invalid: cycle detected AT-RTM → AT-DQ → AT-RTM.",
  "entity": "task_pool",
  "remediation": "Fix wiring graph and publish a new task_pool_version."
}
```

---

## 8. Governance and Change Control

### 8.1 Update Policy
- Task pools are versioned and immutable per version.
- Any change to tasks or wiring requires a new version.
- Presets must reference explicit pool versions for audit reproducibility.

### 8.2 Integrity Checks (Pre-Release)
- schema validation
- uniqueness of atomic_task_id
- cycle detection
- tag consistency checks

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
