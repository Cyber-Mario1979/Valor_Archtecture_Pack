<a id="source-t5-rtm-template-md"></a>
# Source: T5_RTM_Template.md

## Template Metadata
- ID: T5
- Title: Requirements Traceability Matrix (RTM)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# CQV Traceability Matrix Template

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

Ensures traceability of URS requirements through validation lifecycle (DQ, IQ, OQ, PQ, VSR).

| URS_ID | Requirement Description | Risk Assessment Ref | DQ Verification (Design Review) | IQ Verification (Installation) | OQ Verification (Operation) | PQ Verification (Performance) | VSR Reference | Release Decision |
|---------|-------------------------------|---------------------|---------------------------------|-------------------------------|-----------------------------|-------------------------------|----------------|-----------------|
| URS-XXX | [Enter requirement] | RA-XXX | [DQ method] | [IQ method] | [OQ method] | [PQ method] | [VSR] | Accepted/Rejected |
| URS-XXX | [Enter requirement] | RA-XXX | [DQ method] | [IQ method] | [OQ method] | [PQ method] | [VSR] | Accepted/Rejected |

---