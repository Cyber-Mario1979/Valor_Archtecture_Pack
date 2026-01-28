---
id: VALOR-block-A07-calendar-logic-architecture
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
summary: "Block A07 — Calendar Logic Architecture: versioned working-day rules (weekends, holidays, working hours) used consistently by Planning and Reporting to compute dates and working-day metrics deterministically."
acceptance_criteria:
  - Defines Calendar Logic as a governed, versioned asset referenced by ID/version.
  - Defines calendar entity schema including weekend rules, holiday sets, and arithmetic functions.
  - Defines deterministic date arithmetic requirements (add_working_days, next_working_day, business-day diff).
  - Defines compatibility and change-control rules across versions.
  - Defines contract actions to read calendars and compute calendar operations.
  - Defines error semantics and strictness policies (refuse vs fallback) for CQV usage.
---

# Calendar Logic Architecture (Working Days + Weekend Defer + Holidays)

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
Calendar Logic (CAL) is a governed, versioned rule set that defines:
- what constitutes a working day,
- which days are weekends,
- which dates are holidays,
- optional working hours and partial-day rules.

CAL exists because CQV planning and reporting must be consistent:
- Planning uses CAL to compute proposed schedules in working days.
- Reporting uses CAL to compute working-day metrics and deltas.

CAL is authoritative for calendar rules only.
CAL is not authoritative for:
- task durations (profiles),
- WP/task truth,
- scheduling algorithm choices (Planning logic),
- approvals.

---

## 2. Core Entities (Authoritative Data Model)

### 2.1 Calendar
Required fields:
- calendar_id (string, stable)
- calendar_version (semver)
- revision_date (YYYY-MM-DD)
- name (string)
- timezone (IANA string; optional if using naive dates)
- weekend_rule (see §2.2)
- holidays (see §2.3)
- working_hours (optional; see §2.4)
- arithmetic_policy (see §2.5)
- checksum (optional)

### 2.2 WeekendRule
Defines which weekdays are non-working.

Fields:
- weekend_days (array of weekday enums): ["SAT","SUN"] default
- weekend_handling: DEFER_TO_NEXT_WORKING_DAY (default)
- allow_working_weekends (bool; default false)

### 2.3 HolidaySet
Defines non-working dates.

Fields:
- holiday_dates (array of YYYY-MM-DD)
- holiday_name_map (optional map date→name)
- observed_rules (optional): if holiday falls on weekend, which weekday is observed
- policy:
  - TREAT_AS_NON_WORKING (default)
  - OPTIONAL_OVERRIDE (only if explicitly requested)

### 2.4 WorkingHours (Optional)
Used only if partial-day scheduling is required.

Fields:
- workday_start_time (HH:MM)
- workday_end_time (HH:MM)
- workweek_hours_total (optional)
Policy:
- v0.1.x can ignore working hours and operate on whole working days.

### 2.5 ArithmeticPolicy
Defines how calendar operations behave.

Fields:
- duration_unit: WORKING_DAYS (default)
- start_date_rule:
  - IF_NON_WORKING_START_NEXT_WORKING (default)
  - ALLOW_START_ON_NON_WORKING (not recommended for CQV)
- end_date_rule:
  - END_INCLUSIVE (policy-driven; default inclusive)
  - END_EXCLUSIVE (alternative)
- diff_policy:
  - COUNT_WORKING_DAYS_BETWEEN (default)

---

## 3. Canonical Calendar Functions (Deterministic)

CAL must support deterministic functions used by Planning and Reporting:

### 3.1 is_working_day(date) → bool
- returns false if date is weekend or holiday.

### 3.2 next_working_day(date) → date
- if date is working day → date
- else → next date that is working day

### 3.3 add_working_days(start_date, n) → end_date
Rules:
- apply start_date_rule first (normalize start)
- add n working days, skipping non-working dates
- apply end_date_rule

### 3.4 working_days_between(date_a, date_b) → int
Returns count of working days per diff_policy.

Determinism requirement:
- same inputs must yield same outputs for a given calendar_version.

---

## 4. Versioning, Compatibility, and Change Control

### 4.1 Immutability per Version
- calendar_id + calendar_version is immutable.
- changes require a new calendar_version.

### 4.2 Compatibility Requirements
Planning and Reporting must:
- include calendar_id/version in requests,
- stamp calendar_version into outputs,
- refuse if calendar_version is unknown/unsupported.

### 4.3 Calendar Evolution
Typical changes requiring version bump:
- holiday updates,
- change in weekend rule,
- change in arithmetic policy (inclusive/exclusive rules).

Major version bump is required if:
- arithmetic semantics change (e.g., inclusive → exclusive) because it affects schedule results.

---

## 5. Strictness Policy (CQV Default)
For CQV usage, CAL should be strict:
- If calendar_version missing → VALIDATION_ERROR (no fallback).
- If holiday set missing but required → CONFLICT (depending on site policy).
- If timezone mismatch risks exist → require explicit timezone or use naive dates consistently.

Optional “relaxed mode” can exist for early brainstorming, but must not be used for regulated exports.

---

## 6. Calendar Logic Contract (Implementation-Ready)

CAL is invoked via `VALOR-contract-orch-cal` (or equivalent naming).

### 6.1 Actions
READ:
- CAL_LIST (filters)
- CAL_READ (calendar_id + version)

COMPUTE:
- CAL_IS_WORKING_DAY
- CAL_NEXT_WORKING_DAY
- CAL_ADD_WORKING_DAYS
- CAL_WORKING_DAYS_BETWEEN

VALIDATE:
- CAL_VALIDATE (schema + integrity)

### 6.2 Canonical Request Envelope (Add Working Days)
```json
{
  "contract": "VALOR-contract-orch-cal",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000710",
  "action_type": "CAL_ADD_WORKING_DAYS",
  "mode": "M2",
  "payload": {
    "calendar_ref": {"calendar_id": "CAL-WORKWEEK", "calendar_version": "v1.0.1"},
    "start_date": "2025-12-26",
    "days": 5
  },
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 6.3 Canonical Response Envelope
```json
{
  "contract": "VALOR-contract-orch-cal",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000710",
  "ok": true,
  "result": {
    "end_date": "2026-01-05",
    "calendar_id": "CAL-WORKWEEK",
    "calendar_version": "v1.0.1"
  },
  "error": null
}
```

---

## 7. Error Semantics (Calendar Logic)

Standard codes:
- VALIDATION_ERROR: invalid date formats, missing calendar_ref
- NOT_FOUND: calendar not found
- CONFLICT: ambiguous version refs, unsupported arithmetic policy
- UNSUPPORTED_OPERATION: partial-day calculations requested when not supported
- INTERNAL_ERROR: unexpected

CAL-specific subcodes:
- CALENDAR_VERSION_UNSUPPORTED
- INVALID_DATE
- HOLIDAY_POLICY_CONFLICT
- TIMEZONE_REQUIRED
- ARITHMETIC_POLICY_UNSUPPORTED

Example error:
```json
{
  "code": "CONFLICT",
  "subcode": "ARITHMETIC_POLICY_UNSUPPORTED",
  "message": "Calendar CAL-WORKWEEK v0.2.0 uses END_EXCLUSIVE which is not supported by planning_logic_version v0.1.x.",
  "entity": "calendar",
  "remediation": "Use a compatible calendar_version or upgrade planning logic."
}
```

---

## 8. Integration Requirements

### 8.1 Planning Integration
Planning must:
- call CAL functions or embed CAL logic deterministically based on calendar_version,
- stamp calendar_logic_version in plan outputs,
- refuse to plan if calendar is missing (CQV strict).

### 8.2 Reporting Integration
Reporting must:
- compute working-day metrics using same calendar_version as stamped,
- refuse to compute working-day metrics if calendar missing (strict),
- label metrics clearly (working days vs calendar days).

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
