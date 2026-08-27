<!--
Path: docs/testing.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Testing Strategy

The default test suite is deterministic and offline.

- **Unit tests** cover chunking invariants, parser compatibility, language mapping, URL policy, and size enforcement.
- **Integration tests** generate local TXT/CSV/DOCX/PPTX/XLSX/PDF fixtures and exercise real parser libraries.
- **Optional/heavy tests** should be marked `optional` and must not make normal pull requests download large ML models.
- **CI** validates Python 3.11 and 3.12 and measures package coverage.

Network-dependent parser quality evaluation belongs in a separate evaluation workflow, not in deterministic unit tests.
