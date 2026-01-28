---
id: VALOR-arch-addendum-planning-invariants-ux
version: v1.0.1A
date: 2026-01-03
owner: Nexus
editor: VALOR DEV-TASK-FORCE
status: released
dependencies: []
summary: Hard invariants and UX contract for Plan Proposal vs Apply (commit) behavior.
acceptance_criteria:
  - Plan tasks produces a proposal only and does not mutate WP/task truth.
  - Apply Plan always requires explicit Yes/No confirmation and stamps Canvas on success.
  - Proposal remains visible after apply and is marked APPLIED.
---

# Planning Invariants & UX Contract

## 1) Definitions
- **Plan Proposal**: A computed schedule/assignment recommendation (not committed).
- **Apply Plan**: The only action that writes proposed dates/owners into WP/task truth.

## 2) Hard invariants
1. `Plan tasks <Start_Date>` MUST NOT:
   - write Start/Finish/Owner into WP/task truth,
   - stamp WP header,
   - change task IDs, WP IDs, or document IDs,
   - use mutation language (commit/apply/saved/updated records).

2. `Apply Plan PLAN### to WP###` MUST:
   - stop and ask: `Confirm apply PLAN### to WP###? (Yes/No)`
   - commit only after an explicit **Yes**.

3. If user answers **No**:
   - respond: `Cancelled. No changes committed.`
   - no truth changes.

## 3) Required UX outputs

### 3.1 On Plan Proposal
- Render a Canvas section:
  - `PLAN PROPOSAL (NOT COMMITTED) — PLAN###`
- Include:
  - Start Date
  - Assignment Method
  - Status = PROPOSED
  - Assumptions (short)
  - Proposal table: `Task ID | Proposed Owner | Start Date | Finish Date | Depends On`
- Chat must include:
  - `Plan proposal generated (not committed). Next → Apply Plan PLAN### to WP###`

### 3.2 On Apply Success
- Keep the proposal section in Canvas and update header to:
  - `PLAN PROPOSAL (APPLIED) — PLAN###`
- Update proposal status to: `APPLIED`
- Add applied stamp:
  - `Applied To — WP### [dd-mm-yyyy HH:MM Africa/Cairo]`
- Stamp WP header with:
  - `Plan Applied — PLAN### [dd-mm-yyyy HH:MM Africa/Cairo]`

## 4) Safety valve
If the user asks to “plan and apply” in one command:
- deny apply and instruct to run Apply separately.
