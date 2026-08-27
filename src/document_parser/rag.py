# Path: src/document_parser/rag.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""RAG-oriented normalization and chunk export."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from pathlib import Path
import re
from typing import Any


def _stable_id(*parts: str) -> str:
    payload = "|".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:20]


def clean_text(value: str) -> str:
    """Normalize whitespace without collapsing paragraph boundaries."""
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"\n{3,}", "\n\n", value)
    value = re.sub(r"[ \t]{2,}", " ", value)
    return value.strip()


def chunk_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    """Split text into deterministic overlapping chunks with progress guarantees."""
    if max_chars <= 0:
        raise ValueError("max_chars must be greater than zero")
    if overlap < 0:
        raise ValueError("overlap must be zero or greater")
    if overlap >= max_chars:
        raise ValueError("overlap must be smaller than max_chars")

    normalized = clean_text(text)
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    text_length = len(normalized)

    while start < text_length:
        provisional_end = min(text_length, start + max_chars)
        end = provisional_end

        if provisional_end < text_length:
            candidate = normalized[start:provisional_end]
            paragraph_cut = candidate.rfind("\n\n")
            if paragraph_cut >= max_chars // 2:
                end = start + paragraph_cut

        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break
        start = max(start + 1, end - overlap)

    return chunks


def build_rag_json(
    results: dict[str, Any],
    document_path: str | None,
    chunk_size: int = 900,
    overlap: int = 120,
) -> dict[str, Any]:
    """Build a page-aware JSON payload suitable for embedding pipelines."""
    file_name = results.get("file_name") or (Path(document_path).name if document_path else "document")
    file_type = results.get("file_type", "unknown")
    tool_used = results.get("tool_used", "unknown")

    payload: dict[str, Any] = {
        "schema": "rag_chunks_v1",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "document": {
            "file_name": file_name,
            "file_type": file_type,
            "tool_used": tool_used,
            "file_size": results.get("file_size"),
            "pdf_analysis": results.get("pdf_analysis"),
        },
        "chunks": [],
    }

    pages = results.get("pages") or []
    if pages:
        for page in pages:
            page_number = page.get("page_number")
            for chunk_index, chunk in enumerate(
                chunk_text(page.get("content", "") or "", max_chars=chunk_size, overlap=overlap)
            ):
                payload["chunks"].append(
                    {
                        "id": _stable_id(file_name, str(page_number), str(chunk_index), chunk),
                        "text": chunk,
                        "metadata": {
                            "file_name": file_name,
                            "file_type": file_type,
                            "tool_used": tool_used,
                            "page": page_number,
                            "chunk_index": chunk_index,
                        },
                    }
                )
        return payload

    for chunk_index, chunk in enumerate(
        chunk_text(results.get("content", "") or "", max_chars=chunk_size, overlap=overlap)
    ):
        payload["chunks"].append(
            {
                "id": _stable_id(file_name, "document", str(chunk_index), chunk),
                "text": chunk,
                "metadata": {
                    "file_name": file_name,
                    "file_type": file_type,
                    "tool_used": tool_used,
                    "chunk_index": chunk_index,
                },
            }
        )
    return payload
