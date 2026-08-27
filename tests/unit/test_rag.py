# Path: tests/unit/test_rag.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

from document_parser.rag import build_rag_json, chunk_text


def test_chunk_text_rejects_invalid_overlap() -> None:
    try:
        chunk_text("hello world", max_chars=10, overlap=10)
    except ValueError as exc:
        assert "smaller" in str(exc)
    else:
        raise AssertionError("Expected overlap validation to fail")


def test_chunk_text_guarantees_progress() -> None:
    text = "A" * 250
    chunks = chunk_text(text, max_chars=100, overlap=90)
    assert len(chunks) > 1
    assert all(chunks)
    assert len(chunks) < len(text)


def test_build_rag_json_preserves_page_metadata() -> None:
    result = {
        "file_name": "paper.pdf",
        "file_type": "pdf",
        "tool_used": "PyMuPDF",
        "pages": [
            {"page_number": 1, "content": "First page content."},
            {"page_number": 2, "content": "Second page content."},
        ],
    }
    payload = build_rag_json(result, None, chunk_size=50, overlap=5)
    assert payload["schema"] == "rag_chunks_v1"
    assert [chunk["metadata"]["page"] for chunk in payload["chunks"]] == [1, 2]
    assert len({chunk["id"] for chunk in payload["chunks"]}) == 2
