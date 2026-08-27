# Path: src/document_parser/ui.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""Streamlit presentation layer for the document parser."""

from __future__ import annotations

from contextlib import suppress
import json
import logging
from pathlib import Path
import tempfile
from typing import Any

import streamlit as st

from .config import ParserSettings
from .exceptions import DocumentParserError
from .logging_config import configure_logging
from .parser import DocumentParser
from .rag import build_rag_json
from .visualizer import DocumentVisualizer

logger = logging.getLogger(__name__)

_TOOL_LABELS = {
    "Auto (Recommended)": None,
    "PyMuPDF": "pymupdf",
    "PyMuPDF4LLM": "pymupdf4llm",
    "pdfplumber": "pdfplumber",
    "Docling": "docling",
    "Unstructured": "unstructured",
    "Tesseract OCR": "tesseract_ocr",
    "EasyOCR": "easyocr",
    "python-docx": "python-docx",
    "python-pptx": "python-pptx",
    "openpyxl": "openpyxl",
    "Built-in CSV": "builtin_csv",
    "Built-in Text": "builtin",
}


def _parse_uploaded_file(
    uploaded_file: Any,
    parser: DocumentParser,
) -> tuple[dict[str, Any], bytes, str]:
    raw = uploaded_file.getvalue()
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as handle:
        path = Path(handle.name)
        handle.write(raw)
    try:
        result = parser.parse(str(path))
        result["file_name"] = uploaded_file.name
        return result, raw, suffix
    finally:
        with suppress(FileNotFoundError):
            path.unlink()


def _draw_uploaded_pdf(raw: bytes, suffix: str, page_number: int, bboxes: list[dict[str, Any]]) -> Any:
    with tempfile.NamedTemporaryFile(suffix=suffix or ".pdf", delete=False) as handle:
        path = Path(handle.name)
        handle.write(raw)
    try:
        return DocumentVisualizer().draw_bboxes(str(path), page_number, bboxes)
    finally:
        with suppress(FileNotFoundError):
            path.unlink()


def run() -> None:
    settings = ParserSettings.from_env()
    configure_logging(settings.log_level)
    st.set_page_config(page_title="Document Parsing Workbench", page_icon="📄", layout="wide")
    st.title("📄 Document Parsing Workbench")
    st.caption("Multi-format parsing, OCR, layout inspection, and RAG-ready export.")

    if "parsed_results" not in st.session_state:
        st.session_state.parsed_results = None
        st.session_state.source_bytes = None
        st.session_state.source_suffix = None

    input_choices = ["Upload File", "URL"]
    if settings.allow_local_path_input_in_ui:
        input_choices.append("File Path")
    input_method = st.sidebar.radio("Input Method", input_choices)

    source_value: str | None = None
    uploaded_file = None
    if input_method == "Upload File":
        uploaded_file = st.sidebar.file_uploader(
            "Choose a document",
            type=["pdf", "docx", "pptx", "xlsx", "csv", "txt", "md", "markdown", "html", "htm"],
        )
        if uploaded_file and uploaded_file.size > settings.max_file_size_bytes:
            st.sidebar.error(f"File exceeds the {settings.max_file_size_mb} MB limit.")
            uploaded_file = None
    elif input_method == "URL":
        source_value = st.sidebar.text_input("Public HTTP(S) URL").strip() or None
        st.sidebar.caption("Private/loopback network destinations are blocked by default.")
    else:
        source_value = st.sidebar.text_input("Local file path").strip() or None

    selected_label = st.sidebar.selectbox("Parser", list(_TOOL_LABELS))
    detect_scanned = st.sidebar.checkbox("Detect scanned PDFs", value=True)
    extract_images = st.sidebar.checkbox("Extract embedded PDF images", value=False)
    ocr_language = st.sidebar.selectbox("OCR language", ["eng", "fra", "deu", "spa", "ita", "por", "ara"])

    has_source = uploaded_file is not None or bool(source_value)
    if has_source and st.button("🚀 Parse Document", type="primary"):
        parser = DocumentParser(
            tool=_TOOL_LABELS[selected_label],
            detect_scanned=detect_scanned,
            extract_images=extract_images,
            ocr_lang=ocr_language,
            settings=settings,
        )
        try:
            with st.spinner("Parsing document..."):
                if uploaded_file is not None:
                    result, raw, suffix = _parse_uploaded_file(uploaded_file, parser)
                    st.session_state.source_bytes = raw
                    st.session_state.source_suffix = suffix
                else:
                    result = parser.parse(source_value or "")
                    st.session_state.source_bytes = None
                    st.session_state.source_suffix = None
                st.session_state.parsed_results = result
            st.success(f"Parsed with {result.get('tool_used', 'unknown parser')}")
        except (DocumentParserError, FileNotFoundError, ValueError) as exc:
            st.error(str(exc))
        except Exception:
            logger.exception("Unexpected parser failure")
            st.error("Unexpected parser failure. Check application logs for details.")

    result = st.session_state.parsed_results
    if not result:
        st.info("Choose a supported document and run the parser.")
        return

    metadata_col, analysis_col = st.columns(2)
    with metadata_col:
        st.subheader("Metadata")
        st.json(result.get("metadata", {}))
    with analysis_col:
        st.subheader("PDF analysis")
        st.json(result.get("pdf_analysis") or {})

    st.subheader("RAG export")
    chunk_col, overlap_col = st.columns(2)
    chunk_size = int(chunk_col.number_input("Chunk size (characters)", min_value=200, max_value=5000, value=900, step=100))
    overlap = int(overlap_col.number_input("Overlap (characters)", min_value=0, max_value=1000, value=120, step=20))
    if overlap >= chunk_size:
        st.warning("Overlap must be smaller than chunk size.")
    else:
        rag = build_rag_json(result, None, chunk_size=chunk_size, overlap=overlap)
        st.download_button(
            "⬇️ Download RAG JSON",
            json.dumps(rag, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name=f"{result.get('file_name', 'document')}.rag.json",
            mime="application/json",
        )
        st.caption(f"Chunks generated: {len(rag['chunks'])}")

    view = st.radio("View", ["Markdown", "Page by page", "Bounding boxes"], horizontal=True)
    if view == "Markdown":
        st.markdown(result.get("content", "") or "_No content extracted._")
    elif view == "Page by page":
        pages = result.get("pages") or []
        if not pages:
            st.info("This parser did not return page-level output.")
        else:
            page_index = st.slider("Page", 1, len(pages), 1) - 1
            st.markdown(pages[page_index].get("content", "") or "_No page text extracted._")
    else:
        pages = result.get("pages") or []
        raw = st.session_state.source_bytes
        if not pages or not raw or result.get("file_type") != "pdf":
            st.info("Bounding-box rendering is available for uploaded PDFs with bbox-aware parsers.")
        else:
            page_index = st.slider("Page", 1, len(pages), 1, key="bbox_page") - 1
            bboxes = pages[page_index].get("bboxes") or []
            if not bboxes:
                st.info("No bounding boxes were returned for this page.")
            else:
                image = _draw_uploaded_pdf(raw, st.session_state.source_suffix or ".pdf", page_index, bboxes)
                if image is not None:
                    st.image(image, use_container_width=True)

    images = result.get("images") or []
    if images:
        st.subheader(f"Extracted images ({len(images)})")
        columns = st.columns(3)
        for index, item in enumerate(images):
            with columns[index % 3]:
                st.image(item["image"], caption=f"Page {item.get('page', '?')} · Image {index + 1}")
