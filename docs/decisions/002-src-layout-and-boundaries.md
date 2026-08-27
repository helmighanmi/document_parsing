<!--
Path: docs/decisions/002-src-layout-and-boundaries.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# ADR-002: `src/` Layout and Explicit Boundaries

## Status

Accepted.

## Context

The original project mixed Streamlit state, RAG chunking, parser orchestration, configuration, and visualization in top-level modules. That made imports harder to test and encouraged UI concerns to leak into parsing logic.

## Decision

Use a `src/document_parser` package and separate presentation, security, parser orchestration, RAG transformation, configuration, and visualization.

## Consequences

Core behavior can be tested without importing Streamlit, optional dependencies stay behind adapters, and CLI/UI consumers share the same application service.
