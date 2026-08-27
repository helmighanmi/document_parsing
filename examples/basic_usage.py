# Path: examples/basic_usage.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""Minimal programmatic parsing example."""

from document_parser import DocumentParser, build_rag_json

parser = DocumentParser()
result = parser.parse("example.pdf")
rag_payload = build_rag_json(result, "example.pdf")
print(result["tool_used"], len(rag_payload["chunks"]))
