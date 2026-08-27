<!--
Path: docs/migration.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Migration from the Original Layout

| Original | Refactored |
| --- | --- |
| `app.py` | thin entry point + `src/document_parser/ui.py` |
| `parsers.py` | `src/document_parser/parser.py` |
| RAG helpers inside `app.py` | `src/document_parser/rag.py` |
| `visualizer.py` | `src/document_parser/visualizer.py` |
| constant-heavy `config.py` | typed `src/document_parser/config.py` + environment variables |
| ad-hoc URL download | `src/document_parser/security.py` |
| `test_installation.py` | `tests/unit/` + `tests/integration/` |
| multiple overlapping quick-start docs | README + focused `docs/` pages |

Behavior intentionally changed where the old contract was misleading or unsafe: unsupported legacy Office extensions were removed, CSV has its own parser, public local-path input is disabled, remote downloads are bounded, and invalid RAG overlap is rejected.
