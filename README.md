<!--
  Valor Architecture Pack v1.0.1

  This README provides a high‑level overview of the purpose, structure, and
  usage of the Valor architecture pack. The pack is intended for engineers
  and quality teams responsible for integrating regulated CQV workflows into
  their products. It summarises the mission, core concepts, directory
  structure, and important conventions so that teams can navigate and build
  upon this specification with confidence.
-->

# Valor Architecture Pack (v1.0.1)

![Valor architecture blueprint](architecture_blueprint.png)

The **Valor Architecture Pack** is a blueprint for a contract‑driven,
system‑of‑systems (SoS) designed to support **Commissioning, Qualification
and Validation (CQV)** execution.  Valor structures regulated work into
governed **Work Packages**, **task pools**, **presets**, **advisory
planning**, **controlled document generation**, and **audit‑grade
reporting/export**.  It emphasises repeatable execution, traceability and
determinism over “smart guesses”.

This pack consolidates architecture specifications, service contracts,
schemas, templates, governed libraries and test vectors at version
`v1.0.1`.  It is **implementation‑ready**—every document, schema and
contract in this repository has been versioned and aligned to work
together.  There is no code for a running system here; rather, this is
the definitive reference for anyone building or integrating a Valor
implementation.

## Mission and Scope

Valor’s mission is to provide a **governed orchestration system** that
transforms unstructured user intent into deterministic, contract‑safe
actions.  It enforces CQV discipline through gated workflows,
stages, commits, reviews and exports while maintaining an immutable
traceability context.  Valor is **not** a generic
project management tool or ERP substitute; it does not invent
durations/lead times or replace human decisions.

Within its boundary, Valor owns the truth for Work Packages and tasks,
stages tasks from governed task pools, generates planning proposals
based on governed profiles and calendar logic, produces controlled
documents from templates and standards, and generates reports/exports
with mandatory stamps.  Outside its boundary it
references, but does not own, QMS execution, procurement, physical
execution data and final signatures.

## Architecture Overview

Valor is composed of independently useful and independently governed
subsystems that collaborate through explicit contracts.  The major
subsystems and their responsibilities are:

| Subsystem | Purpose |
|----------|---------|
| **Orchestration** | Routes user intent to canonical actions, enforces governance gates, manages traceability context and contract routing rules. |
| **Work Package** | Authoritative truth store for Work Package and task objects, their identifiers, lifecycle states and invariants. |
| **Task Pool Library** | Catalog of atomic tasks, metadata and default dependency wiring. |
| **Preset System** | Versioned selectors that bind a profile, task pool, calendar and standards bundle together. |
| **Planning System** | Advisory scheduling engine that produces dependency‑consistent proposals using governed profiles and calendar logic. |
| **Knowledge & Standards** | Read‑only library of controlled templates and standards bundles with anchored citations. |
| **Document Factory** | Generates controlled documents from Work Package truth plus templates/standards and produces provenance metadata. |
| **Reporting & Export** | Creates reports and exports from Work Package truth, computes metrics and stamps outputs. |
| **Security & Compliance** | Enforces non‑disclosure, operational mode restrictions and safe failure behaviour. |

Subsystems interact exclusively via **contracts**.  Each contract is
versioned (semantic versioning) and identified by a canonical name such
as `VALOR‑contract‑orch‑wp` or `VALOR‑contract‑orch‑plan`.  Calls to
subsystems must conform to the SoS action envelope specification
defined in the architecture documentation.

For a complete description of the SoS context, capability map,
invariants, contract naming conventions and error taxonomy, refer to
`docs/architecture/A01_SoS_Context_Capability_Arch_v1_0_1.md`.

## Directory Structure

This pack follows a clean, opinionated layout.  The table below
summarises the top‑level directories and their roles:

| Path | Contents |
|------|---------|
| `docs/architecture/` | In‑depth Markdown specifications for each subsystem, global principles and invariants, governance and security constraints.  Begin with `A00_Specs_Architecture_Pack_Arch_v1_0_1.md` and follow the reading order specified therein. |
| `contracts/` | YAML definitions of service contracts between the Orchestration subsystem and each subordinate subsystem (WP, Planning, Knowledge & Standards, Document Factory, Reporting & Export).  These files specify the envelopes, action types, payload schemas and result schemas. |
| `action_blocks/` | Additional orchestration action definitions encapsulated as YAML; these blocks can be imported by contracts or used in new flows. |
| `templates/` | Markdown document templates with placeholders for merging regulated data.  Each template corresponds to a JSON Schema in `schemas/documents/`. |
| `libraries/` | Governed data sets used by the Preset and Planning systems.  It contains profiles (duration/lead time matrices), task pools (atomic task definitions) and presets (selectors binding profiles and task pools).  The `calendar/` subfolder holds working‑day calendars. |
| `schemas/` | JSON Schema files (draft‑07) for domain objects, documents and contract payloads.  These schemas enforce structural validity and can be used for automated validation.  See `schemas/documents/index.json` for an index of document schemas. |
| `validation/` | Python scripts and examples for validating render inputs against the provided schemas.  Use these tools to test conformance before committing artefacts to the system. |
| `test_vectors/` | Minimal end‑to‑end JSON examples that exercise staging, commit, export and reporting flows.  They can be used as unit tests or as references when building a client. |
| `scripts/pack_validation/` | Helper scripts for generating and verifying the pack’s manifest.  Run `python generate_manifest.py` to produce a new `manifest.yaml` and `python verify_manifest.py` to ensure file integrity. |
| `Valor_Arch_Addendums_v1.0.1A/` | Supplemental addendums that clarify canvas rendering, planning invariants, UX contracts and export projections beyond the main architecture. |

In addition to the above, the root directory contains a `manifest.yaml` that records the SHA‑256 hash and size of every file for integrity assurance.  All files in this pack adhere to the version `v1.0.1` specified in the manifest.

## Getting Started

1. **Read the specs:** Begin with `A00_Specs_Architecture_Pack_Arch_v1_0_1.md`, which describes the scope, reading order and canonical index of the architecture documentation.  Follow the recommended reading order to build a solid mental model of Valor.
2. **Explore contracts and schemas:** Inspect the contracts in `contracts/` and their associated JSON Schemas in `schemas/contracts/`.  These define the envelopes and result formats for each subsystem interaction.
3. **Review templates and documents:** For each document type (VMP, Risk Assessment, URS, RTM, DQ, IQ, OQ, PQ, VSR), there is a corresponding Markdown template in `templates/` and a JSON Schema in `schemas/documents/` that defines the required fields.  The `schemas/documents/index.json` file lists available document schemas.
4. **Validate your inputs:** Use the Python scripts in `validation/` to validate render inputs against the document schemas before attempting to generate documents.  The `test_vectors/` folder contains example payloads for staging tasks, applying plans and producing exports.
5. **Generate a manifest (optional):** If you modify or extend this pack, run `scripts/pack_validation/generate_manifest.py` to update `manifest.yaml` and `verify_manifest.py` to ensure that file hashes match the manifest entries.

## Conventions and Standards

- **Versioning:** All contracts, schemas and templates follow semantic versioning.  Orchestration may only call contracts with a compatible major version.
- **Identifiers:** Work Packages use the format `WP###` (zero‑padded); tasks use `WP###-T###`.  Preset IDs and profile IDs similarly follow a versioned naming convention.
- **Action Envelope:** Every cross‑subsystem call must wrap its payload in a canonical envelope containing the contract name, version, action ID/type, mode, actor, target, payload and timestamp.
- **Error Taxonomy:** Errors returned by subsystems are categorised using standard codes (e.g., `MODE_VIOLATION`, `VALIDATION_ERROR`, `INVARIANT_VIOLATION`, `NOT_FOUND`, `CONFLICT`, `UNSUPPORTED_OPERATION`, `INTERNAL_ERROR`).

## Extending the Pack

This repository is designed to be extended as Valor evolves.  To add a new
contract, template or library:

1. Follow the existing naming conventions and versioning patterns.
2. Create accompanying JSON Schemas for any new document or contract
   payloads to ensure structural validity.
3. Update `manifest.yaml` using the pack validation scripts to record
   the hash and size of new files.
4. Consider updating the addendums or architecture documentation if
   changes affect invariants, governance rules or system boundaries.

## About This Pack

The Valor Architecture Pack is maintained by the Nexus architecture team.
Its goal is to provide a deterministic, governed foundation for
regulated CQV workflows.  By codifying the system boundary, subsystems,
contracts, invariants and templates, the pack enables multiple teams to
build compatible implementations with confidence.  Should you discover
issues or have questions, please contact the maintainers via the
appropriate project channels.
