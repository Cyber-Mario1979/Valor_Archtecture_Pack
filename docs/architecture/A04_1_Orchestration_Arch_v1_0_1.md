---
id: VALOR-block-A04-1-orchestration-architecture
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
summary: "Block A04.1 — Orchestration System Architecture: the controlled coordinator that routes intent to contracts, enforces governance gates, manages traceability context, and ensures deterministic CQV behavior."
acceptance_criteria:
  - Defines orchestration responsibilities, boundaries, and non-authority constraints.
  - Defines orchestration runtime state model (modes, session context, staged artifacts).
  - Defines orchestration I/O contracts at the envelope level (contract registry, action routing rules).
  - Defines governance gates (stage, commit, plan, apply, export) as enforceable steps.
  - Defines traceability context management and mandatory stamp propagation behavior.
  - Defines error taxonomy handling and safe failure behavior (no silent commit, no guessing).
---

# Orchestration System Architecture

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Position in Valor
Orchestration is Valor’s **system-of-systems controller**. It is the only subsystem that:
- receives unstructured user intent,
- converts that intent into contract-safe actions,
- coordinates multi-step flows across subsystems,
- enforces CQV governance gates and global invariants.

Orchestration is **not** a data-truth store. It is the policy and coordination layer.

---

## 2. Authority and Boundary

### 2.1 Orchestration Owns
Orchestration is authoritative for:
- intent classification and workflow selection,
- governance gating sequence and confirmations,
- traceability context assembly and propagation,
- contract routing rules and version negotiation,
- response policy (proposal vs commitment labeling).

### 2.2 Orchestration Does Not Own
Orchestration is not authoritative for:
- WP/task truth (owned by WP System),
- task definitions (owned by Task Pool Library),
- presets and selection rules (owned by Preset System),
- schedule truth (Planning is advisory; WP owns committed dates),
- templates/standards (owned by K&S),
- generated document content (owned by Document Factory),
- report/export content (owned by Reporting & Export).

This is enforced via **contract-only mutation** (A02 Principle §2.5).

---

## 3. Orchestration Runtime Model

### 3.1 Modes
Orchestration operates in modes that constrain allowed actions:
- **M1 (Architecture/Design Mode)**: define specs, contracts, assets; no commitments to WP truth.
- **M2 (Execution/Implementation Mode)**: create/stage/commit WPs, plan, apply, export.

Mode enforcement:
- If an action requires M2 but the session is in M1 → MODE_VIOLATION.

### 3.2 Session Context (The “Traceability Ledger”)
Orchestration maintains a session context object that must include:

**Selected governed assets**
- architecture_pack_id/version
- preset_id/version (if used)
- task_pool_id/version (if used)
- profile_id/version (if used)
- calendar_logic_version (if used)
- standards_bundle_id/version (if used)
- contract_id/version(s) (for calls executed)

**Active targets**
- active_wp_id (current WP)
- active_doc_ids (if docs generated)
- active_export_ids (if exports generated)

**Staged artifacts**
- staged_task_set_id (or hash)
- staged_schedule_id (proposal reference)
- staged_export_request (if prepared but blocked by stamps)

Orchestration is responsible for ensuring that the required stamp set is known before any regulated output.

### 3.3 Deterministic Decision Policy
- When the user asks for an action and required inputs are missing, orchestration must request the missing inputs rather than guessing.
- When multiple presets/profiles match a query, orchestration must return CONFLICT and request selection.
- Any time a state transition can mutate truth, orchestration must request explicit confirmation.

---

## 4. Governance Gates (Canonical Flow Control)

### 4.1 Gate Definitions
Orchestration enforces the following gates as mandatory steps:

1) **GATE-Stage**
- Purpose: assemble candidate tasks and metadata without allocating IDs.
- Entry condition: WP exists (or WP_CREATE requested).
- Output: staged task set (PROPOSED).

2) **GATE-Commit**
- Purpose: allocate task IDs and write WP truth.
- Entry condition: staged task set exists and user confirmed.
- Output: committed task rows in WP (COMMITTED).

3) **GATE-Plan**
- Purpose: compute PROPOSED schedule using Planning.
- Entry condition: committed tasks exist OR user requests advisory planning on staged set (policy choice).
- Output: schedule proposal (PROPOSED).

4) **GATE-Apply**
- Purpose: apply PROPOSED schedule to WP task fields (dates).
- Entry condition: schedule proposal exists and user confirmed.
- Output: WP task dates updated (COMMITTED) with provenance stamps recorded.

5) **GATE-Export**
- Purpose: generate report/export artifacts.
- Entry condition: required traceability stamps available.
- Output: exported artifact with stamps.

### 4.2 Mandatory Confirmations
Before any COMMIT or APPLY action, orchestration must ask:
- “Confirm commit staged tasks to WP### (Yes/No).”
- “Confirm apply schedule proposal to WP### (Yes/No).”

If user says No → remain PROPOSED; do not mutate WP truth.

---

## 5. Contract Registry and Routing

### 5.1 Contract Registry
Orchestration maintains a registry of known contracts and supported major versions:
- VALOR-contract-orch-wp
- VALOR-contract-orch-plan
- VALOR-contract-orch-ks
- VALOR-contract-orch-doc
- VALOR-contract-orch-rpt

Routing rule:
- Orchestration may invoke a contract only if it supports the MAJOR version required by the target subsystem.
- If not supported → CONFLICT / UNSUPPORTED_MAJOR_VERSION.

### 5.2 Canonical Action Envelope (Orchestration Output)
All calls must use the SoS envelope (A01). Orchestration is responsible for:
- selecting contract + version,
- selecting action_type,
- populating payload from validated user inputs and session context,
- setting options (dry_run, return_full_wp).

Example:
```json
{
  "contract": "VALOR-contract-orch-wp",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000120",
  "action_type": "WP_STAGE_TASKS",
  "mode": "M2",
  "target": {"wp_id": "WP-0007"},
  "payload": {
    "preset_id": "PRESET-PE-HIGH",
    "preset_version": "v1.0.1",
    "selection_context": {"equipment_type": "Process Equipment", "complexity": "High"}
  },
  "options": {"dry_run": false},
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 5.3 Action Routing Rules (Implementation Guidance)
- WP object creation/update → WP System.
- Task suggestion and metadata enrichment → Task Pool + Preset + Profile (read), then stage via WP.
- Planning → Planning subsystem (advisory), then apply via WP.
- Templates/standards → K&S (read).
- Document generation → Doc Factory, with WP truth + template references.
- Export/report → Reporting, with WP truth + stamp set.

---

## 6. Traceability Context Propagation

### 6.1 What Must Be Propagated
Orchestration must propagate and/or store:
- IDs/versions of all governed assets used in a flow,
- calendar logic version used in scheduling,
- contract versions invoked,
- timestamps and action IDs for major lifecycle transitions.

### 6.2 Stamping Gate Enforcement
Before generating documents or exports, orchestration must validate that:
- preset_id/version is known (if preset-driven),
- profile_id/version is known,
- task_pool_id/version is known,
- calendar_logic_version is known.

If any missing → block export and return INVARIANT_VIOLATION / MISSING_TRACEABILITY_STAMPS.

---

## 7. Error Handling and Safe Failure

### 7.1 Standard Errors Orchestration Must Handle
- MODE_VIOLATION: guide user to correct mode or refuse.
- VALIDATION_ERROR: request missing fields.
- INVARIANT_VIOLATION: stop and explain hard rule.
- NOT_FOUND: offer list/search actions.
- CONFLICT: present choices and require user selection.
- UNSUPPORTED_OPERATION: explain scope limitation.
- INTERNAL_ERROR: fail safely; do not claim commit succeeded.

### 7.2 “Never Claim Success Without Proof”
If a contract call fails or is not executed:
- orchestration must not claim that the WP/document/export exists or was updated.

---

## 8. Minimal State Machine (Orchestration Perspective)
States (conceptual):
- S0: Idle (no active WP)
- S1: WP Selected/Created
- S2: Tasks Staged (PROPOSED)
- S3: Tasks Committed (COMMITTED)
- S4: Plan Proposed (PROPOSED schedule)
- S5: Plan Applied (COMMITTED dates)
- S6: Export Generated (artifact issued)

Transitions are gated by confirmations and invariant checks.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
