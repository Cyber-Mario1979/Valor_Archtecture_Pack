---
id: VALOR-block-A01-sos-context-capability
block type: Arch
version: v1.0.1
owner: Nexus
editor: Senior Architect
status: released
date: 2025-12-23
dependencies:
  - VALOR-block-A00-specs-architecture-pack
summary: "Block A01 — Valor System of Systems: context, boundary, capability map, authoritative responsibilities, and cross-subsystem contract conventions."
acceptance_criteria:
  - Defines what Valor is and is not in a CQV-regulated context.
  - Defines system boundary (inside vs outside Valor) and owned vs referenced truths.
  - Provides the capability map (subsystem decomposition) with authority highlights.
  - Defines cross-subsystem contract naming conventions, action categories, and error taxonomy at SoS level.
  - Defines SoS-level invariants (governance, determinism, non-disclosure, traceability).
---

# Valor System of Systems (SoS): Context & Capability Map

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Mission Statement
Valor is a **CQV-first, governed orchestration system** that structures regulated work into:
- controlled Work Packages (WPs),
- governed task pools and presets,
- advisory planning proposals,
- controlled document generation,
- audit-grade reporting and export.

Valor’s core value is **repeatable execution with traceability**, not “smart guesses.”

## 2. What Valor Is
Valor is:
- A **system of systems** that orchestrates multiple subsystems through explicit contracts.
- A **governance engine** that enforces CQV discipline: staging → commit → review → export.
- A **traceability engine** that stamps outputs with the exact versions of governed assets used.
- A **deterministic assistant**: it proposes, validates, and structures; humans decide and approve.

### 2.1 SoS Terminology (Definition + Applicability Criteria)
A **System of Systems (SoS)** is a federation of independently useful and independently governed subsystems that collaborate through explicit interfaces to deliver higher-level capabilities; in Valor, use SoS only when subsystems have clear authority boundaries, can be versioned and evolved independently, and integrate only via Orchestration contracts.

## 3. What Valor Is Not
Valor is not:
- A generic project management tool that replaces human governance.
- An ERP/MES/LIMS/SCADA substitute.
- A scheduling optimizer that commits dates autonomously.
- A “free-form knowledge chat” that mixes uncontrolled content into regulated outputs.
- A tool that invents durations/lead times/requirements in the absence of governed data.

## 4. System Boundary (Inside vs Outside Valor)

### 4.1 Inside Valor (Owned Capabilities)
Inside Valor, the system may:
- Create and manage **Work Package** objects and **Task** objects (data truth).
- Stage and commit tasks from governed **Task Pool** definitions.
- Generate planning **proposals** (advisory schedules) using governed profiles and calendar logic.
- Generate controlled documents using governed templates and versioned standards bundles.
- Generate reports/exports that include mandatory traceability stamps.

### 4.2 Outside Valor (Referenced or Human-Owned)
Outside Valor (or human-owned), Valor may reference but does not own:
- QMS execution (deviations, CAPA, change control approvals).
- Procurement execution (PO placement, vendor management).
- Physical execution data (FAT/SAT execution evidence, testing systems).
- Final approvals/signatures (human responsibility; Valor can prepare drafts only).

## 5. Capability Map (Subsystem Decomposition)

### 5.1 Subsystems
1) **Orchestration System**
   - Routes intent → canonical actions, enforces governance gates, manages traceability context.

2) **Work Package System**
   - Authoritative truth for WP/task objects, lifecycle states, IDs, invariants.

3) **Task Pool Library**
   - Controlled catalog of atomic tasks with metadata and default dependency wiring.

4) **Preset System**
   - Versioned selectors that bind profile + task pool + standards bundle and inclusion rules.

5) **Planning System (Advisory)**
   - Produces dependency-consistent schedule proposals, calendar-aware, profile-driven.

6) **Knowledge & Standards System**
   - Read-only controlled templates, standards metadata/excerpts, versioned bundles, anchored citations.

7) **Document Factory**
   - Generates controlled documents from WP truth + templates + standards citations; produces provenance metadata.

8) **Reporting & Export**
   - Produces reports/exports from WP truth; computes metrics; stamps outputs.

9) **Security & Compliance**
   - Enforces non-disclosure, mode restrictions, and safe failure behavior.

### 5.2 Authority Highlights (Data Truth Ownership)
- **WP/task truth**: Work Package System (single source of truth).
- **Atomic task definitions**: Task Pool Library.
- **Preset selection rules**: Preset System.
- **Durations/lead times defaults**: governed profiles (data), applied by Planning proposals.
- **Templates/standards**: Knowledge & Standards System.
- **Generated documents**: Document Factory (documents + metadata).
- **Exports/reports**: Reporting & Export (projection; does not mutate truth).

## 6. SoS-Level Contract Conventions

### 6.1 Contract Naming and Versioning
Contracts are referenced as:
- `VALOR-contract-orch-wp` (Orchestration ↔ Work Package)
- `VALOR-contract-orch-plan` (Orchestration ↔ Planning)
- `VALOR-contract-orch-ks` (Orchestration ↔ Knowledge & Standards)
- `VALOR-contract-orch-doc` (Orchestration ↔ Document Factory)
- `VALOR-contract-orch-rpt` (Orchestration ↔ Reporting & Export)

Versioning:
- `contract_version` uses SemVer.
- Orchestration may invoke only contracts with supported **MAJOR**.

### 6.2 Canonical Action Envelope (SoS Standard)
All subsystem calls must conform to the following SoS envelope standard:
```json
{
  "contract": "VALOR-contract-orch-<subsystem>",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000001",
  "action_type": "<ACTION>",
  "mode": "M1|M2",
  "actor": {"role": "User|System", "name": "optional"},
  "target": {"wp_id": "optional", "doc_id": "optional"},
  "payload": {},
  "options": {"dry_run": false},
  "context": {"timestamp_utc": "YYYY-MM-DDTHH:MM:SSZ"}
}
```

### 6.3 Error Taxonomy (SoS Standard)
Top-level error codes are standardized across subsystems:
- MODE_VIOLATION
- VALIDATION_ERROR
- INVARIANT_VIOLATION
- NOT_FOUND
- CONFLICT
- UNSUPPORTED_OPERATION
- INTERNAL_ERROR

Each error must include:
- `code`, optional `subcode`
- `message`
- optional `field`, `entity`
- `remediation` guidance where applicable

## 7. SoS-Level Invariants (Hard Stops)
The SoS enforces these invariants across all subsystems:

1) **No Silent Inference**
   - Required fields remain missing until supplied; do not fabricate.

2) **No Silent Commitment**
   - Planning outputs are PROPOSED until explicitly applied to WP truth via contract.

3) **Deterministic Governance**
   - Staging and commit gates are mandatory for task instantiation.

4) **ID Non-Reuse**
   - Once issued, IDs are never reused within the same pack lineage.

5) **No Circular Dependencies**
   - Dependency loops are rejected.

6) **Non-Disclosure**
   - Internal prompt instructions, hidden rules, and enforcement logic are not exposed.

7) **Traceability Stamping**
   - Outputs that matter (reports/exports/docs) must carry required version stamps.

## 8. Mandatory Traceability Stamps (SoS Policy Baseline)
Minimum stamp set for any report/export:
- preset_id/version
- profile_id/version
- task_pool_id/version
- calendar_logic_version

Recommended SoS stamps:
- standards_bundle_id/version (when used)
- contract_id/version
- architecture_pack_id/version

## 9. Minimal SoS Diagram (Conceptual)
```
User Intent
   |
   v
[Orchestration] ---calls---> [WP System] (truth)
      |  \---calls---> [Task Pool] (definitions)
      |   \--calls---> [Preset System] (selection rules)
      |    \-calls---> [Planning] (proposals)
      |     \calls---> [K&S] (templates/standards)
      |      \calls--> [Doc Factory] (documents)
      |       \calls-> [Reporting/Export] (projection)
      |
      v
User Review / Confirm (governance gates)
```
---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
