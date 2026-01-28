<a id="source-t10-vsr-template-v1-0-1-md"></a>
# Source: T10_VSR_Template_V1_0_1.md

## Template Metadata
- ID: T10
- Title: Validation Summary Report (VSR)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Validation Summary Report (VSR) Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `VSR`  |  **Version:** `{{doc.version}}`
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

## 1. Purpose and Scope
Summarize URS, DQ, IQ, OQ, PQ outcomes; assess compliance, deviations/CAPAs, residual risks; support release decision.

## 2. Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| System/Process Owner | Confirms system meets requirements; authorizes release |
| CQV | Prepares VSR; collates data; assesses compliance |
| QA | Reviews/approves VSR; verifies deviations/CAPAs closure |
| Engineering/Automation | Provides design/install data; evaluates technical issues |
| Production/Operations | Executes PQ runs; verifies user acceptance |
| QC | Provides analytical data supporting PQ |

## 3. Validation Lifecycle Summary
- URS Compliance
- Design Qualification
- Installation Qualification
- Operational Qualification
- Performance Qualification

## 4. Risk Assessment and Mitigation
Summarize RA (e.g., FMEA), significant risks, RPN, mitigations, residual risk acceptance.

## 5. Deviations and Corrective Actions
List deviations across URS/DQ/IQ/OQ/PQ; root cause, impact, CAPA; closure status.

## 6. Conclusion and Recommendation
Overall evaluation of validation status; recommend qualified release or conditions.

## 7. References, Document History, Approval Signatures
List referenced documents; revision table; signatures.

---

<!-- Removed deprecated schema templates T11–T15. -->