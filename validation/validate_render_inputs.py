#!/usr/bin/env python3
"""Validate *render-input payload* against a template render-input schema.

Validates placeholder coverage: all required placeholder tokens exist in the payload.

Usage (from pack root):
  python validation/validate_render_inputs.py --template T4_URS_Template_V1_0_0.md --data validation/examples/render_inputs_min.json

Or explicit schema:
  python validation/validate_render_inputs.py --schema schemas/documents/T4_URS_Template_V1_0_0.schema.json --data validation/examples/render_inputs_min.json
"""
import argparse, json, sys
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]

def get_by_dot(obj, token: str):
    cur = obj
    for part in token.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return False, None
    return True, cur

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", help="Path to a schemas/documents/*.schema.json file.")
    ap.add_argument("--template", help="Template filename under templates/ (used to infer schema name).")
    ap.add_argument("--data", required=True, help="Path to JSON payload (render inputs).")
    args = ap.parse_args()

    if not args.schema and not args.template:
        print("ERROR: Provide --schema or --template.", file=sys.stderr)
        return 2

    schema_path = Path(args.schema) if args.schema else (PACK_ROOT/"schemas/documents"/Path(args.template).with_suffix(".schema.json").name)
    data_path = Path(args.data)

    if not schema_path.is_absolute():
        schema_path = (PACK_ROOT/schema_path).resolve()
    if not data_path.is_absolute():
        data_path = (PACK_ROOT/data_path).resolve()

    if not schema_path.exists():
        print(f"ERROR: schema not found: {schema_path}", file=sys.stderr)
        return 2
    if not data_path.exists():
        print(f"ERROR: data not found: {data_path}", file=sys.stderr)
        return 2

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = json.loads(data_path.read_text(encoding="utf-8"))

    required = schema.get("required", [])
    missing = []
    for token in required:
        ok, val = get_by_dot(data, token)
        if not ok or val is None:
            missing.append(token)

    if missing:
        print("❌ Missing required render-input tokens:")
        for t in missing:
            print(f"- {t}")
        return 1

    print("✅ Render-input payload covers all required placeholders.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
