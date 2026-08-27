<!--
Path: CHANGELOG.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Changelog

## 2.0.0 - 2026-08-27

### Architecture

- Migrated top-level modules to a `src/document_parser` package.
- Separated Streamlit UI, CLI, parsing, RAG transformation, URL security, configuration, and visualization.
- Added ADRs, deployment documentation, runbook, contribution guide, and security policy.

### Correctness

- Prevented invalid RAG overlap values from causing non-progressing chunk loops.
- Corrected Docling per-page export to use one-based `page_no` values.
- Stopped advertising legacy `.doc`, `.ppt`, and `.xls` formats unsupported by the chosen libraries.
- Added a real CSV parser instead of routing CSV through openpyxl.
- Added explicit EasyOCR/Tesseract language-code mapping.
- Added empty/blank PDF handling to scanned-PDF inspection.

### Security and operations

- Added SSRF-aware remote URL validation, redirect checks, timeouts, and byte limits.
- Disabled local-path input in the public UI by default.
- Added non-root/read-only Docker hardening, health checks, CI, CodeQL, dependency auditing, and Dependabot.

### Testing

- Added offline unit and generated-fixture integration tests for parser contracts, RAG behavior, security policy, document formats, and PDFs.
