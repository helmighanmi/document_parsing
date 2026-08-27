# Path: src/document_parser/__init__.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""Production-oriented document parsing toolkit."""

from .config import ParserSettings
from .parser import DocumentParser
from .rag import build_rag_json, chunk_text

__all__ = ["DocumentParser", "ParserSettings", "build_rag_json", "chunk_text"]
__version__ = "2.0.0"
