---
id: VALOR-block-A04-4-planning-architecture
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
summary: "Block A04.4 — Planning System Architecture (Advisory): schedule proposal generation from WP truth + governed profiles + calendar logic; produces PROPOSED plans only and never commits truth."
acceptance_criteria:
  - Defines Planning’s advisory-only authority and non-ownership constraints.
  - Defines planning inputs/outputs, including required governed version stamps.
  - Defines the scheduling model (dependencies, working-day calendar rules, milestones).
  - Defines resource assignment as advisory suggestions (not authoritative allocations).
  - Defines contract actions and error semantics for planning requests.
  - Enforces proposal vs commitment boundary and determinism (A02).
---

# Planning System Architecture (Advisory)

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
The Planning System produces **PROPOSED schedules** for a Work Package by combining:
- WP truth (tasks, dependencies, constraints),
- governed profile data (durations, lead times, review/approval cycle assumptions),
- governed calendar logic (working days, weekends, holidays),
- optional resource availability hints.

Planning is **advisory**:
- It does not mutate WP truth.
- It does not allocate authoritative resource capacity.
- It does not “commit dates” without an explicit APPLY step executed via the WP System.

This implements A02 INV-02 (Proposal vs Commitment) and A03 (authority separation).

---

## 2. Boundary and Non-Ownership Rules

### 2.1 Planning Owns
Planning is authoritative for:
- the schedule computation algorithm definition (as a subsystem capability),
- the resulting plan **proposal object** and its internal provenance,
- validation results specific to scheduling (e.g., infeasible constraints).

### 2.2 Planning Does Not Own
Planning is not authoritative for:
- WP/task truth (task list, dependency graph, statuses),
- committed task dates (only WP owns committed_* fields),
- vendor lead-time truth (unless supplied as governed profile data or WP facts),
- approvals and governance decisions,
- export/report truth.

---

## 3. Planning Inputs (Canonical)

Planning must be invoked with explicit versioned inputs. If any required input is missing, Planning must refuse.

### 3.1 Required Inputs
- wp_id
- tasks snapshot (task_id, type/phase, status, dependency edges, duration inputs)
- dependency graph (FS baseline)
- **profile_ref**: {profile_id, profile_version}
- **calendar_logic_ref**: {calendar_id, calendar_version} (or calendar_logic_version)
- planning policy options (see §3.3)

### 3.2 Optional Inputs
- milestones (explicit milestone tasks or milestone markers)
- constraints:
  - earliest_start_date
  - must_finish_by_date (deadline)
  - fixed dates for certain tasks (locked tasks)
- resource hints:
  - role-based availability windows
  - max parallel tasks by role
- vendor/business wait rules (if modeled separately from durations):
  - e.g., “Quotation waiting time” as a VENDOR_WAIT task

### 3.3 Planning Policy Options (v0.1.x)
- dependency_types_allowed: ["FS"] (default)
- calendar_rule: WEEKENDS_OFF (default)
- holidays: optional list or calendar_id reference
- duration_unit: working_days (default)
- schedule_strategy:
  - ASAP (default) — earliest possible schedule respecting dependencies and calendar
  - ALAP (optional future) — latest possible schedule respecting deadline
- treat_missing_durations_as_error: true (default)
- locked_task_dates_policy: STRICT (default) — do not move locked tasks

---

## 4. Scheduling Model

### 4.1 Task Duration
Duration source precedence:
1) explicit task planned_duration_days (if set in WP truth)
2) profile default by task_type/phase (governed)
3) otherwise → VALIDATION_ERROR (no guessing)

Duration is expressed in **working days** under calendar rules (weekends/holidays deferred).

### 4.2 Dependencies
Baseline support:
- FS only (Finish-to-Start), lag_days >= 0

For each successor:
- earliest_start = max(predecessor_finish + lag) across all predecessors
- if locked_start_date exists, must satisfy constraint or raise CONFLICT

Cycle handling:
- If graph contains a cycle, Planning must return INVARIANT_VIOLATION / CYCLE_DETECTED (A02 INV-05).

### 4.3 Milestones
A milestone is modeled as either:
- a task with duration 0 (working days), or
- a named marker attached to a task boundary (finish/start)

Milestones must appear in schedule outputs and can be used for reporting.

### 4.4 Working Day Calendar Logic
Calendar logic must define:
- weekend rules (e.g., Sat/Sun non-working)
- optional holidays
- working-day arithmetic functions:
  - add_working_days(date, n)
  - next_working_day(date)
  - is_working_day(date)

Planning must include calendar_version in all outputs.

### 4.5 Resource Allocation (Advisory)
In v0.1.x, Planning may propose **resource assignments** as hints:
- assign owner_role per task (from WP truth or profile default)
- suggest smoothing rules:
  - max_parallel_by_role (optional)
  - soft constraints that can shift start dates

Important:
- Resource allocation is not authoritative.
- If resource constraints are provided and violate feasibility, Planning returns a warning or CONFLICT depending on strictness policy.

---

## 5. Planning Outputs

### 5.1 Plan Proposal Object
Planning returns a plan proposal with:
- plan_id (unique)
- wp_id
- computed task schedule:
  - proposed_start_date
  - proposed_end_date
  - critical_path_flag (optional)
  - slack_days (optional)
- milestone dates
- resource hints (optional)
- validation summary (errors/warnings)
- provenance stamps (mandatory)

### 5.2 Mandatory Provenance Stamps in Plan Output
Planning outputs must include:
- preset_id/version (if preset-driven input; may be null if not applicable)
- profile_id/version
- task_pool_id/version (if tasks originated from a task pool; may be null if unknown)
- calendar_logic_version (or calendar_id/version)
- planning_logic_version (this block’s version or planning engine version)
- contract_id/version used for the call

If any required stamp is missing at call time, Planning returns VALIDATION_ERROR.

### 5.3 Output Labeling Rule
All schedules produced by Planning are labeled:
- state: PROPOSED
- apply_required: true

---

## 6. Planning Contract (Implementation-Ready)

Planning is invoked via `VALOR-contract-orch-plan`.

### 6.1 Actions
READ/VALIDATE:
- PLAN_VALIDATE_INPUTS
- PLAN_VALIDATE_DEPENDENCIES
- PLAN_PREVIEW (dry-run)

GENERATE:
- PLAN_GENERATE (produce a plan proposal)

OPTIONAL (future):
- PLAN_OPTIMIZE_RESOURCES
- PLAN_COMPARE (compare two proposals)

### 6.2 Canonical Request Envelope
```json
{
  "contract": "VALOR-contract-orch-plan",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000230",
  "action_type": "PLAN_GENERATE",
  "mode": "M2",
  "target": {"wp_id": "WP-0007"},
  "payload": {
    "profile_ref": {"profile_id": "PROF-PE-HIGH", "profile_version": "v1.0.1"},
    "calendar_logic_ref": {"calendar_id": "CAL-WORKWEEK", "calendar_version": "v1.0.1"},
    "tasks": [
      {"task_id": "T-0001", "planned_duration_days": 10, "dependencies": []}
    ],
    "options": {
      "dependency_types_allowed": ["FS"],
      "duration_unit": "working_days",
      "schedule_strategy": "ASAP"
    }
  },
  "options": {"dry_run": false},
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 6.3 Canonical Response Envelope
```json
{
  "contract": "VALOR-contract-orch-plan",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000230",
  "ok": true,
  "result": {
    "plan_id": "PLAN-0003",
    "wp_id": "WP-0007",
    "state": "PROPOSED",
    "task_schedule": [
      {"task_id": "T-0001", "proposed_start_date": "2025-12-23", "proposed_end_date": "2026-01-06"}
    ],
    "stamps": {
      "profile_id": "PROF-PE-HIGH",
      "profile_version": "v1.0.1",
      "calendar_logic_version": "v1.0.1",
      "planning_logic_version": "v0.1.1"
    },
    "warnings": []
  },
  "error": null
}
```

---

## 7. Error Semantics (Planning)

Standard codes:
- VALIDATION_ERROR: missing durations, missing stamps, invalid date formats, invalid options
- INVARIANT_VIOLATION: dependency cycles, negative lag, attempt to commit truth
- MODE_VIOLATION: planning invoked in wrong mode (policy)
- NOT_FOUND: unknown profile/calendar references
- CONFLICT: locked date infeasible, ambiguous version_ref, incompatible constraints
- UNSUPPORTED_OPERATION: dependency type not allowed, unsupported strategy
- INTERNAL_ERROR: unexpected

Planning-specific subcodes:
- MISSING_DURATION
- CALENDAR_LOGIC_MISSING
- CALENDAR_VERSION_UNSUPPORTED
- CYCLE_DETECTED
- LOCKED_DATE_INFEASIBLE
- STAMPS_MISSING
- DEPENDENCY_TYPE_UNSUPPORTED

Example error:
```json
{
  "code": "VALIDATION_ERROR",
  "subcode": "MISSING_DURATION",
  "message": "Cannot plan: task T-0042 has no planned_duration_days and profile has no default for phase=RTM/type=REVIEW.",
  "entity": "task",
  "field": "planned_duration_days",
  "remediation": "Provide duration explicitly or update the profile defaults."
}
```

---

## 8. Integration with WP System (Apply Step)
Planning never writes committed dates. To make dates authoritative:

1) Orchestration requests PLAN_GENERATE (Planning returns PROPOSED schedule).
2) Orchestration presents proposal to user and requests confirmation.
3) If confirmed, Orchestration calls:
   - `WP_UPDATE_TASK_FIELDS` with committed_start_date/committed_end_date
   - includes provenance stamps (profile/calendar/task_pool/preset versions)
4) WP System writes committed dates as authoritative truth.

If the APPLY call fails, Orchestration must not claim success.

---

## 9. Determinism and Reproducibility Requirements
- Planning results must be reproducible given:
  - the same task snapshot,
  - the same dependency graph,
  - the same profile/calendar versions,
  - the same planning policy options.

If any input changes, a new plan_id must be generated.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
