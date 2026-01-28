---
id: VALOR-block-A04-5-document-factory-architecture
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
  - VALOR-block-A12-knowledge-standards-architecture
summary: "Block A04.5 — Document Factory System Architecture: generates controlled CQV documents from WP truth + governed templates + standards citations, producing audit-grade provenance metadata without mutating WP truth."
acceptance_criteria:
  - Defines Document Factory’s authority and non-ownership boundaries.
  - Defines entities (Document, DocumentMetadata, CitationSet) and required metadata fields.
  - Defines generation pipeline (compose, validate, render, review-gate, finalize) with governance hooks.
  - Defines contract actions and response envelopes for document generation.
  - Enforces provenance stamping, anchored citations, and determinism requirements.
  - Defines error taxonomy and safe failure behavior suitable for CQV audit expectations.
---

# Document Factory System Architecture

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
The Document Factory (DOC) is the subsystem responsible for producing **controlled CQV documents** (drafts and finalized outputs) from:
- authoritative WP/task truth (WP System),
- governed templates (K&S),
- governed standards bundles and anchored citations (K&S),
- user-supplied project specifics (through WP fields or explicit inputs).

DOC is authoritative for:
- the produced document artifact content,
- its provenance metadata (what inputs and versions produced it),
- deterministic rendering and content assembly rules.

DOC is not authoritative for:
- WP/task truth (it reads; does not mutate),
- planning truth (it can embed proposals only if explicitly provided and labeled),
- approvals/signatures (human responsibility).

---

## 2. Boundary and Non-Ownership Rules

### 2.1 DOC Owns
- Document object lifecycle (draft → review-ready → finalized)
- Document content outputs (Markdown/PDF/Word if supported)
- Document metadata registry (doc_id, versions, stamps, citations, checksums)
- Validation rules specific to document completeness and template requirements

### 2.2 DOC Does Not Own
- WP/task truth (any change required must be requested via WP contract by Orchestration)
- Standards/template truth (read-only consumption from K&S)
- Export/report truth (RPT subsystem)
- Approvals and signatures (may provide signature blocks but cannot sign)

---

## 3. Core Entities (Authoritative Data Model)

### 3.1 Document
A Document is a generated artifact associated with a WP.

Required fields:
- doc_id (string, immutable)
- doc_type (enum): VMP | URS | RA | RTM | DQ | IQ | OQ | PQ | VSR | REPORT
- doc_version (string; semver or incrementing)
- wp_id (string)
- state (enum): DRAFT | REVIEW_READY | FINAL
- created_at_utc, updated_at_utc
- template_ref: {template_id, template_version}
- bundle_ref: {bundle_id, bundle_version} (if applicable)
- content_format (enum): MARKDOWN | DOCX | PDF (policy-dependent)
- content (string or binary reference)
- checksum (string) (for FINAL, mandatory)

### 3.2 DocumentMetadata (Provenance Record)
A provenance record is mandatory for audit-grade outputs.

Required fields:
- doc_id
- doc_version
- generation_action_id (ACT-*)
- generation_timestamp_utc
- inputs_snapshot:
  - wp_snapshot_hash
  - task_snapshot_hash (optional)
  - user_inputs_hash (optional)
- stamps (see §5)
- citations (see §3.3)
- validation_summary (errors/warnings)
- generator_version (doc_factory_version)

### 3.3 CitationSet (Anchored References)
Citations must be stable and anchored.

Citation item fields:
- asset_type: standard | template
- asset_id
- asset_version
- anchor_id
- anchor_title
- excerpt_policy: METADATA_ONLY | PUBLIC_EXCERPT | INTERNAL_ONLY
- retrieval_timestamp_utc (optional)

---

## 4. Document Lifecycle (Governance-Aligned)

### 4.1 States
- DRAFT: generated content intended for iterative editing
- REVIEW_READY: content passes completeness checks and is ready for formal review
- FINAL: content is finalized with checksum; further edits require new version

### 4.2 State Transitions
| From | To | Trigger | Gate |
|---|---|---|---|
| DRAFT | REVIEW_READY | DOC_VALIDATE + user request | template completeness pass |
| REVIEW_READY | FINAL | DOC_FINALIZE | explicit user confirmation + checksum created |
| FINAL | DRAFT (new version) | DOC_REGENERATE | creates doc_version increment |

Hard rule:
- FINAL documents are immutable; new changes require new doc_version.

---

## 5. Traceability and Stamping (Mandatory)

### 5.1 Required Stamp Set
A generated document must include, at minimum:
- preset_id/version (if preset-driven)
- profile_id/version (if schedule/durations referenced or required by template)
- task_pool_id/version (if tasks derived from task pool)
- calendar_logic_version (if any schedule/date arithmetic included)
- standards_bundle_id/version (if any standards referenced)
- template_id/version (always)
- doc_factory_version
- contract_id/version used for DOC call

### 5.2 Stamp Placement
DOC must ensure stamps appear in:
- document header (document control section)
- document metadata record

If a required stamp is missing, DOC must refuse generation with:
- INVARIANT_VIOLATION / MISSING_TRACEABILITY_STAMPS

---

## 6. Generation Pipeline (Implementation-Ready)

### 6.1 Pipeline Stages
1) **Resolve Inputs**
   - Fetch WP truth snapshot (WP_GET)
   - Fetch template (KS_READ_TEMPLATE)
   - Fetch standards bundle (KS_READ_BUNDLE) if applicable
   - Validate required inputs (template.required_inputs)

2) **Assemble Content**
   - Populate template placeholders using WP truth fields
   - Insert sections from task list if required (e.g., RTM trace table)
   - Insert citations or references using anchored citation objects

3) **Validate Completeness**
   - Ensure required sections populated
   - Ensure required citations present (if template mandates)
   - Ensure stamps present

4) **Render Output**
   - Generate Markdown (baseline)
   - If DOCX/PDF supported: render deterministically from Markdown/source blocks

5) **Review Gate**
   - Mark as REVIEW_READY only if validation passes

6) **Finalize**
   - Generate checksum
   - Lock as FINAL and store provenance metadata

### 6.2 Determinism Requirements
Given the same:
- WP snapshot,
- template version,
- bundle version,
- user inputs,
- DOC version,
the output must be the same (content + checksum).

---

## 7. Document Factory Contract (Implementation-Ready)

DOC is invoked via `VALOR-contract-orch-doc`.

### 7.1 Actions
- DOC_GENERATE_DRAFT
- DOC_VALIDATE
- DOC_MARK_REVIEW_READY
- DOC_FINALIZE
- DOC_REGENERATE (new version)
- DOC_GET (doc_id)
- DOC_LIST (filters by wp_id/doc_type/state)

### 7.2 Canonical Request Envelope (Generate Draft)
<!-- NOTE: Example is illustrative, not complete. Refer to schema for full structure. -->
```json
{
  "contract": "VALOR-contract-orch-doc",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000310",
  "action_type": "DOC_GENERATE_DRAFT",
  "mode": "M2",
  "target": {"wp_id": "WP-0007"},
  "payload": {
    "doc_type": "URS",
    "template_ref": {"template_id": "TPL-URS", "template_version": "v1.0.1"},
    "bundle_ref": {"bundle_id": "STD-BUNDLE-CQV", "bundle_version": "v1.0.1"},
    "stamps": {
      "preset_id": "PRESET-PE-HIGH",
      "preset_version": "v1.0.1",
      "profile_id": "PROF-PE-HIGH",
      "profile_version": "v1.0.1",
      "task_pool_id": "TP-CORE",
      "task_pool_version": "v1.0.1",
      "calendar_logic_version": "v1.0.1"
    },
    "user_inputs": {
      "equipment_description": "..."
    }
  },
  "options": {"return_content": true},
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 7.3 Canonical Response Envelope
<!-- NOTE: Example is illustrative, not complete. Refer to schema for full structure. -->
```json
{
  "contract": "VALOR-contract-orch-doc",
  "contract_version": "v1.0.1",
  "action_id": "ACT-000310",
  "ok": true,
  "result": {
    "doc_id": "DOC-0005",
    "doc_type": "URS",
    "doc_version": "v1.0.1",
    "state": "DRAFT",
    "content_format": "MARKDOWN",
    "content": "# URS\n...",
    "metadata": {
      "stamps": {"template_id": "TPL-URS", "template_version": "v1.0.1"},
      "citations": []
    }
  },
  "error": null
}
```

---

## 8. Error Semantics (Document Factory)

Standard codes:
- VALIDATION_ERROR: missing required input fields, invalid template refs
- INVARIANT_VIOLATION: missing stamps, attempt to mutate WP truth, finalize without checksum
- MODE_VIOLATION: wrong mode
- NOT_FOUND: missing template/bundle/wp/doc
- CONFLICT: ambiguous version refs, incompatible template vs doc_type
- UNSUPPORTED_OPERATION: unsupported format request
- INTERNAL_ERROR: unexpected

DOC-specific subcodes:
- TEMPLATE_REQUIRED_INPUT_MISSING
- MISSING_TRACEABILITY_STAMPS
- CANNOT_FINALIZE_WITH_ERRORS
- FINAL_IMMUTABLE
- FORMAT_NOT_SUPPORTED
- CITATION_ANCHOR_MISSING

Example error:
```json
{
  "code": "VALIDATION_ERROR",
  "subcode": "TEMPLATE_REQUIRED_INPUT_MISSING",
  "message": "Cannot generate URS: missing required input wp.scope.",
  "field": "wp.scope",
  "entity": "template_inputs",
  "remediation": "Update WP scope field and retry document generation."
}
```

---

## 9. Integration Points
- Orchestration coordinates DOC flows and enforces gates/confirmations.
- WP System provides authoritative snapshots; DOC must not patch WP truth.
- K&S provides templates/bundles/anchors.
- Reporting may reference doc metadata for traceability but does not own docs.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
