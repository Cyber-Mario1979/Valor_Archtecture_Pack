# Valor Architecture Pack (v1.0.1)

This pack is structured for implementation readiness.

## Layout
- docs/architecture/          Architecture & subsystem specs (Markdown)
- contracts/                  Service contracts (YAML) with schema refs
- action_blocks/              Additional action blocks (YAML)
- templates/                  Document templates (Markdown) with placeholders
- libraries/                  Governed data libraries (profiles, task pools) for deterministic planning inputs
- libraries/profile_library/  Profile matrices (durations, lead times, flags) as versioned datasets
- libraries/task_pool/        Atomic task pool definitions referencing profile keys (no embedded numbers)
- libraries/preset_library/   Preset selectors binding task pools + profiles + calendar refs (versioned datasets)

- schemas/
  - objects/                  Canonical domain object schemas (draft-07)
  - documents/                Per-template render-input schemas (draft-07) + index.json
  - contracts/                Contract envelope + action result schemas (draft-07)
- validation/                 Render-input validation tools (placeholder coverage)
- test_vectors/               Minimal end-to-end vectors for staging/commit/export flows
- scripts/pack_validation/     Pack integrity scripts (manifest generator/verifier)

## ID formats (canonical)
- Work Package ID: `WP###` (three digits, zero-padded)
- Task ID: `WP###-T###`

## Versioning
All contracts/templates/docs in this pack are unified to: `v1.0.1`.
