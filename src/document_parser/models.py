# Path: src/document_parser/models.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""Shared typing contracts for parser output."""

from __future__ import annotations

from typing import Any, TypedDict


class PageResult(TypedDict, total=False):
    page_number: int
    content: str
    bboxes: list[dict[str, Any]]
    metadata: dict[str, Any]


class ParseResult(TypedDict, total=False):
    tool_used: str
    content: str
    pages: list[PageResult]
    images: list[dict[str, Any]]
    metadata: dict[str, Any]
    pdf_analysis: dict[str, Any] | None
    errors: list[str]
    file_name: str
    file_type: str
    file_size: int
