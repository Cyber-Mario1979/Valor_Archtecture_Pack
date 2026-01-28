---
id: VALOR-block-A15-global-glossary
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
summary: "Centralized, canonical glossary of technical terms used across the Valor architecture pack."
acceptance_criteria:
  - Provides authoritative definitions for core Valor architecture terms.
  - Uses one term per heading for easy parsing.
---

# Global Glossary (Centralized)

## System of Systems (SoS)
A federation of independently governed subsystems that interact through explicit interfaces to deliver higher-level capabilities, while each subsystem retains its own authority and evolution path.

## Orchestration
The coordinating subsystem that routes user intent into contract actions, enforces governance gates, validates readiness, and ensures stamps and audit events are produced.

## Work Package (WP)
The authoritative container for scope, tasks, dependencies, validations, and lifecycle state representing a governed unit of CQV work.

## Contract
A versioned, schema-defined interface between subsystems defining actions, envelopes, validation rules, and error semantics.

## Invariant (INV)
A hard-stop rule that must not be violated across the system.

## Stamp
A provenance tuple written into outputs indicating the exact versions of governed assets used.

---

## CHANGELOG
| Date       | Changes     | Type / Version |
| ---------- | ----------- | -------------- |
| 2025-12-23 | First Issue | Arch_v1.0.1    |
