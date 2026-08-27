<!--
Path: README.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Document Parsing Workbench

A production-oriented document ingestion toolkit for **PDF, DOCX, PPTX, XLSX, CSV, text, Markdown, and HTML**, with optional OCR/Docling backends, layout visualization, and page-aware RAG export.

The repository is intentionally structured to demonstrate the full engineering lifecycle around an AI-adjacent document pipeline: architecture, dependency management, defensive ingestion, deterministic testing, containerization, CI/CD, security checks, observability-ready logging, and operational documentation.

## Architecture

```text
User / CLI / Streamlit
        |
        v
+----------------------+       +----------------------+
| Presentation Layer   |       | Safe URL Ingestion   |
| ui.py / cli.py       |------>| security.py          |
+----------+-----------+       +----------+-----------+
           |                              |
           v                              v
+-----------------------------------------------------+
| DocumentParser                                       |
| format detection -> parser selection -> normalized  |
| ParseResult contract                                |
+------------+----------------------+-----------------+
             |                      |
             v                      v
+-------------------------+   +------------------------+
| Parser Backends         |   | PDF Inspection        |
| PyMuPDF / pdfplumber    |   | scanned/hybrid/layout |
| Office / CSV / OCR      |   +------------------------+
| Docling / Unstructured  |
+------------+------------+
             |
             v
+-------------------------+      +---------------------+
| Normalized ParseResult  |----->| RAG Export         |
| content/pages/metadata  |      | chunk + provenance |
+-------------------------+      +---------------------+
```

Detailed design: [`docs/architecture.md`](docs/architecture.md).

## Engineering signals

- `src/` package layout with a thin Streamlit entry point.
- Typed runtime configuration through environment variables.
- Safe remote ingestion with scheme validation, DNS/IP checks, redirect validation, timeouts, and byte limits.
- Explicit parser/format compatibility instead of silent misuse.
- Deterministic unit and local integration tests without network calls.
- Page-aware RAG chunks with stable IDs and source provenance.
- Non-root, read-only Docker runtime with dropped Linux capabilities.
- GitHub Actions for linting, typing, tests, Docker builds, dependency audit, and CodeQL.
- ADRs explaining Python version, package structure, and ingestion security choices.

## Python version

**Python 3.11 is the reference runtime.** CI also validates Python 3.12. The project requires `>=3.11,<3.14`.

This is a conservative compatibility baseline for the mixed document/ML ecosystem rather than a “newest Python at any cost” choice. Streamlit, PyMuPDF/PyMuPDF4LLM, and current Docling releases all support modern Python versions beginning at 3.10, while 3.11 remains a mature target for OCR/ML dependency stacks.

See [`docs/decisions/001-python-runtime.md`](docs/decisions/001-python-runtime.md).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
make test
make run
```

Open `http://localhost:8501`.

### OCR support

```bash
# Ubuntu/Debian system packages
sudo apt-get install tesseract-ocr poppler-utils

# Python OCR adapter
python -m pip install -e '.[ocr]'
```

Additional backends are optional:

```bash
python -m pip install -e '.[docling]'
python -m pip install -e '.[easyocr]'
python -m pip install -e '.[unstructured]'
```

## CLI

```bash
document-parser report.pdf --output report.md
document-parser report.pdf --rag --output report.rag.json
```

Or without installing the console script:

```bash
python -m document_parser.cli report.pdf --rag
```

## Programmatic API

```python
from document_parser import DocumentParser, build_rag_json

parser = DocumentParser()
result = parser.parse("report.pdf")
rag = build_rag_json(result, "report.pdf", chunk_size=900, overlap=120)
```

## Supported formats

| Format | Extensions | Default strategy |
| --- | --- | --- |
| PDF | `.pdf` | scanned detection, then PyMuPDF4LLM/PyMuPDF or OCR |
| Word | `.docx` | python-docx |
| PowerPoint | `.pptx` | python-pptx |
| Excel | `.xlsx` | openpyxl |
| CSV | `.csv` | Python CSV parser |
| Text | `.txt`, `.md`, `.markdown`, `.html`, `.htm` | built-in text reader |

Legacy binary Office formats (`.doc`, `.ppt`, `.xls`) are deliberately **not advertised as supported**, because the selected libraries do not parse those formats reliably without conversion or additional dependencies.

## RAG export contract

The RAG exporter produces stable, page-aware chunks:

```json
{
  "schema": "rag_chunks_v1",
  "document": {
    "file_name": "report.pdf",
    "file_type": "pdf",
    "tool_used": "PyMuPDF"
  },
  "chunks": [
    {
      "id": "...",
      "text": "...",
      "metadata": {
        "page": 1,
        "chunk_index": 0
      }
    }
  ]
}
```

`overlap` must be smaller than `chunk_size`; the implementation validates this and guarantees forward progress.

## Quality commands

```bash
make lint
make typecheck
make test
make test-integration
make security
make ci
```

## Docker

```bash
docker compose up --build
```

The default image includes Tesseract + Poppler and installs the Python `ocr` extra. Heavyweight ML backends such as EasyOCR and Docling are intentionally not baked into the default runtime image.

## Security model

The public Streamlit UI allows upload and public HTTP(S) URL ingestion. Arbitrary local-path input is disabled by default.

Remote URLs are protected by:

- HTTP/HTTPS-only policy;
- no embedded URL credentials;
- private, loopback, link-local, multicast, reserved, and unspecified IP rejection;
- validation before every redirect;
- connect/read timeouts;
- content-length and streaming byte limits.

See [`SECURITY.md`](SECURITY.md) and [`docs/decisions/003-safe-remote-ingestion.md`](docs/decisions/003-safe-remote-ingestion.md).

## Dependency licensing

This repository's source code is MIT-licensed. **Dependencies retain their own licenses.** In particular, PyMuPDF and PyMuPDF4LLM are currently offered under AGPL-3.0 or a commercial Artifex license. Review [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) before redistributing or using the dependency stack in a proprietary service.

## Repository structure

```text
.
├── .github/workflows/        # CI and security automation
├── docs/                     # architecture, ADRs, runbook
├── examples/                 # minimal integration examples
├── src/document_parser/
│   ├── cli.py                # automation interface
│   ├── config.py             # typed runtime settings
│   ├── exceptions.py         # domain errors
│   ├── parser.py             # parser orchestration/backends
│   ├── rag.py                # RAG chunking/export
│   ├── security.py           # safe URL ingestion
│   ├── ui.py                 # Streamlit presentation
│   └── visualizer.py         # PDF layout visualization
├── tests/unit/
├── tests/integration/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Author

**GHANMI Helmi**  
Current Role: AI Engineer  
Past Role: Researcher in Applied Mathematics  
Research profile: https://www.researchgate.net/profile/Ghanmi-Helmi
