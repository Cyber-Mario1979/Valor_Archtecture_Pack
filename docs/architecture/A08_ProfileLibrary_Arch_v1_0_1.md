---
id: VALOR-block-A08-profile-library-architecture
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
summary: "Block A08 — Profile Library Architecture: governed duration/lead-time matrices keyed by task semantics and context, providing deterministic defaults used by Planning and stamped into outputs."
acceptance_criteria:
  - Defines Profile Library as authoritative governed data for durations/lead times (not embedded in prompts/presets).
  - Defines Profile entity schema including keys, dimensions, and value semantics (working days vs calendar months).
  - Defines duration key mapping between atomic tasks and profile entries.
  - Defines governance/change control and versioning policy for profile updates.
  - Defines contracts for reading profiles and resolving duration values for tasks.
  - Defines error semantics for missing keys, incompatible units, and context conflicts.
---

# Profile Library Architecture (Durations + Lead Times Matrices)

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
The Profile Library (PROF) is a governed, versioned store of **planning data**:
- default task durations (authoring, review, approval, execution),
- vendor wait times (quotation, FAT scheduling),
- procurement cycle assumptions (PO processing),
- equipment manufacturing lead times,
- facility construction/install lead times (future).

This data must be governed because it directly impacts:
- schedule proposals,
- KPI calculations,
- report/export artifacts.

PROF is authoritative for:
- default duration/lead time values and their units,
- the dimensional model (what context dimensions exist),
- mapping rules (how to select the right value from context).

PROF is not authoritative for:
- WP/task truth values explicitly set by users (these override defaults),
- scheduling algorithm (Planning),
- calendar rules (Calendar Logic).

Alignment:
- A02 INV-01: no guessing; if profile key missing and no override, planning must fail.
- A02 “versioned assets”: durations must live here, not in prompts or presets.

---

## 2. Core Entities (Authoritative Data Model)

### 2.1 Profile
A Profile is a versioned matrix package.

Required fields:
- profile_id (string, stable)
- version (semver)
- revision_date (YYYY-MM-DD)
- name (string)
- description (string)
- applicability:
  - equipment_domain: ProcessEquipment | Utilities | Facility
  - complexity: Low | Medium | High
  - scope: SingleEquipment | Project
  - optional system_types
- dimensions (array of dimension definitions; see §2.2)
- entries (map of profile_key → ProfileEntry; see §2.3)
- unit_policy (see §2.4)
- governance:
  - owner_function
  - change_control_ref (optional)
  - checksum (optional)

### 2.2 Dimension Definition
Defines context axes used for selecting values.

Fields:
- name (e.g., phase, task_type, owner_role, system_type, vendor_model)
- allowed_values (array)
- required (bool)
- default_value (optional)

Recommended v0.1.x dimensions:
- phase
- task_type
- scope (SingleEquipment/Project)
- complexity (Low/Medium/High)
Optional:
- vendor_model (Local/Intercontinental)
- system_type

### 2.3 ProfileEntry
A profile entry maps a key to one or more context-specific values.

Fields:
- profile_key (string, stable)
- description (string)
- value_table (array of rows):
  - each row: {context_selector, value, unit}
- selection_priority (integer; default 0)
- notes (optional)

Context selector is a partial match object, e.g.:
```json
{"phase":"URS","task_type":"AUTHORING","complexity":"High"}
```

### 2.4 Unit Policy
Units must be explicit.

Allowed units:
- WORKING_DAYS (default for authoring/review/approval/execution)
- CALENDAR_DAYS (rare; must be explicit)
- CALENDAR_WEEKS
- CALENDAR_MONTHS (common for manufacturing lead times)
- CALENDAR_YEARS (rare)

Policy:
- Planning must not convert CALENDAR_MONTHS into WORKING_DAYS unless conversion rule is explicitly defined and approved.
- If conversion is required, it must be declared (e.g., 1 month = 30 calendar days) and stamped.

CQV default:
- Prefer WORKING_DAYS for internal work.
- Prefer CALENDAR_MONTHS for vendor manufacturing lead times (explicit).

---

## 3. Duration Key Mapping (Atomic Tasks → Profile Keys)

### 3.1 Why Keys Matter
Atomic tasks reference profile keys via `duration_ref.profile_key`. This is the controlled bridge:
- Task Pool defines “what tasks exist.”
- Profile defines “how long they typically take.”

### 3.2 Key Naming Convention (Recommended)
`<PHASE>_<TASKTYPE>_<SUBTYPE>_DUR`
Examples:
- URS_AUTHORING_DUR
- URS_REVIEW_DUR
- URS_APPROVAL_DUR
- RTM_CYCLE_DUR
- QUOTATION_WAIT_DUR
- MANUFACTURING_LEADTIME_BLISTERLINE

Keys must be stable across versions; meaning changes require version bump, not key redefinition.

### 3.3 Overrides
If WP/task instance has an explicit planned_duration_days:
- it overrides profile-derived default for that task only.
- RPT should report both “default” and “overridden” status where useful.

---

## 4. Selection Logic (How a Value Is Picked)

Given:
- profile_id/version
- profile_key
- selection_context (equipment_domain, complexity, scope, system_type, vendor_model, etc.)

Selection algorithm (deterministic):
1) Filter rows where selector matches all provided fields.
2) Choose the most specific match (highest number of matched fields).
3) If tie, choose highest selection_priority.
4) If still tie, deterministic tie-break by stable row ordering.
5) If no row matches → NOT_FOUND / PROFILE_KEY_VALUE_NOT_FOUND.

No guessing:
- If missing, the caller must provide an override or update the profile.

---

## 5. Governance and Change Control

### 5.1 Immutability per Version
- profile_id + version is immutable.
- any value changes → new version.

### 5.2 Change Control Expectations
Because this impacts CQV timelines:
- profile updates should be reviewed by owners (CQV/QA/Engineering as applicable),
- changes should reference rationale (e.g., “blister line lead time observed 6–8 months”).

### 5.3 Compatibility Checks
A profile version is compatible with a task pool version if:
- every atomic task duration_ref.profile_key exists in the profile, or
- atomic task is flagged “duration optional” and planning policy allows.

If incompatible:
- return CONFLICT / PROFILE_INCOMPATIBLE_WITH_TASK_POOL.

---

## 6. Profile Library Contract (Implementation-Ready)

PROF is invoked via `VALOR-contract-orch-prof`.

### 6.1 Actions
READ:
- PROF_LIST (filters by applicability)
- PROF_READ (profile_id + version)
- PROF_READ_KEYS (list keys + descriptions)

RESOLVE:
- PROF_RESOLVE_VALUE
  - Inputs: profile_ref + profile_key + selection_context
  - Output: value + unit + match rationale

VALIDATE:
- PROF_VALIDATE_PROFILE (schema + integrity)
- PROF_VALIDATE_COMPATIBILITY (profile_ref + task_pool_ref)

### 6.2 Canonical Request (Resolve Value)
```json
{
  "contract": "VALOR-contract-orch-prof",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000810",
  "action_type": "PROF_RESOLVE_VALUE",
  "mode": "M2",
  "payload": {
    "profile_ref": {"profile_id": "PROF-PE-HIGH", "profile_version": "v1.0.1"},
    "profile_key": "RTM_CYCLE_DUR",
    "selection_context": {"complexity": "High", "scope": "Project", "vendor_model": "Intercontinental"}
  },
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 6.3 Canonical Response
```json
{
  "contract": "VALOR-contract-orch-prof",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000810",
  "ok": true,
  "result": {
    "profile_key": "RTM_CYCLE_DUR",
    "value": 30,
    "unit": "WORKING_DAYS",
    "match": {"matched_fields": ["complexity","scope","vendor_model"], "row_priority": 10}
  },
  "error": null
}
```

---

## 7. Error Semantics (Profile Library)

Standard codes:
- VALIDATION_ERROR: invalid context, invalid key format
- NOT_FOUND: profile not found, key not found
- CONFLICT: ambiguous match, incompatible units, compatibility failure
- UNSUPPORTED_OPERATION: unsupported unit conversions
- INTERNAL_ERROR: unexpected

PROF-specific subcodes:
- PROFILE_KEY_NOT_FOUND
- PROFILE_KEY_VALUE_NOT_FOUND
- MULTIPLE_EQUAL_MATCHES
- UNIT_CONVERSION_NOT_APPROVED
- PROFILE_INCOMPATIBLE_WITH_TASK_POOL

Example error:
```json
{
  "code": "NOT_FOUND",
  "subcode": "PROFILE_KEY_VALUE_NOT_FOUND",
  "message": "No value found for profile_key MANUFACTURING_LEADTIME_BLISTERLINE with context complexity=High/scope=Project.",
  "entity": "profile",
  "remediation": "Add a matching entry in the profile (new version) or override duration in the WP task."
}
```

---

## 8. Integration Requirements
- Task Pool atomic tasks reference profile keys; presets bind a profile version.
- Planning resolves durations using PROF and applies calendar logic where unit is WORKING_DAYS.
- Reporting stamps profile_id/version and should flag overridden durations.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
