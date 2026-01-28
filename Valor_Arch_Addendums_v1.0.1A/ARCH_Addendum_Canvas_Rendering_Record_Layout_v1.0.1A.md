---
id: VALOR-arch-addendum-canvas-rendering
version: v1.0.1A
date: 2026-01-03
owner: Nexus
editor: VALOR DEV-TASK-FORCE
status: released
dependencies: []
summary: Canonical Canvas rendering layout for WP truth, Task truth, and Plan proposals (document-like, not code blocks).
acceptance_criteria:
  - WP/Task truth uses bullet-per-field layout with arrow markers.
  - Missing values are blank after arrow (never 'No Entry').
  - Preset staging shows descriptions only; structured task fields appear only after explicit add.
  - Plan proposals persist and switch to APPLIED after commit.
---

# Canvas Rendering & Record Layout Contract

## 1) Global rules
- Canvas is the **truth view** for WP/task/doc records.
- Never render Canvas truth in fenced code blocks.
- Missing values render as **blank after the arrow** (e.g., `**Title** ➡️ `). Do not print `No Entry`.

## 2) Work Package (WP) Canvas layout

### 2.1 Title (first line)
`Work Package WP###`

### 2.2 Header fields (exact order; one bullet per field)
- **Work Package ID** ➡️ WP###
- **Title** ➡️
- **Area** ➡️
- **Scope** ➡️
- **Objective** ➡️
- **Governance** ➡️
- **Status** ➡️ Opened

### 2.3 Optional stamps
- **Plan Applied** ➡️ PLAN### [dd-mm-yyyy HH:MM Africa/Cairo]

## 3) Tasks section

### 3.1 Tasks header
`**Tasks**`

- If none: `- No tasks created yet.`

### 3.2 Structured task record (canonical)
- **Task ID** ➡️ WP###-T###
  - **Description** ➡️
  - **Owner** ➡️
  - **Start Date** ➡️
  - **Finish Date** ➡️
  - **Status** ➡️ Opened
  - **Depends On** ➡️ —

## 4) Preset staging visibility
- After `Use Preset WP <code>`:
  - WP Canvas must still show `Tasks` = none (`No tasks created yet.`).
  - Staged items are **descriptions-only** and are displayed in chat as:

**STAGED TASKS (NOT COMMITTED) — WP###**
1. <description>
2. <description>

- Structured tasks (IDs + fields) are created only after:
  - `Add Suggested Tasks WP###`

## 5) Plan Proposal section
- Proposal block appears in WP Canvas when planning occurs:
  - `PLAN PROPOSAL (NOT COMMITTED) — PLAN###`
- After apply, proposal remains and becomes:
  - `PLAN PROPOSAL (APPLIED) — PLAN###`
