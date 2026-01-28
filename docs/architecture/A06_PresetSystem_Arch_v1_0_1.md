---
id: VALOR-block-A06-preset-system-architecture
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
  - VALOR-block-A05-task-pool-architecture
summary: "Block A06 — Preset System Architecture: versioned selectors that bind task pool + profile + standards bundle and define deterministic inclusion/exclusion and tailoring rules for staging CQV work packages."
acceptance_criteria:
  - Defines Preset System authority and boundaries (selectors only; does not own WP truth).
  - Defines Preset entity schema including bindings (task_pool/profile/standards bundle/calendar) and rule sets.
  - Defines deterministic selection and tailoring rules with precedence and conflict behavior.
  - Defines preset lifecycle/versioning and compatibility policy.
  - Defines contract actions for listing/reading/resolving presets and their error semantics.
  - Defines mandatory stamp propagation requirements for downstream subsystems.
---

# Preset System Architecture (Selectors + Binding Rules)

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
The Preset System (PS) provides **versioned, governed presets** that convert a high-level context (equipment domain + complexity + scope) into a fully specified “work recipe”:
- which task pool version to use,
- which profile version to use (durations/lead times defaults),
- which standards bundle and templates are in scope,
- which calendar logic version applies,
- which tasks are required/optional/inserted,
- which departments/roles are in scope.

Presets are the mechanism that makes Valor deterministic and auditable:
- presets are pinned by ID/version,
- outputs stamp preset_id/version as provenance.

PS is authoritative for:
- preset definitions and rules,
- binding references to governed assets (task pool/profile/bundle/calendar),
- deterministic tailoring decisions encoded as rules.

PS is not authoritative for:
- WP/task truth instances (WP System),
- schedule computation (Planning),
- document generation (Document Factory),
- reports/exports (Reporting).

---

## 2. Core Entities (Authoritative Data Model)

### 2.1 Preset
A Preset is a versioned selector + binding object.

Required fields:
- preset_id (string, stable)
- version (semver)
- revision_date (YYYY-MM-DD)
- name (string)
- description (string)
- applicability:
  - equipment_domain: ProcessEquipment | Utilities | Facility
  - complexity: Low | Medium | High
  - scope: SingleEquipment | Project
  - optional system_types (array; e.g., RollerCompactor, BlisterLine)
- bindings:
  - task_pool_ref: {task_pool_id, task_pool_version}
  - profile_ref: {profile_id, profile_version}
  - standards_bundle_ref: {bundle_id, bundle_version}
  - calendar_logic_ref: {calendar_id, calendar_version}
- rule_set (see §2.2)
- outputs:
  - default_doc_set (array of doc_types) (optional)
  - default_milestones (array) (optional)
- governance:
  - owner_function
  - change_control_ref (optional)
  - checksum (optional)

### 2.2 RuleSet (Tailoring Rules)
Rules define how to tailor the resolved task set and metadata.

A rule has:
- rule_id
- rule_type (enum): INCLUDE | EXCLUDE | OPTIONAL | INSERT | OVERRIDE | REQUIRE
- condition (boolean expression over selection_context)
- target (what it applies to)
- payload (rule action details)
- priority (integer; higher wins)
- rationale (string; mandatory for CQV auditability)

Example rule payloads:
- INCLUDE: include atomic_task_ids with tags
- EXCLUDE: remove atomic_task_ids
- INSERT: insert specific block tasks between phases
- OVERRIDE: override owner_role_default or duration_ref keys (not numeric values)
- REQUIRE: enforce presence of WP fields before commit/export

### 2.3 SelectionContext (Input to Preset Resolution)
Required fields:
- equipment_domain
- complexity
- scope
Optional:
- system_type
- departments_in_scope
- site_calendar_overrides
- vendor_model (local vs intercontinental) (optional)

---

## 3. Deterministic Resolution Model

### 3.1 Resolution Output
Resolving a preset produces a “Preset Resolution” object:
- preset_id/version
- bound asset refs (task pool/profile/bundle/calendar) — pinned
- resolved rule decisions (which rules fired)
- resolved task set constraints (e.g., “VMP required”)
- resolved departments/roles in scope
- stamp set to propagate downstream

### 3.2 Rule Precedence
Rule precedence is deterministic:
1) Higher priority wins
2) If same priority:
   - OVERRIDE > INSERT > INCLUDE/EXCLUDE > OPTIONAL
3) If still tied:
   - stable sort by rule_id

If two rules conflict and neither overrides the other deterministically:
- return CONFLICT and require explicit user decision or preset update.

### 3.3 No Numeric Durations in Presets
Presets may not embed numeric durations or lead times.
They reference governed profile keys only (A02 “versioned assets not embedded rules”).

---

## 4. Compatibility and Versioning Policy

### 4.1 Preset Immutability
- A preset version is immutable once published.
- Any change requires a new preset version.

### 4.2 Binding Compatibility
A preset version must only reference compatible asset versions:
- task pool version compatible with preset major version policy
- profile version compatible with task pool tasks (duration keys exist)
- standards bundle compatible with intended document set
- calendar version supported by planning/reporting logic

If bindings are incompatible:
- PS must fail with CONFLICT / BINDING_INCOMPATIBLE.

---

## 5. Preset-Driven CQV Scenarios (Canonical)

### 5.1 VMP Optional Predecessor Scenario
- Preset for Project scope:
  - includes VMP tasks
  - requires VMP approval before URS authoring
- Preset for SingleEquipment scope:
  - excludes VMP tasks
  - allows URS authoring first

### 5.2 High Complexity Process Equipment Scenario
- Includes vendor wait blocks (quotation, FAT scheduling)
- Includes procurement + lead-time tasks
- Includes RTM insertion block (mandatory)
- Binds to standards bundle for CQV process equipment

---

## 6. Preset System Contract (Implementation-Ready)

PS is invoked via `VALOR-contract-orch-ps`.

### 6.1 Actions
READ:
- PS_LIST_PRESETS (filters by applicability)
- PS_READ_PRESET (preset_id + version)

RESOLVE:
- PS_RESOLVE_PRESET
  - Inputs: selection_context + optional preferred preset_id/version
  - Output: pinned bindings + rule decisions + stamp set

VALIDATE:
- PS_VALIDATE_BINDINGS (check referenced assets exist and compatible)
- PS_VALIDATE_RULESET (check determinism and no contradictions)

### 6.2 Canonical Request Envelope (Resolve Preset)
```json
{
  "contract": "VALOR-contract-orch-ps",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000610",
  "action_type": "PS_RESOLVE_PRESET",
  "mode": "M2",
  "payload": {
    "selection_context": {
      "equipment_domain": "ProcessEquipment",
      "complexity": "High",
      "scope": "Project",
      "system_type": "BlisterLine"
    }
  },
  "options": {"require_exact_match": true},
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 6.3 Canonical Response Envelope
```json
{
  "contract": "VALOR-contract-orch-ps",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000610",
  "ok": true,
  "result": {
    "preset_id": "PRESET-PE-HIGH",
    "preset_version": "v1.0.1",
    "bindings": {
      "task_pool_ref": {"task_pool_id": "TP-CORE", "task_pool_version": "v1.0.1"},
      "profile_ref": {"profile_id": "PROF-PE-HIGH", "profile_version": "v1.0.1"},
      "standards_bundle_ref": {"bundle_id": "STD-BUNDLE-CQV", "bundle_version": "v1.0.1"},
      "calendar_logic_ref": {"calendar_id": "CAL-WORKWEEK", "calendar_version": "v1.0.1"}
    },
    "rules_fired": ["R-INS-RTM", "R-REQ-VMP"],
    "stamps": {
      "preset_id": "PRESET-PE-HIGH",
      "preset_version": "v1.0.1",
      "profile_id": "PROF-PE-HIGH",
      "profile_version": "v1.0.1",
      "task_pool_id": "TP-CORE",
      "task_pool_version": "v1.0.1",
      "calendar_logic_version": "v1.0.1",
      "standards_bundle_id": "STD-BUNDLE-CQV",
      "standards_bundle_version": "v1.0.1"
    }
  },
  "error": null
}
```

---

## 7. Error Semantics (Preset System)

Standard codes:
- VALIDATION_ERROR: invalid context, missing required fields
- NOT_FOUND: preset/version not found
- CONFLICT: ambiguous match, incompatible bindings, nondeterministic rules
- UNSUPPORTED_OPERATION: unsupported matching strategy
- INTERNAL_ERROR: unexpected

PS-specific subcodes:
- NO_MATCH
- MULTIPLE_MATCHES
- BINDING_INCOMPATIBLE
- RULESET_NONDETERMINISTIC
- RULE_CONTRADICTION

Example error:
```json
{
  "code": "CONFLICT",
  "subcode": "MULTIPLE_MATCHES",
  "message": "Multiple presets match selection context ProcessEquipment/High/Project.",
  "entity": "preset",
  "remediation": "Specify preset_id/version explicitly or refine selection context (system_type)."
}
```

---

## 8. Stamp Propagation Requirements
PS is responsible for producing the “stamp set” that Orchestration must carry into:
- WP staging/commit (store preset/profile/task_pool refs in WP metadata),
- Planning requests (profile + calendar versions),
- Document generation (template/bundle versions),
- Reporting exports (minimum stamp set enforced).

Failure mode prevention:
- If Orchestration cannot confirm stamp set, it must block exports (A02 INV-07).

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
