<!--
Path: docs/decisions/001-python-runtime.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# ADR-001: Python 3.11 Reference Runtime

## Status

Accepted.

## Context

The repository combines web UI, PDF tooling, Office parsers, OCR, and optional ML-heavy libraries. The newest Python release is not automatically the lowest-risk production baseline for that ecosystem.

## Decision

Use Python 3.11 as the Docker/reference runtime and validate 3.11 + 3.12 in CI. Declare `>=3.11,<3.14` for the package.

## Consequences

This favors broad wheel availability and mature ML compatibility while still using modern Python typing/runtime features. The version can be advanced after the optional dependency matrix is validated in CI.
