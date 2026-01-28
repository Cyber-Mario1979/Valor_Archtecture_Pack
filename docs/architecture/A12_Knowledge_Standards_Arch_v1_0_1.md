---
id: VALOR-block-A12-knowledge-standards-architecture
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
  - VALOR-block-A10-security-compliance-architecture
summary: "Block A12 — Knowledge & Standards System Architecture: governed read-only libraries (standards, references, templates) delivered as versioned bundles with anchored citations and excerpt policy for CQV-safe document/report generation."
acceptance_criteria:
  - Defines K&S as read-only governed content with versioned bundles and anchors.
  - Defines entities (StandardRecord, TemplateRecord, Bundle, Anchor, CitationPolicy).
  - Defines anchored citation mechanism and excerpt policy constraints (metadata-only vs excerpt).
  - Defines contract actions to list/read bundles/templates/anchors and validate references.
  - Defines stamping and provenance requirements for downstream DOC/RPT systems.
  - Defines error semantics and safe handling aligned with Security & Compliance constraints.
---

# Knowledge & Standards System Architecture (Read-Only Governance + Bundles + Anchors)

Terminology: See **A15_Global_Glossary_Arch_v1_0_1.md** for definitions.


## 1. Purpose and Authority
Knowledge & Standards (K&S) is the subsystem that provides **governed, read-only reference assets** used across Valor:
- standards registers (internal/external),
- reference procedures and policies (metadata and controlled excerpts only),
- document templates (URS/RTM/DQ/IQ/OQ/PQ/VSR templates),
- standards bundles (pre-selected sets for a specific context).

K&S is authoritative for:
- the curated reference asset metadata,
- bundling/versioning of reference sets,
- anchored citation IDs and policies,
- template versions and required-input definitions.

K&S is not authoritative for:
- WP/task truth,
- document generation outputs (DOC),
- reporting outputs (RPT),
- approvals.

K&S is designed explicitly to support CQV auditability while respecting confidentiality and copyright.

---

## 2. Read-Only Governance Model

### 2.1 Immutable Assets Per Version
All K&S assets are immutable once published:
- standard_id + version
- template_id + version
- bundle_id + version
- anchor_id (within an asset version)

Changes require publishing a new version.

### 2.2 Why Read-Only Matters
Read-only behavior prevents:
- “silent” changes in standards references,
- drift between what a document cites and what the library contains,
- audit inconsistencies.

---

## 3. Core Entities (Authoritative Data Model)

### 3.1 StandardRecord
Represents a standard or reference source.

Required fields:
- standard_id (string, stable)
- version (string; may be edition/year or SemVer)
- title (string)
- publisher (string)
- scope_tags (array)
- access_classification (enum): PUBLIC | LICENSED | INTERNAL | CONFIDENTIAL
- excerpt_policy (enum; see §3.5)
- anchors (array of Anchor; see §3.4)
- metadata:
  - effective_date (optional)
  - supersedes (optional)
  - superseded_by (optional)
- checksum (optional)

### 3.2 TemplateRecord
Represents a governed template used by Document Factory and sometimes Reporting.

Required fields:
- template_id (string, stable)
- version (semver)
- name (string)
- doc_type (enum): VMP | URS | RA | RTM | DQ | IQ | OQ | PQ | VSR | REPORT
- required_inputs (array of input refs) (what fields must exist in WP/user_inputs)
- required_stamps (array; minimum stamp set)
- anchor_policy (required anchors or bundle references)
- content_format (enum): MARKDOWN | DOCX | PDF (policy)
- template_body (stored or referenced)
- checksum (optional)

### 3.3 Bundle
A bundle is a versioned selection of standards and templates for a given context.

Required fields:
- bundle_id (string, stable)
- version (semver)
- name (string)
- applicability:
  - equipment_domain
  - complexity
  - scope
- included_standards (array of {standard_id, version})
- included_templates (array of {template_id, version})
- default_citation_set (array of AnchoredRef; see §3.6)
- excerpt_policy_override (optional; must not weaken the strictest underlying policy)
- checksum (optional)

### 3.4 Anchor
Anchors are stable reference points inside a standard/template.

Fields:
- anchor_id (string, stable within asset version)
- anchor_title (string)
- anchor_type (enum): SECTION | CLAUSE | TABLE | FIGURE | APPENDIX | PARAGRAPH
- locator (string) (e.g., “Section 5.2”, “Table 3”)
- excerpt_allowed (bool; derived from excerpt policy)
- notes (optional)

### 3.5 ExcerptPolicy
Defines what K&S may return in responses for a given asset.

Policies:
- METADATA_ONLY: return title/ID/version/anchor metadata only; no content.
- PUBLIC_EXCERPT: allow small excerpt within defined limit and only from public sources.
- INTERNAL_ONLY: allow internal excerpt to authorized contexts (v0.1.x usually treated as metadata-only unless explicitly configured).
- NO_EXCERPTS: never return content, only anchors.

Security rule (from A10):
- K&S must refuse to output restricted excerpts.

### 3.6 AnchoredRef (Citations)
Citations in docs/reports must reference anchors:

Fields:
- asset_type: standard | template
- asset_id
- asset_version
- anchor_id
- citation_label (optional; e.g., “[S1]”)
- excerpt_policy_applied (resolved)

---

## 4. Anchored Citation Mechanism (Audit-Grade)

### 4.1 Why Anchors
In CQV, saying “per ISO/ASTM” is insufficient. A citation must be:
- precise (which section),
- stable (anchored to a version),
- governed (immutable).

### 4.2 Citation Resolution
Given an AnchoredRef, K&S returns:
- title + version + anchor_title + locator
- excerpt if allowed by excerpt policy
- a canonical citation string

### 4.3 Bundle-Level Citation Sets
Bundles may define default anchor sets required for certain doc types (e.g., URS must cite specific clauses).

Document Factory must validate required anchors exist and are included.

---

## 5. K&S Contract (Implementation-Ready)

K&S is accessed via `VALOR-contract-orch-ks`.

### 5.1 Actions
LIST/READ:
- KS_LIST_STANDARDS (filters)
- KS_READ_STANDARD (standard_id + version)
- KS_LIST_TEMPLATES (filters)
- KS_READ_TEMPLATE (template_id + version)
- KS_LIST_BUNDLES (filters)
- KS_READ_BUNDLE (bundle_id + version)

ANCHORS/CITATIONS:
- KS_LIST_ANCHORS (asset ref)
- KS_RESOLVE_CITATION (anchored_ref)
- KS_VALIDATE_CITATION_SET (list of anchored_refs)

VALIDATE:
- KS_VALIDATE_BUNDLE_INTEGRITY (includes exist, versions exist, anchors exist)
- KS_VALIDATE_TEMPLATE_REQUIREMENTS (required_inputs/stamps/anchors)

### 5.2 Canonical Request (Resolve Citation)
```json
{
  "contract": "VALOR-contract-orch-ks",
  "contract_version": "v1.0.1",
  "action_id": "ACT-001210",
  "action_type": "KS_RESOLVE_CITATION",
  "mode": "M2",
  "payload": {
    "anchored_ref": {
      "asset_type": "standard",
      "asset_id": "STD-123",
      "asset_version": "2020",
      "anchor_id": "A-5-2"
    }
  },
  "context": {"timestamp_utc": "2025-12-22T00:00:00Z"}
}
```

### 5.3 Canonical Response
<!-- NOTE: Example is illustrative, not complete. Refer to schema for full structure. -->
```json
{
  "contract": "VALOR-contract-orch-ks",
  "contract_version": "v1.0.1",
  "action_id": "ACT-001210",
  "ok": true,
  "result": {
    "citation": {
      "title": "Standard Title",
      "asset_id": "STD-123",
      "asset_version": "2020",
      "anchor_title": "Requirements for ...",
      "locator": "Section 5.2",
      "excerpt": null,
      "excerpt_policy": "METADATA_ONLY"
    }
  },
  "error": null
}
```

---

## 6. Stamping and Provenance Requirements

### 6.1 What Downstream Must Stamp
When DOC or RPT uses K&S assets, their outputs must stamp:
- bundle_id/version (if used)
- template_id/version (if used)
- standards referenced (standard_id/version at minimum; anchors in citations)

### 6.2 K&S Outputs Must Be Versioned
K&S responses must always include asset_id/version for any provided metadata.
No unversioned citations are allowed.

---

## 7. Error Semantics (K&S)

Standard codes:
- NOT_FOUND: asset/version/anchor not found
- VALIDATION_ERROR: invalid request schema, missing fields
- CONFLICT: ambiguous versions, superseded version requested without explicit pin
- UNSUPPORTED_OPERATION: excerpt requested but policy prohibits
- INTERNAL_ERROR: unexpected

K&S-specific subcodes:
- ASSET_VERSION_NOT_FOUND
- ANCHOR_NOT_FOUND
- EXCERPT_BLOCKED
- BUNDLE_INTEGRITY_FAILED
- TEMPLATE_REQUIREMENT_MISSING

Example error:
```json
{
  "code": "UNSUPPORTED_OPERATION",
  "subcode": "EXCERPT_BLOCKED",
  "message": "Excerpt output is not permitted for this standard (access_classification=LICENSED, excerpt_policy=METADATA_ONLY).",
  "entity": "standard",
  "remediation": "Use anchored metadata citation only or provide an approved public excerpt source."
}
```

---

## 8. Integration Requirements
- Presets bind to bundle_id/version; Orchestration propagates this.
- Document Factory uses templates + citation sets; validates required anchors.
- Reporting can include traceability tables referencing standards/template versions and anchor metadata.
- Security & Compliance rules constrain excerpt outputs.

---

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
