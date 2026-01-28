<a id="source-t3-risk-assessment-template-v1-0-1-md"></a>
# Source: T3_Risk_Assessment_Template_V1_0_1.md

## Template Metadata
- ID: T3
- Title: Risk Assessment (FMEA)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# Risk Assessment (FMEA)

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `RA`  |  **Version:** `{{doc.version}}`
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

**Project/Equipment:** [Insert]  
**Area/Line:** [Insert]  
**Document No.:** RA-XXX  
**Prepared by:** [CQV/Engineering]  
**Reviewed by:** [QA]  
**Approved by:** [Head QA/Production]  

## 1. Purpose
Identify and assess risks (failure modes) to GMP compliance and product quality.

## 2. Scope
Covers risks associated with design, installation, operation, and performance.

## 3. References
- ICH Q9 (Quality Risk Management)
- EU GMP Annex 15
- ISPE Risk-Based Guide

## 4. Risk Assessment Table
| Step/URS Ref | Requirement / Function | Failure Mode | Potential Effect | S (1-5) | O (1-5) | D (1-5) | RPN | Mitigation |
|--------------|------------------------|--------------|-----------------|---------|---------|---------|-----|------------|
| URS-001 | SS316L product contact | Material not compliant | Contamination risk | 5 | 2 | 2 | 20 | Vendor certificate + IQ check |
| URS-002 | Alarm recording | Alarm not timestamped | Data integrity failure | 4 | 3 | 3 | 36 | OQ test of audit trail |
| URS-003 | Capacity ≥ 100 kg | Insufficient throughput | Production delays | 3 | 2 | 3 | 18 | PQ execution with full batch |

## 5. Approval
Prepared by: ____ Date: ____  
Reviewed by: ____ Date: ____  
Approved by: ____ Date: ____  

---