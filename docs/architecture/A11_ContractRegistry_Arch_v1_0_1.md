---
id: VALOR-block-A11-contract-registry-architecture
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
  - VALOR-block-A04-1-orchestration-architecture
summary: "Block A11 — Contract Registry Architecture: canonical contract IDs, versioning strategy, action envelopes, compatibility policy, and validation rules enabling Orchestration to coordinate subsystems deterministically."
acceptance_criteria:
  - Defines what a contract is in Valor and why contracts are mandatory.
  - Defines canonical contract identifiers, action catalogs, and per-contract versioning rules (SemVer).
  - Defines the standard envelope schema and required fields (traceability-aware).
  - Defines compatibility policy (major/minor/patch behavior) and negotiation rules.
  - Defines validation, error semantics, and fail-safe behaviors for contract invocation.
  - Defines a registry metadata schema for documenting contracts in the pack.
---

# Contract Registry Architecture (IDs + Versioning + Envelopes + Compatibility)

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose
Contracts are the formal interface between Valor subsystems. They exist to:
- prevent hidden coupling,
- enforce governance and safety invariants,
- guarantee deterministic behavior and auditability,
- enable a “system of systems” to evolve without constant rewrites.

Orchestration may only interact with subsystems via contracts. If a behavior cannot be expressed as a contract action, it is not allowed.

---

## 2. What a Contract Is (Canonical Definition)
A contract is a versioned specification containing:
- contract_id and contract_version (SemVer),
- an action catalog (action_type list) with required/optional fields,
- request/response envelope schemas,
- validation rules and error taxonomy,
- invariants that must be enforced by the contract implementer,
- stamp propagation requirements (when relevant).

A contract is not:
- a prompt narrative,
- a hidden rules list,
- an informal “workflow description” without schema.

---

## 3. Canonical Contract IDs (Registry Standard)

### 3.1 System-of-Systems Contracts (Core)
- `VALOR-contract-orch-wp` — Orchestration ↔ Work Package System
- `VALOR-contract-orch-plan` — Orchestration ↔ Planning (Advisory)
- `VALOR-contract-orch-doc` — Orchestration ↔ Document Factory
- `VALOR-contract-orch-rpt` — Orchestration ↔ Reporting & Export
- `VALOR-contract-orch-ks` — Orchestration ↔ Knowledge & Standards

### 3.2 Data Asset Contracts (Support)
- `VALOR-contract-orch-tp` — Orchestration ↔ Task Pool Library
- `VALOR-contract-orch-ps` — Orchestration ↔ Preset System
- `VALOR-contract-orch-prof` — Orchestration ↔ Profile Library
- `VALOR-contract-orch-cal` — Orchestration ↔ Calendar Logic

### 3.3 Security/Policy Contracts (Optional)
- `VALOR-contract-orch-sec` — Orchestration ↔ Security & Compliance checks (if separated)

---

## 4. SemVer Rules (Compatibility Policy)

### 4.1 Contract Versioning
Contracts use SemVer: MAJOR.MINOR.PATCH

- **MAJOR**: breaking changes (schema changes, renamed fields, action semantics changes)
- **MINOR**: backward-compatible additions (new optional fields, new actions)
- **PATCH**: bug fixes / clarifications with no behavior change required

### 4.2 Compatibility Requirements
Orchestration must:
- accept MINOR/PATCH upgrades within the same MAJOR,
- refuse incompatible MAJOR versions unless explicitly upgraded.

Subsytems must:
- reject requests using unsupported MAJOR versions,
- return CONFLICT / UNSUPPORTED_MAJOR_VERSION.

### 4.3 Negotiation Policy (Implementation Guidance)
Orchestration selects the highest supported MINOR within the required MAJOR.
If a subsystem returns a “supported_versions” list, orchestration may choose the best match deterministically.

---

## 5. Standard Envelope Schema (All Contracts)

### 5.1 Request Envelope (Canonical)
Required fields:
- contract (string)
- contract_version (string)
- action_id (string)
- action_type (string)
- mode (M1|M2)
- payload (object)
- context (object with timestamp_utc)

Optional fields:
- actor (role/name)
- target (wp_id/task_id/doc_id/artifact_id)
- options (dry_run, return_content, strict, etc.)

Canonical structure:
```json
{
  "contract": "VALOR-contract-orch-wp",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000001",
  "action_type": "WP_STAGE_TASKS",
  "mode": "M2",
  "actor": {"role": "User", "name": "optional"},
  "target": {"wp_id": "WP-0007"},
  "payload": {},
  "options": {"dry_run": false},
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 5.2 Response Envelope (Canonical)
Required fields:
- contract
- contract_version
- action_id
- ok (bool)
- result (object|null)
- error (object|null)

Canonical structure:
```json
{
  "contract": "VALOR-contract-orch-wp",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000001",
  "ok": true,
  "result": {},
  "error": null
}
```

---

## 6. Stamp Propagation in Contracts

### 6.1 Stamp Requirements by Contract Category
- WP contract: stores preset/profile/task_pool/calendar refs in WP metadata; enforces staging/commit boundaries.
- PLAN contract: requires profile+calendar refs and returns stamps + planning_logic_version.
- DOC contract: requires stamps + template/bundle refs; returns provenance metadata.
- RPT contract: requires minimum stamps; returns schema_version + stamps.

### 6.2 Stamp Validation Rule (Global)
For any action that generates regulated outputs (DOC_FINALIZE, RPT_GENERATE_EXPORT, etc.):
- missing stamp set → INVARIANT_VIOLATION / MISSING_TRACEABILITY_STAMPS.

---

## 7. Action Catalog Structure (Per Contract)

Each contract must define:
- action_type name
- allowed modes
- required payload fields
- validation rules
- result schema (what success returns)
- side-effect classification:
  - READ_ONLY
  - STAGE_ONLY
  - MUTATES_TRUTH
  - GENERATES_ARTIFACT

Example (WP contract snippet):
- WP_GET — READ_ONLY
- WP_STAGE_TASKS — STAGE_ONLY
- WP_COMMIT_STAGED_TASKS — MUTATES_TRUTH
- WP_UPDATE_TASK_FIELDS — MUTATES_TRUTH

This classification is used by SEC and Governance to enforce gates.

---

## 8. Validation and Guardrails

### 8.1 Pre-Call Validation (Orchestration)
Orchestration must validate:
- contract is known,
- contract_version is supported,
- action_type exists in catalog,
- required fields are present,
- mode is permitted,
- if action is MUTATES_TRUTH, confirmation must be recorded.

### 8.2 Subsystem Validation (Implementer)
Subsystems must validate:
- schema correctness,
- invariants relevant to the domain (cycles, stamps, immutability),
- and must fail closed on missing required fields.

### 8.3 Idempotency Guidance
Actions should specify idempotency where relevant:
- READ actions: idempotent
- STAGE actions: idempotent if same inputs produce same staged hash
- COMMIT actions: either:
  - idempotent via staged_task_set_id (commit once), or
  - returns CONFLICT if already committed

---

## 9. Error Semantics (Contract-Level)

Standard codes (A01):
- MODE_VIOLATION
- VALIDATION_ERROR
- INVARIANT_VIOLATION
- NOT_FOUND
- CONFLICT
- UNSUPPORTED_OPERATION
- INTERNAL_ERROR

Contract-specific subcodes include:
- CONTRACT_NOT_REGISTERED
- ACTION_TYPE_UNKNOWN
- CONTRACT_VERSION_UNSUPPORTED
- UNSUPPORTED_MAJOR_VERSION
- PAYLOAD_SCHEMA_MISMATCH
- CONFIRMATION_REQUIRED

Example error:
```json
{
  "code": "CONFLICT",
  "subcode": "CONTRACT_VERSION_UNSUPPORTED",
  "message": "Requested contract_version v2.0.0 is not supported. Supported: v1.0.1–v0.4.x.",
  "entity": "contract",
  "remediation": "Use a supported version or upgrade the orchestration contract registry."
}
```

---

## 10. Contract Registry Metadata Schema (Documentation in Pack)

Each contract entry in the registry must include:
- contract_id
- current_version
- supported_versions
- owner_subsystem
- action_catalog (list)
- schema_refs (JSON schema files if available)
- change_log (top appended)
- dependencies (other contracts or asset schemas)

This enables:
- reproducible builds,
- audit trace (“which contract version governed this export”),
- safer evolution.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
