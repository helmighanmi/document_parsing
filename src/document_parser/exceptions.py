# Path: src/document_parser/exceptions.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""Domain-specific exceptions for predictable error handling."""


class DocumentParserError(Exception):
    """Base exception for document parser failures."""


class UnsupportedDocumentError(DocumentParserError):
    """Raised when a file format or parser combination is unsupported."""


class OptionalDependencyError(DocumentParserError):
    """Raised when an optional parser dependency is not installed."""


class SourceSecurityError(DocumentParserError):
    """Raised when an external source violates ingestion security policy."""


class FileTooLargeError(DocumentParserError):
    """Raised when an input exceeds the configured size limit."""
