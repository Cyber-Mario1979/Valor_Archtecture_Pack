<a id="source-t8-oq-protocol-template-v1-0-1-md"></a>
# Source: T8_OQ_Protocol_Template_V1_0_1.md

## Template Metadata
- ID: T8
- Title: Operational Qualification (OQ) Protocol
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Operational Qualification (OQ) Protocol

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
Verify operational performance across ranges; confirm critical functions, alarms, interlocks; ensure data integrity.

## Roles & Responsibilities
| Role | Responsibility |
| --- | --- |
| CQV Engineer | Executes OQ scripts and records results |
| Process Owner | Reviews parameters and accepts outcomes |
| Quality | Ensures compliance; approves deviations |
| Automation/CSV | Supports software testing and DI verification |

## References

> **AUTO-FILL:** `{{doc.citations_list_md}}` (anchored citations list)

- URS, DQ, IQ
- EU GMP Annex 15
- ASTM E2500

## Test Matrix
| Test ID | Objective | Method | Acceptance Criteria | Records |
| --- | --- | --- | --- | --- |
| OQ-001 | Verify alarm activation | Force alarm; monitor response | Alarm logs with correct timestamp | Event log capture |
| OQ-002 | Verify temperature control | Operate at setpoints across range | Maintain within ±2 °C of setpoint | Recorder printout |
| OQ-003 | Verify safety interlock | Attempt unsafe start | Prevented; warning displayed | Checklist |

## Deviations
Record deviations, impact, corrective actions.

## Approval
Prepared by: ___ Date: ___  
Reviewed by: ___ Date: ___  
Approved by: ___ Date: ___

---