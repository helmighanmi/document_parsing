<!--
Path: docs/runbook.md
Author: GHANMI Helmi
Current Role: AI Engineer
Past Role: Researcher in Applied Mathematics
Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi
-->

# Operational Runbook

## Health

Streamlit health endpoint: `/_stcore/health` on port `8501`.

## Common failure classes

**OCR backend missing:** install Tesseract + Poppler and the Python `ocr` extra.

**Remote URL rejected:** confirm it resolves only to public IP space and stays within redirect/size limits.

**Parser mismatch:** use auto selection or choose a backend compatible with the actual file type.

**Large or slow document:** lower `MAX_FILE_SIZE_MB`, enforce platform timeouts, and isolate heavy OCR/Docling execution in a worker service before scaling beyond a demo/single-process deployment.

## Incident hygiene

Never log document bodies, credentials, or uploaded file contents. Log source name, parser, size, timing, and failure class only.
