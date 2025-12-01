# NebulaBunny FREEZE — Protocol Layer (MIT)

This repository contains the **open protocol layer** of the NebulaBunny FREEZE system.

Its purpose is to define how a quant research or trading system can produce
fully reproducible, auditable evidence packages — **FREEZE-A** and **FREEZE-B** —
that can be independently verified without disclosing proprietary algorithms.

## What is included (MIT open source)

### 1. Protocol Schemas
- JSON Schema definitions for FREEZE-A / FREEZE-B.
- five_fingerprint schema (code_git_hash / data_version / spec_hash / seed / env_fingerprint).

### 2. Specification Documents
Located in `protocol/specs/`, they describe:
- Required fields & units.
- Versioning rules.
- Backwards compatibility requirements.
- Reproducibility principles.

### 3. CLI Tools (structural only)
`nb-freeze` is a minimal, safe-to-open-source tool that:
- Generates a skeletal FREEZE-A package.
- Validates FREEZE-A/B structure (schema + hash + directory layout).
- Verifies OTS timestamp files (optional).

It does **not** contain drift, execution, cost, or replay logic.

### 4. Examples
Located under `protocol/examples/`:
- `freeze_a_example/`
- `freeze_b_example/`

Both are **synthetic** and safe for public demonstration.

### 5. Validators
Open-source structural validators:
- `validate_freeze_a.py`
- `validate_freeze_b.py`
- `ots_verifier.py`

They focus on schema + hash + timestamp checks only.

## What is intentionally *not* included

This repository **does not** contain:
- Drift calculation engine  
- Execution quality engine  
- Stress cost engine  
- Replay engine  
- Strategy logic  
- Backtest or execution algorithms  

These remain part of the internal BCL-licensed engine.

For internal structure and licensing of the commercial engine,
see `engine-proprietary/INTERNAL_LAYERING.md`.

## License

- Protocol layer: **MIT License**
- Internal engine (not included here): **NebulaBunny BCL License**

## Version

Current protocol version: **v1.0.0**
