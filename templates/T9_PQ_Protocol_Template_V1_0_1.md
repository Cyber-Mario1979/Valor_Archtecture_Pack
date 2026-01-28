<a id="source-t9-pq-protocol-template-v1-0-1-md"></a>
# Source: T9_PQ_Protocol_Template_V1_0_1.md

## Template Metadata
- ID: T9
- Title: Performance Qualification (PQ) Protocol
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Performance Qualification (PQ) Protocol

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `DOC`  |  **Version:** `{{doc.version}}`
> **Stamps:** `{{doc.stamps.preset.id}}@{{doc.stamps.preset.version}}` · `{{doc.stamps.profile.id}}@{{doc.stamps.profile.version}}` · `{{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}}` · `{{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}}`
> **Generated:** `{{doc.generated_utc}}`  |  **Author:** `{{doc.actors.author}}`  |  **Reviewer:** `{{doc.actors.reviewer}}`  |  **Approver:** `{{doc.actors.approver}}`


## Document Info (Auto-filled)

| Field | Value |
|---|---|
| Work Package ID | {{wp.id}} |
| Work Package Title | {{wp.title}} |
| Document ID | {{doc.id}} |
| Document Title | {{doc.title}} |
| Document Type | {{doc.doc_type}} |
| Status | {{doc.status}} |
| Version | {{doc.version}} |
| Revision Date | {{doc.revision_date}} |
| Generated (UTC) | {{doc.generated_utc}} |
| Author | {{doc.actors.author}} |
| Reviewer | {{doc.actors.reviewer}} |
| Approver | {{doc.actors.approver}} |
| Preset | {{doc.stamps.preset.id}}@{{doc.stamps.preset.version}} |
| Profile | {{doc.stamps.profile.id}}@{{doc.stamps.profile.version}} |
| Calendar | {{doc.stamps.calendar.id}}@{{doc.stamps.calendar.version}} |
| Bundle | {{doc.stamps.bundle.id}}@{{doc.stamps.bundle.version}} |

## Sign-off (Auto-filled)

| Role | Name | Date | Signature |
|---|---|---|---|
| Author | {{doc.actors.author}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Reviewer | {{doc.actors.reviewer}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |
| Approver | {{doc.actors.approver}} | {{doc.revision_date}} | {{doc.signatures_table_md}} |

## Purpose and Scope
Demonstrate consistent performance under routine conditions; assess throughput, product quality, reproducibility.

## Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| CQV | Plans and executes PQ runs |
| Production | Operates equipment per batch records |
| QC | Conducts analytical testing |
| QA | Reviews PQ documentation; approves status |

## References

> **AUTO-FILL:** `{{doc.citations_list_md}}` (anchored citations list)

- URS, DQ, IQ, OQ
- Process validation master plan
- EU GMP Annex 15; ICH Q8/Q9/Q10

## Test Matrix
| Test ID | Objective | Method | Acceptance Criteria | Records |
| --- | --- | --- | --- | --- |
| PQ-001 | Verify throughput | Full-scale batch | ≥ target throughput within tolerance | Batch record |
| PQ-002 | Verify product quality | In-process and final QC | All within specifications | QC certificates |
| PQ-003 | Verify reproducibility | Three consecutive runs | No critical deviations; consistent results | VSR summary |

## Deviations
List deviations, impact, corrective actions.

## Approval
Prepared by: ___ Date: ___  
Reviewed by: ___ Date: ___  
Approved by: ___ Date: ___

---