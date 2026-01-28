<a id="source-t4-urs-template-v1-0-1-md"></a>
# Source: T4_URS_Template_V1_0_1.md

## Template Metadata
- ID: T4
- Title: User Requirements Specification (URS)
- Version: V1.0.1
- Revision Date: {{doc.revision_date}}

# User Requirements Specification (URS) Template

> **AUTO-FILL (render inputs)**
> **WP:** `{{wp.id}}`  |  **Doc:** `{{doc.id}}`  |  **Doc Type:** `URS`  |  **Version:** `{{doc.version}}`
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
### 1.1 Purpose
Define the purpose of the system/equipment, including intended use and regulatory/business drivers.

### 1.2 Scope
- In Scope: [Main system functions, subsystems]
- Out of Scope: [Anything explicitly excluded]

## 2. Roles & Responsibilities
| Role | Responsibility |
|------|----------------|
| System Owner | Owns content & approvals |
| Process Owner | Confirms process fit |
| Automation/CSV | Ensures compliance with computerized systems |
| EHS/SHE | Confirms safety & sustainability inputs |
| Quality | Ensures compliance with GMP/QA |
| Project Manager | Oversees alignment with project goals |

## 3. System Description
- Overview: [Brief description of the system]
- Interfaces: [Upstream/Downstream systems]
- Main Functions: [High-level functional description]

## 4. Definitions & Abbreviations
List key terms, e.g.: CQA, CPP, DQ/IQ/OQ/PQ, etc.

## 5. Requirement Classification
- M = Mandatory
- B = Beneficial
- N = Nice-to-have

## 6. User Requirements — Functional
> **AUTO-FILL:** You can optionally inject the full requirements table as markdown via `{{urs.requirements_table_md}}`.

| URS Ref | Requirement | Priority (M/B/N) | Verification (DQ/IQ/OQ/PQ) |
|---------|-------------|------------------|-----------------------------|
| 6.1 | [System shall perform its core function reliably] | | |
| 6.2 | [System capacity/throughput requirements] | | |
| 6.3 | [Integration with related systems] | | |

## 7. User Requirements — Design & Materials
| URS Ref | Requirement | Priority | Verification |
|---------|-------------|----------|--------------|
| 7.1 | [Materials compatible with intended use] | | |
| 7.2 | [Surfaces smooth and cleanable] | | |
| 7.3 | [Non-reactive and non-shedding materials] | | |

## 8. User Requirements — Facility & Environment
| URS Ref | Requirement | Priority | Verification |
|---------|-------------|----------|--------------|
| 8.1 | [Operating temperature range] | | |
| 8.2 | [Relative humidity range] | | |
| 8.3 | [Cleanroom classification/environmental conditions] | | |

## 9. User Requirements — Utilities
| URS Ref | Utility | Requirement |
|---------|---------|-------------|
| 9.1 | Electrical | [Voltage, frequency, phases] |
| 9.2 | Air/Water | [Compressed air, cooling, vacuum] |
| 9.3 | Other | [List as needed] |

## 10. User Requirements — Computerized Systems
| URS Ref | Requirement |
|---------|-------------|
| 10.1 | [Compliance with 21 CFR Part 11, Annex 11] |
| 10.2 | [Audit trails, security, backup] |
| 10.3 | [User management and access controls] |

## 11. User Requirements — Safety, Health & Environment
| URS Ref | Requirement |
|---------|-------------|
| 11.1 | [Operator safety] |
| 11.2 | [Emergency stops and safety interlocks] |
| 11.3 | [Noise/vibration limits] |
| 11.4 | [Environmental impact] |

## 12. User Requirements — Maintenance & Support
| URS Ref | Requirement |
|---------|-------------|
| 12.1 | [Ease of maintenance and access] |
| 12.2 | [Spare parts availability] |
| 12.3 | [Training and manuals] |
| 12.4 | [Warranty and service agreements] |

## 13. Documentation Deliverables
- GA Drawings, Technical Datasheets, Manuals, Qualification Protocols, Certificates.

## 14. References
- ISPE Baseline Guide Vol.5, GAMP 5, ICH Q8/Q9/Q10, EU GMP Annex 15, ASTM E2500, local regulatory (e.g., EDA).

## 15. Traceability
- Define trace through design and testing. Reference RTM.

## 16. Risk Assessment
- Summary of initial RA, identification of critical requirements.

## 17. Acceptance Criteria
- Define general acceptance criteria for fit-for-use.

## 18. Document History
| Rev | Date | Summary of Changes | Author |
|-----|------|--------------------|--------|
| 0.1 | [dd-mmm-yyyy] | Draft issued | [Name/Role] |

## 19. Approval Signatures
| Name | Title | Department | Date | Signature |
|------|-------|------------|------|------------|
| | | | | |
| | | | | |
| | | | | |

---