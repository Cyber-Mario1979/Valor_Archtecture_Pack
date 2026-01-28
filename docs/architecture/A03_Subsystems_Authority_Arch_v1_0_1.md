---
id: VALOR-block-A03-subsystems-authority
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
summary: "Block A03 — Subsystems overview and authority matrix defining data truth ownership, allowed operations, and integration responsibilities across Valor."
acceptance_criteria:
  - Enumerates all Valor subsystems and their primary responsibilities.
  - Defines authoritative ownership (data truth) for each governed asset type.
  - Defines allowed operation classes per subsystem (read, stage, commit, generate, export).
  - Defines “does not own” constraints to prevent hidden coupling.
  - Provides a cross-subsystem integration map (who calls whom, and why).
---

# Subsystems Overview + Authority Matrix

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Subsystem List (Canonical)
Valor is a system of systems composed of the following subsystems:

1) Orchestration System  
2) Work Package System (WP)  
3) Task Pool Library (TP)  
4) Preset System (PS)  
5) Planning System (PLAN) — advisory  
6) Knowledge & Standards System (K&S) — read-only governed content  
7) Document Factory (DOC) — generated documents + provenance  
8) Reporting & Export (RPT) — projection + exports  
9) Security & Compliance (SEC) — enforcement constraints  

This block defines:
- what each subsystem is responsible for,
- what each subsystem is authoritative for (truth ownership),
- what each subsystem must never do (non-ownership rules),
- how subsystems integrate via contracts.

---

## 2. Authority Matrix (Data Truth Ownership)

### 2.1 Governed Asset Types
The core governed asset types are:
- Work Package (WP) and Task objects
- Task Pool definitions (atomic tasks)
- Presets (selectors/binders)
- Profiles (matrix data packages)
- Calendar Logic (working days/holidays rule sets)
- Standards Bundles and Templates (K&S assets)
- Generated Documents and Document Metadata (DOC outputs)
- Reports/Exports and computed metrics (RPT outputs)
- Contracts (action sets and envelopes; SoS policy + subsystem definitions)

### 2.2 Ownership Table
| Asset / Truth | Authoritative Owner | Notes |
|---|---|---|
| Work Package object | WP System | Single source of truth for WP fields, lifecycle, IDs |
| Task object | WP System | Single source of truth for task rows, dependencies, statuses, dates (when applied) |
| Dependency graph validity | WP System | Cycle checks, schema checks, allowed dependency types |
| Task Pool (atomic tasks) | Task Pool Library | Definitions + metadata + default wiring |
| Preset definitions | Preset System | References profile/task pool/standards bundle versions |
| Profiles (durations/lead times defaults) | Profile Library (governed data) | Applied by Planning; not invented by prompts |
| Calendar logic | Calendar Logic Asset | Used by Planning + Reporting; versioned and stamped |
| Standards bundles | K&S | Versioned sets of standards/templates for stamping |
| Templates | K&S | Controlled scaffolds consumed by Document Factory |
| Generated documents | Document Factory | Owns document outputs + provenance metadata |
| Document metadata registry | Document Factory (or WP if attached) | Metadata is produced by DOC; WP stores references |
| Reports/exports | Reporting & Export | Projection only; cannot mutate WP truth |
| Traceability stamps policy | Orchestration (policy) + RPT/DOC (enforcement) | Orchestration gates; outputs enforce |
| Security constraints | SEC | Non-disclosure, mode restrictions, safe failure |

---

## 3. Allowed Operation Classes by Subsystem

### 3.1 Operation Classes
- READ: retrieve objects/metadata without mutation
- STAGE: prepare suggestions or drafts without allocating IDs or committing truth
- COMMIT: create or mutate authoritative truth objects (IDs may be allocated)
- GENERATE: create derived artifacts (documents/reports/exports) without mutating upstream truth
- VALIDATE: run rule checks and return errors/warnings
- STAMP: attach required traceability and provenance metadata

### 3.2 Operations Table
| Subsystem | READ | STAGE | COMMIT | GENERATE | VALIDATE | STAMP |
|---|---:|---:|---:|---:|---:|---:|
| Orchestration | Yes | Yes (intent normalization) | No (by itself) | No (delegates) | Yes (pre-checks) | Yes (policy) |
| WP System | Yes | Yes (stage tasks) | Yes (commit tasks/updates) | No | Yes | No (stores stamp references if provided) |
| Task Pool Library | Yes | No | Yes (library updates across releases only) | No | Yes (library integrity) | No |
| Preset System | Yes | No | Yes (preset updates across releases only) | No | Yes | No |
| Planning | Yes (inputs) | No | No | Yes (plans) | Yes | Yes (includes calendar/profile version in results) |
| K&S | Yes | No | No | No | Yes | Yes (anchors/versions in responses) |
| Document Factory | Yes (inputs) | Yes (draft) | No (approvals) | Yes (documents) | Yes | Yes (provenance stamps) |
| Reporting & Export | Yes | No | No | Yes (reports/exports) | Yes | Yes (traceability stamps) |
| Security & Compliance | Yes | No | No | No | Yes | No |

Key rule:
- Only the WP System may COMMIT WP/task truth.
- Planning and Reporting may GENERATE only; they must never COMMIT upstream truth.

---

## 4. “Does Not Own” Constraints (Anti-Coupling Rules)

### 4.1 Orchestration
Does not own:
- WP/task data truth
- scheduling truth
- document content truth

Must:
- request mutations via contracts only
- enforce governance gates and stamping policy

### 4.2 Planning
Does not own:
- WP/task truth
- approval decisions
- standards/templates

Must:
- return PROPOSED schedules
- require calendar logic and profile versions
- reject invalid dependency graphs

### 4.3 Reporting & Export
Does not own:
- WP/task truth
- template truth
- planning truth

Must:
- project and compute metrics deterministically
- stamp outputs with required stamps
- refuse exports if stamps missing

### 4.4 K&S
Does not own:
- WP/task truth
- approvals
- generated documents

Must:
- remain read-only in-session
- provide anchored, versioned references

---

## 5. Integration Map (Who Calls Whom)

### 5.1 Canonical Call Graph
- User → Orchestration (intent)
- Orchestration → WP System (create/update/stage/commit/validate)
- Orchestration → Preset System (read preset definition)
- Orchestration → Task Pool Library (read task definitions)
- Orchestration → Planning (compute PROPOSED schedules)
- Orchestration → K&S (read templates/standards bundles)
- Orchestration → Document Factory (generate docs + provenance)
- Orchestration → Reporting & Export (generate report/export + stamps)
- Orchestration → SEC (enforce restrictions)

### 5.2 Why Orchestration Is Central
Orchestration is the only component with enough context to:
- coordinate multi-step flows (stage → commit → plan → apply → export),
- enforce cross-subsystem invariants (A02),
- carry traceability context across calls.

---

## 6. Practical Implications (Implementation Guidance)

### 6.1 Preventing “Prompt Drift”
To prevent silent drift in regulated logic:
- task pools, presets, profiles, and calendar logic must live as versioned assets,
- prompts reference IDs/versions only,
- reports/exports must stamp these versions.

### 6.2 Preventing “Shadow Truth”
Avoid “truth in text”:
- textual summaries are not authoritative unless reflected in WP objects.
- planning outputs are not authoritative unless applied to WP task fields.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
