# Path: tests/unit/test_parser_contract.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

import pytest

from document_parser.exceptions import UnsupportedDocumentError
from document_parser.parser import DocumentParser, _easyocr_language


def test_supported_extensions_match_real_library_capabilities() -> None:
    extensions = DocumentParser.supported_extensions()
    assert ".docx" in extensions
    assert ".pptx" in extensions
    assert ".xlsx" in extensions
    assert ".csv" in extensions
    assert ".doc" not in extensions
    assert ".ppt" not in extensions
    assert ".xls" not in extensions


def test_parser_rejects_incompatible_tool() -> None:
    parser = DocumentParser(tool="python-docx")
    with pytest.raises(UnsupportedDocumentError):
        parser._validate_tool_compatibility("python-docx", "pdf")


def test_easyocr_language_mapping_is_not_tesseract_mapping() -> None:
    assert _easyocr_language("eng") == "en"
    assert _easyocr_language("fra") == "fr"
