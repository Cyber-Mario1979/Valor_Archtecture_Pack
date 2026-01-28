---
id: VALOR-block-A14-inv-reference-index
block type: Arch
version: v1.0.1
owner: Nexus
editor: Senior Architect
status: released
date: 2025-12-23
dependencies:
  - VALOR-block-A00-specs-architecture-pack
  - VALOR-block-A02-principles-invariants
summary: "Master index of all INV-xx references across the architecture pack for validation and tooling checks."
acceptance_criteria:
  - Lists every INV-xx reference with file and line number.
---
# INV Reference Index (v1.0.1)

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.

This index enumerates every occurrence of `INV-xx` across the v1.0.1 architecture pack (line numbers are 1-based).

| INV | File | Line | Context |
|---|---|---:|---|
| INV-01 | A02_Principles_Invariants_Arch_v1_0_1.md | 86 | ### INV-01: No Silent Inference |
| INV-01 | A02_Principles_Invariants_Arch_v1_0_1.md | 238 | - Pre-call validation for required fields (INV-01). |
| INV-01 | A02_Principles_Invariants_Arch_v1_0_1.md | 246 | - Schema validation + required fields for readiness transitions (INV-01). |
| INV-01 | A08_ProfileLibrary_Arch_v1_0_1.md | 54 | - A02 INV-01: no guessing; if profile key missing and no override, planning must fail. |
| INV-02 | A02_Principles_Invariants_Arch_v1_0_1.md | 101 | ### INV-02: Proposal vs Commitment Boundary |
| INV-02 | A02_Principles_Invariants_Arch_v1_0_1.md | 240 | - Proposal vs commitment gating (INV-02). |
| INV-02 | A02_Principles_Invariants_Arch_v1_0_1.md | 254 | - Label all plans as PROPOSED unless applied (INV-02). |
| INV-02 | A04_4_Planning_Arch_v1_0_1.md | 42 | This implements A02 INV-02 (Proposal vs Commitment) and A03 (authority separation). |
| INV-03 | A02_Principles_Invariants_Arch_v1_0_1.md | 117 | ### INV-03: Staging Before Commit (Task Creation Gate) |
| INV-03 | A02_Principles_Invariants_Arch_v1_0_1.md | 239 | - Staging/commit gate flows (INV-03). |
| INV-03 | A02_Principles_Invariants_Arch_v1_0_1.md | 249 | - Reject direct task creation when staging required (INV-03). |
| INV-03 | A04_2_WorkPackage_Arch_v1_0_1.md | 133 | - Cannot commit without staging (A02 INV-03). |
| INV-04 | A02_Principles_Invariants_Arch_v1_0_1.md | 131 | ### INV-04: ID Non-Reuse |
| INV-04 | A02_Principles_Invariants_Arch_v1_0_1.md | 247 | - ID allocation with no reuse (INV-04). |
| INV-04 | A04_2_WorkPackage_Arch_v1_0_1.md | 159 | Invariant (A02 INV-04): |
| INV-05 | A02_Principles_Invariants_Arch_v1_0_1.md | 144 | ### INV-05: No Circular Dependencies |
| INV-05 | A02_Principles_Invariants_Arch_v1_0_1.md | 248 | - Cycle detection for dependencies (INV-05). |
| INV-05 | A02_Principles_Invariants_Arch_v1_0_1.md | 253 | - Reject cycles or inconsistent dependencies (INV-05). |
| INV-05 | A04_2_WorkPackage_Arch_v1_0_1.md | 171 | Invariant (A02 INV-05): |
| INV-05 | A04_4_Planning_Arch_v1_0_1.md | 120 | - If graph contains a cycle, Planning must return INVARIANT_VIOLATION / CYCLE_DETECTED (A02 INV-05). |
| INV-06 | A02_Principles_Invariants_Arch_v1_0_1.md | 158 | ### INV-06: Calendar-Aware Date Arithmetic |
| INV-06 | A02_Principles_Invariants_Arch_v1_0_1.md | 252 | - Calendar logic version required (INV-06). |
| INV-06 | A02_Principles_Invariants_Arch_v1_0_1.md | 259 | - Consistent duration calculation aligned with calendar logic (INV-06). |
| INV-07 | A02_Principles_Invariants_Arch_v1_0_1.md | 173 | ### INV-07: Traceability Stamps Are Mandatory for Regulated Outputs |
| INV-07 | A02_Principles_Invariants_Arch_v1_0_1.md | 241 | - Output generation blocked without traceability stamps (INV-07). |
| INV-07 | A02_Principles_Invariants_Arch_v1_0_1.md | 257 | - Stamp requirements (INV-07). |
| INV-07 | A04_6_Reporting_Export_Arch_v1_0_1.md | 48 | - Mandatory stamps for regulated outputs (A02 INV-07) |
| INV-07 | A06_PresetSystem_Arch_v1_0_1.md | 293 | - If Orchestration cannot confirm stamp set, it must block exports (A02 INV-07). |
| INV-07 | A09_Governance_Branching_Arch_v1_0_1.md | 108 | - required stamps present (A02 INV-07), |
| INV-08 | A02_Principles_Invariants_Arch_v1_0_1.md | 192 | ### INV-08: Non-Disclosure of Internal Instructions |
| INV-08 | A02_Principles_Invariants_Arch_v1_0_1.md | 243 | - Non-disclosure policy (INV-08). |
| INV-09 | A02_Principles_Invariants_Arch_v1_0_1.md | 206 | ### INV-09: Reporting Is Projection Only |
| INV-09 | A02_Principles_Invariants_Arch_v1_0_1.md | 258 | - Projection-only rule (INV-09). |
| INV-09 | A04_6_Reporting_Export_Arch_v1_0_1.md | 47 | - Projection-only (A02 INV-09) |
| INV-10 | A02_Principles_Invariants_Arch_v1_0_1.md | 219 | ### INV-10: Compatibility by Major Version |
| INV-10 | A02_Principles_Invariants_Arch_v1_0_1.md | 242 | - Contract major version compatibility (INV-10). |

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
