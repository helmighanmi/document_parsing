<!--
Path: docs/architecture.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Architecture

## Goals

The system converts heterogeneous documents into one predictable `ParseResult` contract that downstream UI, CLI, and RAG components can consume without knowing which parsing backend was used.

## Boundaries

### Presentation

`ui.py` owns Streamlit state and rendering. `cli.py` owns terminal arguments and file output. Neither contains parsing algorithms.

### Application/domain service

`parser.py` owns format detection, parser selection, compatibility checks, parsing orchestration, and normalization of backend-specific output.

### Infrastructure adapters

External libraries such as PyMuPDF, pdfplumber, Docling, Tesseract, and Office readers are imported at adapter boundaries. Heavy dependencies remain optional where possible.

### Security

`security.py` owns URL trust decisions, redirect validation, size limits, and temporary download lifecycle. Network policy is not mixed into parser algorithms.

### RAG transformation

`rag.py` converts normalized parser output into page-aware chunks. This keeps retrieval concerns separate from document extraction.

## Data flow

1. A user supplies an upload, local path through the programmatic API, or HTTP(S) URL.
2. The source is validated and bounded.
3. File type is detected by extension.
4. A compatible backend is selected explicitly or automatically.
5. Backend output is normalized to content/pages/metadata/images.
6. Optional PDF analysis classifies digital/scanned/hybrid pages.
7. Consumers render content or transform it into RAG chunks.

## Failure model

Expected failures use domain-specific exceptions: unsupported format, optional dependency missing, unsafe source, and file too large. Unexpected backend failures are logged with context and surfaced without exposing internal stack traces in normal UI flows.
